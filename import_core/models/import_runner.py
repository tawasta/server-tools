from odoo import _, exceptions, models


class GenericImportRunner(models.AbstractModel):
    _name = "generic.import.runner"
    _description = "Generic import runner dispatcher"

    def run_step(self, code, row_index, row, lines_by_model, state):
        model_name = f"generic.import.runner.{code}"
        if model_name not in self.env.registry:
            return state
        return self.env[model_name].run(row_index, row, lines_by_model, state)


class GenericImportRunnerBase(models.AbstractModel):
    _name = "generic.import.runner.base"
    _description = "Base runner"

    def _clean_vals(self, vals):
        return {
            k: (v if v not in ("", None) else False)
            for k, v in (vals or {}).items()
        }

    def _build_domain(self, search_vals):
        domain = []
        for field_name, value in (search_vals or {}).items():
            if value in ("", None, False):
                continue
            domain.append((field_name, "=", value))
        return domain

    def _apply_create_state_links_to_vals(
        self,
        model_name,
        create_vals,
        search_vals,
        state,
        lines_by_model,
    ):
        create_vals = dict(create_vals or {})
        search_vals = dict(search_vals or {})
        state = dict(state or {})

        links = lines_by_model.get("_state_links", [])

        for link in links:
            if link.get("apply_on") != "create":
                continue

            if link.get("target_model") != model_name:
                continue

            source_state_key = link.get("source_state_key")
            source_record = state.get(source_state_key)

            if not source_record:
                raise exceptions.UserError(
                    _(
                        "Create state link ei löydä lähdettä.\n\n"
                        "Malli: %(model)s\n"
                        "Target field: %(field)s\n"
                        "Source state key: %(source)s\n"
                        "State keys: %(keys)s\n"
                        "State links: %(links)s"
                    )
                    % {
                        "model": model_name,
                        "field": link.get("target_field"),
                        "source": source_state_key,
                        "keys": ", ".join(sorted(state.keys())),
                        "links": str(links),
                    }
                )

            field_name = link.get("target_field")
            if not field_name:
                continue

            create_vals.setdefault(field_name, source_record.id)
            search_vals.setdefault(field_name, source_record.id)

        return create_vals, search_vals

    def _get_or_create(self, model_name, create_vals, search_vals, row_index, row):
        record = False

        domain = self._build_domain(search_vals)
        if domain:
            record = self.env[model_name].search(domain, limit=1)

        if record:
            return record

        vals = self._clean_vals(create_vals)
        if not vals:
            return False

        try:
            return self.env[model_name].create(vals)
        except Exception as e:
            raise exceptions.UserError(
                _(
                    "Virhe luotaessa tietuetta malliin %(model)s.\n\n"
                    "CSV-rivi: %(rownum)s\n"
                    "Rivin data: %(row)s\n\n"
                    "Kenttäarvot: %(vals)s\n\n"
                    "Odoo-virhe: %(error)s"
                )
                % {
                    "model": model_name,
                    "rownum": row_index,
                    "row": str(row),
                    "vals": str(vals),
                    "error": str(e),
                }
            ) from e

    def _get_or_create_from_lines(
        self,
        model_name,
        lines_by_model,
        row_index,
        row,
        state=None,
    ):
        data = lines_by_model.get(model_name) or {
            "create": [],
            "search": [],
        }

        create_vals = dict(data.get("create") or [])
        search_vals = dict(data.get("search") or [])

        create_vals, search_vals = self._apply_create_state_links_to_vals(
            model_name,
            create_vals,
            search_vals,
            state or {},
            lines_by_model,
        )

        return self._get_or_create(
            model_name,
            create_vals,
            search_vals,
            row_index,
            row,
        )

    def _state_key_for_model(self, model_name):
        return (model_name or "").replace(".", "_")

    def _set_state_record(self, state, key, record):
        if not record:
            return state

        state = dict(state or {})

        if key:
            state[key] = record

        model_key = self._state_key_for_model(record._name)
        if model_key:
            state[model_key] = record

        return state

    def run(self, row_index, row, lines_by_model, state):
        return state