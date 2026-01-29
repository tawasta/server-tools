import json
from odoo import SUPERUSER_ID
from odoo.api import Environment


_MAX_TEXT = 20000


def _truncate(text: str, limit: int = _MAX_TEXT) -> str:
    if not text:
        return ""
    return text if len(text) <= limit else text[:limit] + "\n...[truncated]..."


def _dump(val) -> str:
    if val is None:
        return ""
    if isinstance(val, (dict, list, int, float, bool)):
        try:
            return json.dumps(val, ensure_ascii=False)
        except Exception:
            return _truncate(str(val))
    return _truncate(str(val))


def log_fastapi_call(
    env: Environment,
    *,
    method: str,
    path: str,
    payload=None,
    response=None,
    status_code: int = 200,
):
    """
    Minimal helper that writes one log row.
    Call it at the END of your FastAPI endpoint function.

    Example:
        result = {...}
        log_fastapi_call(env, method="GET", path="/x", payload=params, response=result)
        return result
    """

    admin_env = Environment(env.cr, SUPERUSER_ID, dict(env.context))

    vals = {
        "method": method,
        "path": path,
        "odoo_user_id": env.user.id if env and env.user else False,
        "payload": _dump(payload),
        "response": _dump(response),
        "status_code": int(status_code or 0),
    }

    admin_env["fastapi.rest.log"].create(vals)
