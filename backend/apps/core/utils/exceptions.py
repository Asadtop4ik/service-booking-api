from typing import Any

from .exception_constants import IconTypes


class DomainException(Exception):  # noqa: N818
    def __init__(  # noqa: PLR0913
        self,
        code: int,
        ctx: dict[Any, Any] | None = None,
        show: bool = True,
        icon_type: str = IconTypes.ERROR,
        lang_code=None,
        message: str = "",
    ) -> None:
        self.code = code
        self.ctx = ctx
        self.lang_code = lang_code
        self.show = show
        self.icon_type = icon_type
        super().__init__(message)
