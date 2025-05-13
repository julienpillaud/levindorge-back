from typing import Any


class DomainError(Exception):
    def __init__(self, detail: Any):
        self.detail = detail


class NotFoundError(DomainError):
    pass


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
