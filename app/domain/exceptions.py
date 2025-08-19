from typing import Any

from cleanstack.exceptions import DomainError


class UnprocessableContentError(DomainError):
    def __init__(self, invalid_refs: list[tuple[str, Any]]):
        self.detail = [
            {
                "type": "value_error",
                "loc": ["body", field],
                "msg": f"{field} '{value}' not found.",
                "input": value,
            }
            for field, value in invalid_refs
        ]
