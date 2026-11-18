"""Draw the made-up sample documents used in the video (nothing here is a real business or person)."""
import pathlib
import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

MONO_BOLD: str = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
SANS_BOLD: str = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SANS: str = "/System/Library/Fonts/Supplemental/Arial.ttf"

RECEIPT_LINES: list[tuple[str, str]] = [
    ("2 x Flat White", "9.50"),
    ("1 x Avocado Toast", "11.25"),
    ("1 x Blueberry Muffin", "3.75"),
    ("1 x Oat Milk (add)", "0.80"),
]


def draw_receipt() -> Image.Image:
    img = Image.new("RGB", (900, 1280), "white")
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(MONO_BOLD, 58)
    mid = ImageFont.truetype(MONO_BOLD, 34)
    d.text((450, 60), "BLUE HERON CAFE", font=big, fill="black", anchor="mt")
    d.text((450, 140), "214 Harbor St, Harbor Point", font=mid, fill="black", anchor="mt")
    d.text((450, 185), "Tel (555) 010-0142", font=mid, fill="black", anchor="mt")
    d.text((60, 270), "Date: 11/14/2026", font=mid, fill="black")
    d.text((840, 270), "08:47", font=mid, fill="black", anchor="rt")
    d.text((60, 315), "Order #1087", font=mid, fill="black")
    d.text((840, 315), "Server: Mia", font=mid, fill="black", anchor="rt")
    d.line((60, 380, 840, 380), fill="black", width=4)
    y = 410
    for name, price in RECEIPT_LINES:
        d.text((60, y), name, font=mid, fill="black")
        d.text((840, y), price, font=mid, fill="black", anchor="rt")
        y += 58
    d.line((60, y + 10, 840, y + 10), fill="black", width=4)
    y += 40
    for name, price in [("Subtotal", "25.30"), ("Tax 8.5%", "2.15")]:
        d.text((60, y), name, font=mid, fill="black")
        d.text((840, y), price, font=mid, fill="black", anchor="rt")
        y += 58
    d.text((60, y + 10), "TOTAL", font=big, fill="black")
    d.text((840, y + 10), "27.45", font=big, fill="black", anchor="rt")
    y += 110
    for name, price in [("Tip", "4.00"), ("PAID  VISA ****4417", "31.45")]:
        d.text((60, y), name, font=mid, fill="black")
        d.text((840, y), price, font=mid, fill="black", anchor="rt")
        y += 58
    d.text((450, y + 50), "Thank you! See you soon.", font=mid, fill="black", anchor="mt")
    return img


def phone_photo(receipt: Image.Image, seed: int) -> Image.Image:
    """Same receipt as a bad phone photo: tilted, soft, dim, on a dark table."""
    rng = random.Random(seed)
    paper = receipt.convert("RGBA").rotate(-7, expand=True, resample=Image.BICUBIC)
    table = Image.new("RGB", (1200, 1600), (58, 44, 36))
    table.paste(paper, ((1200 - paper.width) // 2, (1600 - paper.height) // 2), paper)
    shade = Image.linear_gradient("L").resize((1200, 1600)).rotate(90, expand=False)
    table = Image.composite(table, Image.new("RGB", table.size, (20, 16, 14)), shade.point(lambda v: 110 + v * 145 // 255))
    table = ImageEnhance.Contrast(table).enhance(0.62)
    table = ImageEnhance.Brightness(table).enhance(0.8)
    table = table.filter(ImageFilter.GaussianBlur(2.2))
    px = table.load()
    for _ in range(60000):
        x, y = rng.randrange(1200), rng.randrange(1600)
        r, g, b = px[x, y]
        n = rng.randint(-22, 22)
        px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return table.resize((750, 1000), Image.BICUBIC)


def draw_invoice() -> Image.Image:
    img = Image.new("RGB", (1400, 760), "white")
    d = ImageDraw.Draw(img)
    h1 = ImageFont.truetype(SANS_BOLD, 52)
    b = ImageFont.truetype(SANS_BOLD, 34)
    r = ImageFont.truetype(SANS, 34)
    d.text((60, 50), "NORTHWIND OFFICE SUPPLY", font=h1, fill="black")
    d.text((60, 125), "Invoice INV-2291   ·   Due 12/01/2026", font=r, fill="black")
    cols = [60, 700, 900, 1120, 1340]
    rows = [("Item", "Qty", "Unit price", "Amount"),
            ("A4 paper, 500 sheets", "12", "6.40", "76.80"),
            ("Black gel pens, box of 10", "5", "8.95", "44.75"),
            ("Stapler, heavy duty", "2", "23.50", "47.00"),
            ("Sticky notes, 12-pack", "8", "4.25", "34.00")]
    y = 210
    for i, row in enumerate(rows):
        f = b if i == 0 else r
        if i == 0:
            d.rectangle((60, y, 1340, y + 78), fill=(225, 232, 240))
        for j, cell in enumerate(row):
            if j == 0:
                d.text((cols[0] + 18, y + 20), cell, font=f, fill="black")
            else:
                d.text((cols[j + 1] - 18, y + 20), cell, font=f, fill="black", anchor="rt")
        y += 78
    for k in range(6):
        d.line((60, 210 + 78 * k, 1340, 210 + 78 * k), fill="black", width=3)
    for x in cols:
        d.line((x, 210, x, 210 + 78 * 5), fill="black", width=3)
    d.text((1340 - 18, y + 30), "Invoice total   202.55", font=b, fill="black", anchor="rt")
    return img


def draw_simple_receipt(title: str, header: list[str], lines: list[tuple[str, str]], totals: list[tuple[str, str]],
                        footer: list[tuple[str, str]]) -> Image.Image:
    img = Image.new("RGB", (900, 1280), "white")
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(MONO_BOLD, 52)
    mid = ImageFont.truetype(MONO_BOLD, 34)
    d.text((450, 60), title, font=big, fill="black", anchor="mt")
    y = 150
    for text in header:
        d.text((450, y), text, font=mid, fill="black", anchor="mt")
        y += 48
    y += 30
    d.line((60, y, 840, y), fill="black", width=4)
    y += 30
    for group in (lines, totals, footer):
        for name, price in group:
            d.text((60, y), name, font=mid, fill="black")
            d.text((840, y), price, font=mid, fill="black", anchor="rt")
            y += 58
        d.line((60, y + 6, 840, y + 6), fill="black", width=4)
        y += 36
    return img


def main() -> None:
    receipt = draw_receipt()
    receipt.save("receipt.png")
    phone_photo(receipt, 7).save("receipt-photo.jpg", quality=72)
    draw_invoice().save("invoice.png")
    hardware = draw_simple_receipt(
        "PINE & NAIL HARDWARE", ["88 Mill Road, Cedar Falls", "Date: 2026-11-15  14:02"],
        [("3 x Wood Screws 50pk", "12.60"), ("1 x Hammer 16oz", "18.99"), ("1 x Painter's Tape", "6.49"),
         ("Loyalty discount", "-5.00")],
        [("Subtotal", "33.08"), ("Tax 7%", "2.32"), ("TOTAL", "35.40")],
        [("PAID  DEBIT ****2209", "35.40")])
    market = draw_simple_receipt(
        "GREENLEAF MARKET", ["5 Orchard Lane, Westbrook", "15 Nov 2026  18:31"],
        [("Bananas 1.2 kg", "2.28"), ("Whole Milk 1L", "1.89"), ("Sourdough Loaf", "5.50"), ("Eggs x12", "4.75")],
        [("Subtotal", "14.42"), ("Tax", "0.00"), ("TOTAL", "14.42")],
        [("CASH", "20.00"), ("CHANGE", "5.58")])
    pathlib.Path("receipts").mkdir(exist_ok=True)
    phone_photo(receipt, 21).save("receipts/cafe-photo.jpg", quality=72)
    hardware.save("receipts/hardware.png")
    phone_photo(market, 23).save("receipts/market-photo.jpg", quality=72)


if __name__ == "__main__":
    main()
