from odoo import SUPERUSER_ID, api


def post_init_hook(env):
    env = api.Environment(env.cr, SUPERUSER_ID, {})
    env["ir.cron"].with_context(active_test=False).search([]).write(
        {
            "email_template_id": env.ref(
                "scheduler_error_mailer_futural_template.scheduler_error_mailer"
            ).id
        }
    )
