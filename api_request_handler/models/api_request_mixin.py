import json
import logging

import httpx

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ApiRequestMixin(models.Model):
    _name = "api.request.mixin"
    _description = "API Request Mixin"
    _order = "create_date desc"

    @api.model
    def _api_request_make(
        self,
        method,
        endpoint,
        params=None,
        content=None,
        values=None,
        files=None,
        json=None,
        headers=None,
        auth=None,
        timeout=30.0,
        verify_ssl=True,
    ) -> httpx.Response:
        """Make an API request and log it.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            endpoint (str): The API endpoint URL.
            params (dict, optional): Query parameters. Defaults to None.
            content (bytes, optional): Raw request body. Defaults to None.
            values (dict, optional): Form data values. Defaults to None.
            files (dict, optional): Files to upload. Defaults to None.
            json (dict, optional): JSON payload. Defaults to None.
            headers (dict, optional): HTTP headers. Defaults to None.
            auth (tuple, optional): Authentication credentials. Defaults to None.
            timeout (float, optional): Request timeout in seconds. Defaults to 30.0.
            verify_ssl (bool, optional): Whether to verify SSL certificate.
                                         Defaults to True.

        Returns:
            httpx.Response: The API response.

        Raises:
            ValidationError: If the request fails or the method is invalid.
        """
        method = method.upper()
        valid_methods = ["GET", "POST", "PUT", "DELETE"]

        if method not in valid_methods:
            raise ValidationError(_("Unsupported HTTP method: %s") % method)

        _logger.debug(
            "Making %s request to %s with:\n"
            "Headers: %s\n"
            "Values: %s\n"
            "Params: %s\n"
            "Content: %s\n"
            "Files: %s\n"
            "JSON: %s",
            method,
            endpoint,
            headers,
            values,
            params,
            content,
            bool(files),  # Avoid logging file contents
            json,
        )

        try:
            with httpx.Client(timeout=timeout, verify=verify_ssl) as client:
                response = client.request(
                    method,
                    endpoint,
                    headers=headers,
                    data=values,
                    params=params,
                    content=content,
                    files=files,
                    auth=auth,
                    json=json,
                )

                # Log the request
                self._api_request_log(
                    method=method,
                    endpoint=endpoint,
                    headers=headers,
                    payload=json or values,
                    params=params,
                    response=response,
                )

                # Validate the response
                self._api_request_validate(response)

                return response

        except httpx.RequestError as e:
            _logger.exception("API request failed: %s", str(e))
            self._api_request_log(
                method=method,
                endpoint=endpoint,
                headers=headers,
                payload=json or values,
                params=params,
                response=None,
                error=str(e),
            )
            return False

    @api.model
    def _api_request_validate(self, response) -> bool:
        """
        Validate the API response.
        Args:
            response (httpx.Response): The API response.

        Raises:
            ValidationError: If the response status code indicates an error.
        """
        if not 200 <= response.status_code < 300:
            error_msg = (
                f"API request failed with status {response.status_code}: "
                f"{response.text}"
            )
            _logger.error(error_msg)
            # TODO: change the error handling based on config settings?
            raise ValidationError(response.text)

        return True

    @api.model
    def _api_request_log(
        self,
        method,
        endpoint,
        params,
        payload,
        headers,
        response=None,
        error=None,
    ) -> None:
        """Log an API request to the api.request model."""
        status_code = response.status_code if response else 500
        response_text = response.text if response else str(error) or "No response"

        self.env["api.request"].sudo().create(
            {
                "method": method,
                "endpoint": endpoint,
                "params": json.dumps(params) if params else False,
                "payload": json.dumps(payload) if payload else False,
                "headers": json.dumps(headers) if headers else False,
                "response": response_text,
                "status_code": status_code,
                "successful": 200 <= status_code < 300 if response else False,
                "error_message": str(error) if error else False,
                "res_model": self._name,
                "res_id": self.id if isinstance(self, models.Model) else False,
            }
        )
