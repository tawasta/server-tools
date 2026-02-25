from odoo import _, exceptions, models


class RunnerPartner(models.AbstractModel):
    _name = "generic.import.runner.partner"
    _inherit = "generic.import.runner.base"
    _description = "Import Runner: Partners"

    def _clean_vals(self, vals: dict) -> dict:
        return {k: (v if v not in ("", None) else False) for k, v in (vals or {}).items()}

    def _build_domain(self, search_vals: dict):
        domain = []
        for field_name, value in (search_vals or {}).items():
            if value in ("", None, False):
                continue
            domain.append((field_name, "=", value))
        return domain

    def run(self, row_index, row, lines_by_model, state):
        state = dict(state or {})

        row_type = (row.get("Tyyppi") or "").strip().lower()
        is_child = row_type == "child"
        main_partner = state.get("main_partner")

        data = lines_by_model.get("res.partner") or {"create": [], "search": []}
        partner_create_vals = dict(data.get("create") or [])
        partner_search_vals = dict(data.get("search") or [])

        if is_child:
            if not main_partner:
                raise exceptions.UserError(
                    _(
                        "Child-kontaktirivi ilman pääkontaktia.\n\n"
                        "CSV-rivi: %(rownum)s\n"
                        "Rivin data: %(row)s\n\n"
                        "Varmista, että child-riviä ennen on main-rivi."
                    )
                    % {"rownum": row_index, "row": str(row)}
                )
            partner_search_vals = {}
            partner_create_vals.setdefault("parent_id", main_partner.id)

        partner = False
        domain = self._build_domain(partner_search_vals)
        if domain:
            partner = self.env["res.partner"].search(domain, limit=1)

        if not partner:
            if not partner_create_vals:
                return state

            vals = self._clean_vals(partner_create_vals)
            if not vals.get("name"):
                raise exceptions.UserError(
                    _(
                        "Partnerilta puuttuu nimi (name).\n\n"
                        "CSV-rivi: %(rownum)s\n"
                        "Rivin data: %(row)s\n\n"
                        "Kenttäarvot (partner): %(vals)s"
                    )
                    % {"rownum": row_index, "row": str(row), "vals": str(vals)}
                )

            try:
                partner = self.env["res.partner"].create(vals)
            except Exception as e:
                raise exceptions.UserError(
                    _(
                        "Virhe luotaessa partneria.\n\n"
                        "CSV-rivi: %(rownum)s\n"
                        "Rivin data: %(row)s\n\n"
                        "Kenttäarvot (partner): %(vals)s\n\n"
                        "Odoo-virhe: %(error)s"
                    )
                    % {
                        "rownum": row_index,
                        "row": str(row),
                        "vals": str(vals),
                        "error": str(e),
                    }
                ) from e

        state["partner"] = partner
        if not is_child:
            state["main_partner"] = partner
        else:
            state["_skip_rest"] = True

        return state