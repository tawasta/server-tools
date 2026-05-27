from odoo import _, exceptions, models


class RunnerPartner(models.AbstractModel):
    _name = "generic.import.runner.partner"
    _inherit = "generic.import.runner.base"
    _description = "Import Runner: Partners"

    def run(self, row_index, row, lines_by_model, state):
        state = dict(state or {})

        row_type = (row.get("Tyyppi") or "").strip().lower()
        is_child = row_type == "child"
        main_partner = state.get("main_partner")

        data = lines_by_model.get("res.partner") or {
            "create": [],
            "search": [],
        }

        create_vals = dict(data.get("create") or [])
        search_vals = dict(data.get("search") or [])

        if is_child:
            if not main_partner:
                raise exceptions.UserError(
                    _(
                        "Child-kontaktirivi ilman pääkontaktia.\n\n"
                        "CSV-rivi: %(rownum)s\n"
                        "Rivin data: %(row)s\n\n"
                        "Varmista, että child-riviä ennen on main-rivi."
                    )
                    % {
                        "rownum": row_index,
                        "row": str(row),
                    }
                )

            search_vals = {}
            create_vals.setdefault("parent_id", main_partner.id)

        vals = self._clean_vals(create_vals)

        if not search_vals and not vals:
            return state

        if not vals.get("name") and not search_vals:
            raise exceptions.UserError(
                _(
                    "Partnerilta puuttuu nimi (name).\n\n"
                    "CSV-rivi: %(rownum)s\n"
                    "Rivin data: %(row)s\n\n"
                    "Kenttäarvot (partner): %(vals)s"
                )
                % {
                    "rownum": row_index,
                    "row": str(row),
                    "vals": str(vals),
                }
            )

        partner = self._get_or_create(
            "res.partner",
            create_vals,
            search_vals,
            row_index,
            row,
        )

        if not partner:
            return state

        state = self._set_state_record(state, "partner", partner)

        if is_child:
            state["_skip_rest"] = True
        else:
            state["main_partner"] = partner

        return state