"""Every receipt image in a folder becomes one CSV row."""
import csv
import pathlib
import sys
import time

from receipt import Receipt, find_problems, read_receipt, with_iso_date

IMAGE_SUFFIXES: frozenset[str] = frozenset({".png", ".jpg", ".jpeg"})
HEADER: list[str] = ["file", "merchant", "date", "subtotal", "tax", "total", "status"]


def to_row(file_name: str, receipt: Receipt, status: str) -> list[str]:
    amounts = [f"{amount:.2f}" for amount in (receipt.subtotal, receipt.tax, receipt.total)]
    return [file_name, receipt.merchant, receipt.date, *amounts, status]


def main() -> None:
    folder = pathlib.Path(sys.argv[1])
    csv_path = pathlib.Path(sys.argv[2])
    images = sorted(
        path for path in folder.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES
    )
    with csv_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        for image in images:
            started = time.time()
            receipt = with_iso_date(read_receipt(str(image)))
            problems = find_problems(receipt)
            status = "OK" if not problems else "CHECK: " + "; ".join(problems)
            writer.writerow(to_row(image.name, receipt, status))
            seconds = time.time() - started
            print(f"{image.name:<20} {receipt.merchant:<22} {receipt.date}"
                  f"  {receipt.total:>7.2f}  {status}  ({seconds:.0f} s)")
    print(f"wrote {len(images)} rows to {csv_path}")


if __name__ == "__main__":
    main()
