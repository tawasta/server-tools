from odoo import models


class GenericImportRunner(models.AbstractModel):
    _name = "generic.import.runner"
    _description = "Generic import runner dispatcher"

    def run_step(self, code, row_index, row, lines_by_model, state):
        """
        Dispatch to model: generic.import.runner.<code>
        If not installed -> ignore silently.
        """
        model_name = f"generic.import.runner.{code}"
        if model_name not in self.env.registry:
            return state
        return self.env[model_name].run(row_index, row, lines_by_model, state)


class GenericImportRunnerBase(models.AbstractModel):
    _name = "generic.import.runner.base"
    _description = "Base runner"

    def run(self, row_index, row, lines_by_model, state):
        return state