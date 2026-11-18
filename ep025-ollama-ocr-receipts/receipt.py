"""Receipt image in, checked JSON out. One local model call, nothing leaves the machine."""
import sys
import time
from datetime import datetime

from ollama import chat
from pydantic import BaseModel, Field

MODEL: str = "glm-ocr:q8_0"
PROMPT: str = "Extract this receipt as JSON."
# The model copies the date as printed, so this code lists the formats it accepts.
# "%m/%d/%Y" is US order: use "%d/%m/%Y" if your receipts are day-first.
DATE_FORMATS: tuple[str, ...] = ("%Y-%m-%d", "%m/%d/%Y", "%d %b %Y")


class Item(BaseModel):
    name: str
    line_total: float = Field(description="the amount printed at the end of this line")


class Receipt(BaseModel):
    merchant: str
    date: str = Field(description="the purchase date")
    items: list[Item]
    subtotal: float
    tax: float
    total: float = Field(description="the amount after tax and before any tip")


def read_receipt(image_path: str) -> Receipt:
    reply = chat(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT, "images": [image_path]}],
        format=Receipt.model_json_schema(),
        options={"temperature": 0},
    )
    return Receipt.model_validate_json(reply.message.content)


def to_iso_date(printed: str) -> str:
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(printed.strip(), date_format).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"unknown date format {printed!r}: add it to DATE_FORMATS")


def with_iso_date(receipt: Receipt) -> Receipt:
    return receipt.model_copy(update={"date": to_iso_date(receipt.date)})


def find_problems(receipt: Receipt) -> list[str]:
    """Arithmetic the model cannot talk its way around."""
    problems: list[str] = []
    items_sum = round(sum(item.line_total for item in receipt.items), 2)
    if abs(items_sum - receipt.subtotal) > 0.005:
        problems.append(f"items add up to {items_sum:.2f}, not {receipt.subtotal:.2f}")
    if abs(receipt.subtotal + receipt.tax - receipt.total) > 0.005:
        problems.append(f"subtotal + tax is not {receipt.total:.2f}")
    return problems


def main() -> None:
    started = time.time()
    receipt = with_iso_date(read_receipt(sys.argv[1]))
    print(receipt.model_dump_json(indent=2))
    problems = find_problems(receipt)
    for problem in problems:
        print("CHECK FAILED:", problem)
    if not problems:
        print("CHECKS PASSED: items = subtotal, subtotal + tax = total")
    print(f"took {time.time() - started:.1f} s")


if __name__ == "__main__":
    main()
