from playwright.sync_api import sync_playwright
import re
import json
import os

FILE = "products.json"

# 🟢 load existing products
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)
else:
    existing = []

# 🟢 remove old Festval data
existing = [p for p in existing if p.get("store") != "Festval"]

new_products = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Opening Festval...")
    page.goto("https://superfestval.com.br")
    page.wait_for_timeout(2000)

    # 🟢 AUTO SELECT CITY
    try:
        page.click("text=Curitiba", timeout=2000)
    except:
        try:
            page.locator("button").first.click()
        except:
            print("⚠️ Could not auto-select city")

    page.wait_for_timeout(6000)

    # 🟢 OPEN OFERTAS
    try:
        page.click("text=Ofertas", timeout=2000)
    except:
        print("⚠️ Could not open ofertas")

    page.wait_for_timeout(1500)

    # 🟢 SCROLL
    for _ in range(6):
        page.mouse.wheel(0, 10000)
        page.wait_for_timeout(1000)

    print("Extracting Festval products...")

    cards = page.locator("*:has-text('R$')")
    count = cards.count()

    for i in range(count):
        try:
            text = cards.nth(i).inner_text().strip()

            if "CATEGORIAS" in text.upper():
                continue

            lines = text.split("\n")

            name = None
            price = None

            for line in lines:

                if "R$" in line:
                    match = re.search(r"R\$ ?([0-9]+,[0-9]+)", line)
                    if match:
                        price = float(match.group(1).replace(",", "."))

                else:
                    if len(line) > 5 and not name:
                        name = line.strip()

            # 🧹 filter garbage
            if name and price:
                if (
                    len(name) < 5 or
                    name.isupper() or
                    "OFERTA" in name.upper()
                ):
                    continue

                new_products.append({
                    "store": "Festval",
                    "name": name,
                    "price": price
                })

        except:
            pass

    browser.close()

# 🟢 merge data
final_products = existing + new_products

# 🟢 save
with open(FILE, "w", encoding="utf-8") as f:
    json.dump(final_products, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {len(new_products)} Festval products")
