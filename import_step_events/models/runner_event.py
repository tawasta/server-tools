from odoo import models


class RunnerEvent(models.AbstractModel):
    _name = "generic.import.runner.event"
    _inherit = "generic.import.runner.base"
    _description = "Import Runner: Events and Registrations"

    def run(self, row_index, row, lines_by_model, state):
        state = dict(state or {})

        event = self._get_or_create_from_lines(
            "event.event",
            lines_by_model,
            row_index,
            row,
            state=state,
        )

        if event:
            state = self._set_state_record(state, "event", event)

        registration = self._get_or_create_from_lines(
            "event.registration",
            lines_by_model,
            row_index,
            row,
            state=state,
        )

        if registration:
            state = self._set_state_record(
                state,
                "event_registration",
                registration,
            )

        return state
