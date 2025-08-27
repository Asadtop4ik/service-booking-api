from copy import deepcopy

from apps.core.error_messages import ERRORS

from .exception_constants import ErrorLanguageTypes, ErrorTypes, IconTypes


def get_error_message(code, lang_code, ctx=None) -> tuple:
    messages = ERRORS.get(code)
    message = messages.get(lang_code)
    if ctx:
        message = message.format(**ctx)
    return message, messages.get("status_code")


def get_validation_error_codes(error_code, lang_code, messages):
    """Retrieve error message and code based on the error code and language code."""
    messages = ERRORS.get(error_code, {})
    message = messages.get(
        lang_code, "Unknown error"
    )  # Default message if lang_code not found
    return [message], messages


def get_error_code_mapping():
    """Return a mapping of error codes to their corresponding numeric values."""
    return {
        "unique": 1004,
        "required": 1001,
        "invalid_choice": 1005,
        "does_not_exist": 1006,
    }


def format_error_response(
    error_data=None,
    exception_instance=None,
    icon_type=IconTypes.ERROR,
    error_type=ErrorTypes.VALIDATION_ERROR,
    lang_code=ErrorLanguageTypes.RU,
) -> tuple:
    if error_type == ErrorTypes.VALIDATION_ERROR:
        return handle_validation_error(error_data, icon_type, error_type, lang_code)
    if error_type == ErrorTypes.DOMAIN_ERROR:
        return handle_domain_error(exception_instance, icon_type, error_type, lang_code)
    if error_type == ErrorTypes.SERVER_ERROR:
        return handle_server_error(exception_instance, icon_type, error_type, lang_code)

    return [], 500


def handle_validation_error(error_data, icon_type, error_type, lang_code):
    error_response = []
    status_code = 400
    base_template = {
        "key": None,
        "code": None,
        "show": True,
        "icon_type": icon_type,
        "type": error_type,
        "messages": [],
    }

    for key, messages in error_data.items():
        current_template = deepcopy(base_template)
        localized_messages = messages
        final_key = key

        for message_code, error_code in get_error_code_mapping().items():
            if isinstance(messages, dict):
                for field, errors in messages.items():
                    if (
                        errors
                        and hasattr(errors[0], "code")
                        and message_code == errors[0].code
                    ):
                        localized_messages, status = get_validation_error_codes(
                            error_code, lang_code, messages
                        )
                        current_template["code"] = error_code
                        final_key = field or key
                        break
            elif hasattr(messages[0], "code") and message_code == messages[0].code:
                localized_messages, status = get_validation_error_codes(
                    error_code, lang_code, messages
                )
                current_template["code"] = error_code
                break

        current_template.update(
            {
                "key": final_key,
                "messages": localized_messages,
            }
        )
        error_response.append(current_template)

    return error_response, status_code


def handle_domain_error(exception_instance, icon_type, error_type, lang_code):
    error_code = exception_instance.code
    ctx = exception_instance.ctx
    lang = exception_instance.lang_code or lang_code
    show = exception_instance.show
    icon = exception_instance.icon_type

    message, status_code = get_error_message(error_code, lang, ctx=ctx)

    error_template = {
        "key": None,
        "code": error_code,
        "show": show,
        "icon_type": icon,
        "type": error_type,
        "messages": [message],
    }

    return [error_template], status_code


def handle_server_error(exception_instance, icon_type, error_type, lang_code):
    error_template = {
        "key": None,
        "code": None,
        "show": True,
        "icon_type": icon_type,
        "type": error_type,
        "messages": [],
    }
    status_code = 500

    error_code = getattr(exception_instance, "code", None)
    if error_code:
        messages, status = get_validation_error_codes(error_code, lang_code, [])
        status_code = status.get("status_code", status_code)
        error_template.update(
            {
                "code": error_code,
                "messages": messages,
            }
        )
    else:
        error_template["messages"].append(str(exception_instance))

    return error_template, status_code
