from .core import CORE_ERRORS
from .user import USER_ERRORS

ERROR_START_NUMBERS = {
    1: "core",
    2: "users",
}


ERRORS = {
    **CORE_ERRORS,
    **USER_ERRORS,
}
