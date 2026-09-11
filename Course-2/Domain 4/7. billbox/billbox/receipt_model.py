"""
receipt_model.py
----------------
A Pydantic model that VALIDATES an extracted receipt.

Part 3 gave us a schema that guarantees the SHAPE of the data (syntax). But shape
being valid does not mean the NUMBERS are right (semantics). This model checks the
semantics:

  - Do the line items actually add up to the stated total?
  - Is a required field (like the total) actually present?

These are SEMANTIC checks - exactly the kind a JSON schema cannot make. When a
check fails, we raise a clear error that we can feed back to Claude on a retry.
"""

from pydantic import BaseModel, field_validator, model_validator


class LineItem(BaseModel):
    name: str
    price: float


class Receipt(BaseModel):
    merchant: str
    date: str
    line_items: list[LineItem]
    stated_total: float | None
    calculated_total: float
    conflict_detected: bool

    @field_validator("stated_total")
    @classmethod
    def total_must_be_present(cls, v):
        """
        A missing total is a real problem. We reject None here so the caller can
        decide what to do - though as Part 4 explains, retrying will NOT help if
        the total is genuinely absent from the receipt.
        """
        if v is None:
            raise ValueError(
                "stated_total is missing - the receipt has no total amount."
            )
        return v

    @model_validator(mode="after")
    def totals_must_agree(self):
        """
        The SEMANTIC check a schema cannot do: the line items must sum to the
        stated total (within 1 rupee for rounding). This is the 'calculated vs
        stated' self-correction pattern from the exam.
        """
        items_sum = sum(item.price for item in self.line_items)

        # Keep our own calculation honest regardless of what the model reported.
        if abs(items_sum - self.calculated_total) > 1.0:
            raise ValueError(
                f"calculated_total ({self.calculated_total}) does not match the "
                f"actual sum of line items ({items_sum:.2f})."
            )

        if self.stated_total is not None and abs(items_sum - self.stated_total) > 1.0:
            raise ValueError(
                f"Line items sum to {items_sum:.2f}, but stated_total is "
                f"{self.stated_total}. They differ by "
                f"{abs(items_sum - self.stated_total):.2f} rupees."
            )
        return self
