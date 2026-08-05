from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    data = response.data
    fields = data if isinstance(data, dict) else {}
    message = "Request could not be processed."

    if isinstance(data, dict):
        detail = data.get("detail")
        if detail is not None:
            message = str(detail)
            fields = {}
        elif data:
            first_value = next(iter(data.values()))
            if isinstance(first_value, list) and first_value:
                message = str(first_value[0])
            else:
                message = str(first_value)

    response.data = {
        "error": {
            "code": "invalid_request",
            "message": message,
            "fields": fields,
        }
    }
    return response
