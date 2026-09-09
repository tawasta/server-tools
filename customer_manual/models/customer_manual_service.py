import hashlib

from bs4 import BeautifulSoup

from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class CustomerManualNote(models.Model):
    """Instruction block shown in the installation-specific manual."""

    _name = "customer.manual.note"
    _description = "Manual Instruction"
    _order = "sequence, id"

    section_key = fields.Char(
        required=True,
        index=True,
        help=(
            "Stable key derived from the normalized module-category name "
            "(see CustomerManualService._topic_key_for_category). Not tied "
            "to a numeric category id, so it survives category id churn."
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
        help="Link to the original Futural documentation.",
    )


class CustomerManualSection(models.Model):
    """Admin-set "Open original manual" link for one live (module-derived)
    topic."""

    _name = "customer.manual.section"
    _description = "Manual Topic Settings"
    _order = "name"

    section_key = fields.Char(
        required=True,
        index=True,
        help="Stable key computed by "
        "CustomerManualService._topic_key_for_category(); one record "
        "anchors the admin-set link for one live topic.",
    )
    name = fields.Char(
        required=True,
        help="Last known display name of the topic, kept for readability "
        "only (the live label shown in the manual always comes from "
        "get_data()).",
    )
    manual_url = fields.Char(
        string="Original manual URL",
        help="Link shown as 'Open original manual' for this topic.",
    )

    _sql_constraints = [
        (
            "section_key_uniq",
            "unique(section_key)",
            "Only one settings record is allowed per topic.",
        ),
    ]


class CustomerManualService(models.AbstractModel):
    """Small RPC layer for the manual OWL view."""

    _name = "customer.manual.service"
    _description = "Manual Service"

    OTHER_TOPIC_KEY = "topic_other"

    @api.model
    def _normalize_topic_name(self, name):
        """Trim, collapse internal whitespace, casefold."""
        return " ".join((name or "").split()).casefold()

    @api.model
    def _topic_key_from_name(self, raw_name):
        """Deterministic key for a raw (untranslated) topic name. Two
        names that normalize equal produce an identical key, which is how
        module categories that only differ by casing/whitespace end up
        merged into a single topic instead of duplicated ones."""
        normalized = self._normalize_topic_name(raw_name)
        if not normalized:
            return self.OTHER_TOPIC_KEY
        digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]
        return f"topic_{digest}"

    @api.model
    def _topic_key_for_category(self, category):
        """category: an ir.module.category recordset (0 or 1 records)."""
        if not category:
            return self.OTHER_TOPIC_KEY
        # lang=False forces the source-language name, so the key never
        # drifts between sessions using different languages.
        raw_name = category.with_context(lang=False).name
        return self._topic_key_from_name(raw_name)

    @api.model
    def _check_edit_access(self):
        if not self.env.user.has_group("customer_manual.group_customer_manual_edit"):
            raise AccessError(_("You are not allowed to edit the customer manual."))

    @api.model
    def _hidden_category_ids(self):
        """Ids of the "Technical" category tree and the two theme
        categories, same set ir.module.module.search_panel_select_range()
        excludes from Odoo's own Apps view (base/models/ir_module.py).
        category.visible is not used for this: it defaults to True and
        core never actually reads it anywhere."""
        xmlids = (
            "base.module_category_hidden",
            "base.module_category_website_theme",
            "base.module_category_theme",
        )
        roots = self.env["ir.module.category"]
        for xmlid in xmlids:
            category = self.env.ref(xmlid, raise_if_not_found=False)
            if category:
                roots |= category

        if not roots:
            return set()

        descendants = self.env["ir.module.category"].search(
            [("id", "child_of", roots.ids)]
        )
        return set(descendants.ids)

    @api.model
    def _is_topic_visible(self, modules, hidden_category_ids):
        """modules: ir.module.module recordset for one topic. A topic is
        hidden only when none of its modules are a real application and
        every one of them sits in the Technical/Theme category tree."""
        if not modules:
            return True
        if any(module.application for module in modules):
            return True
        return any(
            module.category_id.id not in hidden_category_ids for module in modules
        )

    @api.model
    def _build_sections(self):
        """Build the live, deduplicated list of topics from installed
        modules, overlaid with each topic's admin-set link and stored
        notes."""
        notes = (
            self.env["customer.manual.note"]
            .sudo()
            .search(
                [("active", "=", True)],
                order="section_key, sequence, id",
            )
        )

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

        sections = {}
        modules_by_section = {}

        for module in modules:
            category = module.category_id
            section_key = self._topic_key_for_category(category)
            section_name = category.name if category else _("Other")

            section = sections.setdefault(
                section_key,
                {
                    "key": section_key,
                    "name": section_name,
                    "manual_url": "",
                    "visible": True,
                    "notes": notes_by_section.get(section_key, []),
                    "modules": [],
                    "module_count": 0,
                    "note_count": 0,
                },
            )
            modules_by_section.setdefault(
                section_key, self.env["ir.module.module"].sudo()
            )
            modules_by_section[section_key] |= module

            technical_description = BeautifulSoup(
                module.description_html or "",
                "html.parser",
            )

            contributors_div = technical_description.find("div", id="contributors")

            if contributors_div:
                contributors_div.decompose()

            section["modules"].append(
                {
                    "key": module.name,
                    "name": module.shortdesc or module.name,
                    "technical_name": module.name,
                    "description_html": str(technical_description) or "",
                }
            )
            section["module_count"] += 1

        settings_by_key = {
            record.section_key: record
            for record in self.env["customer.manual.section"].sudo().search([])
        }
        hidden_category_ids = self._hidden_category_ids()

        for key, section in sections.items():
            setting = settings_by_key.get(key)
            section["manual_url"] = (setting.manual_url if setting else "") or ""
            section["visible"] = self._is_topic_visible(
                modules_by_section.get(key), hidden_category_ids
            )
            section["notes"] = section.get("notes") or []
            section["note_count"] = len(section["notes"])

        return sorted(
            sections.values(),
            key=lambda section: (section["name"] or "").lower(),
        )

    @api.model
    def get_data(self):
        """Build the data structure used by the manual view."""
        section_list = self._build_sections()
        visible_sections = [section for section in section_list if section["visible"]]

        return {
            "company": self.env.company.name,
            "sections": section_list,
            "total_sections": len(visible_sections),
            "total_modules": sum(
                section["module_count"] for section in visible_sections
            ),
            "total_notes": sum(section["note_count"] for section in visible_sections),
        }

    @api.model
    def save_section_notes(self, section_key, section_name, section_notes):
        """Replace the notes of one section with the submitted list."""
        self._check_edit_access()

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

    @api.model
    def save_section_link(self, section_key, section_name, manual_url):
        """Create or update the "Open original manual" link for one topic."""
        self._check_edit_access()

        Section = self.env["customer.manual.section"].sudo()
        record = Section.search([("section_key", "=", section_key)], limit=1)
        values = {"manual_url": (manual_url or "").strip()}
        if record:
            record.write({"name": section_name or record.name, **values})
        else:
            Section.create(
                {
                    "section_key": section_key,
                    "name": section_name or section_key,
                    **values,
                }
            )
        return True
