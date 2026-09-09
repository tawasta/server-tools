from odoo import api, fields, models
import logging
from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)


class CustomerManualNote(models.Model):
    """Instruction block shown in the installation-specific manual."""

    _name = "customer.manual.note"
    _description = "Manual Instruction"
    _order = "sequence, id"

    section_key = fields.Char(
        required=True,
        index=True,
        help=(
            "Technical section key used by the OWL view. "
            "At the moment sections are based on module categories, "
            "for example category_12."
        ),
    )
    section_name = fields.Char(
        required=True,
        help=(
            "Section name shown to the user. Stored on the note as well, "
            "so the instruction is still understandable if the category name changes."
        ),
    )
    title = fields.Char(
        string="Title",
        translate=True,
        help="Heading shown above the instruction text.",
    )
    body_html = fields.Html(
        string="Body",
        sanitize=True,
        translate=True,
        help="Rich text instruction content edited in the manual view.",
    )
    sequence = fields.Integer(
        default=10,
        help="Order of the instruction inside its section.",
    )
    active = fields.Boolean(
        default=True,
        help="Hidden instructions can be restored later if needed.",
    )

    manual_url = fields.Char(
        string="Original manual URL",
        help="Link to the original Futural documentation."
    )


class CustomerManualService(models.AbstractModel):
    """Small RPC layer for the manual OWL view."""

    _name = "customer.manual.service"
    _description = "Manual Service"

    @api.model
    def get_data(self):
        """Build the data structure used by the manual view."""
        sections = {}

        notes = (
            self.env["customer.manual.note"]
            .sudo()
            .search(
                [("active", "=", True)],
                order="section_key, sequence, id",
            )
        )

        # Group notes first so they can be attached while sections are built.
        notes_by_section = {}
        for note in notes:
            notes_by_section.setdefault(note.section_key, []).append(
                {
                    "id": note.id,
                    "title": note.title or "",
                    "body_html": note.body_html or "",
                    "sequence": note.sequence,
                    "manual_url": note.manual_url,
                }
            )

        modules = (
            self.env["ir.module.module"]
            .sudo()
            .search(
                [("state", "=", "installed")],
                order="category_id, shortdesc, name",
            )
        )

        for module in modules:
            category = module.category_id
            section_id = category.id if category else 0
            section_name = category.name if category else "Other"
            section_key = f"category_{section_id}"

            module_manual_url = module.website or ""

            # One section can contain many installed modules.
            section = sections.setdefault(
                section_key,
                {
                    "key": section_key,
                    "id": section_id,
                    "name": section_name,
                    "manual_url": module_manual_url,
                    "notes": notes_by_section.get(section_key, []),
                    "modules": [],
                    "module_count": 0,
                    "note_count": 0,
                },
            )

            if not section.get("manual_url") and module_manual_url:
                section["manual_url"] = module_manual_url

            technical_description = BeautifulSoup(
                module.description_html or "",
                "html.parser",
            )

            contributors_div = technical_description.find("div", id="contributors")

            if contributors_div:
                contributors_div.decompose()

            updated_technical_description = str(technical_description)

            # Technical module details are only shown in the maintainer section.
            section["modules"].append(
                {
                    "key": module.name,
                    "name": module.shortdesc or module.name,
                    "technical_name": module.name,
                    "description_html": updated_technical_description or "",
                }
            )
            section["module_count"] += 1

        section_list = sorted(
            sections.values(),
            key=lambda section: (section["name"] or "").lower(),
        )

        # Keep counters in Python so the template stays simple.
        for section in section_list:
            section["notes"] = section.get("notes") or []
            section["note_count"] = len(section["notes"])

        return {
            "company": self.env.company.name,
            "sections": section_list,
            "total_sections": len(section_list),
            "total_modules": sum(section["module_count"] for section in section_list),
            "total_notes": sum(section["note_count"] for section in section_list),
        }

    @api.model
    def save_section_notes(self, section_key, section_name, section_notes):
        """Replace the notes of one section with the submitted list."""
        Note = self.env["customer.manual.note"].sudo()
        existing_notes = Note.search([("section_key", "=", section_key)])
        kept_ids = set()

        for index, note in enumerate(section_notes or []):
            if not isinstance(note, dict):
                continue

            values = {
                "section_key": section_key,
                "section_name": section_name or section_key,
                "title": note.get("title") or "",
                "body_html": note.get("body_html") or "",
                "manual_url": note.get("manual_url") or "",
                "sequence": (index + 1) * 10,
                "active": True,
            }

            note_id = note.get("id")
            record = (
                Note.browse(note_id).exists() if isinstance(note_id, int) else False
            )

            # Never update a note from another section by accident.
            if record and record.section_key == section_key:
                record.write(values)
            else:
                record = Note.create(values)

            kept_ids.add(record.id)

        # Missing records were removed in the UI.
        existing_notes.filtered(lambda item: item.id not in kept_ids).unlink()
        return True