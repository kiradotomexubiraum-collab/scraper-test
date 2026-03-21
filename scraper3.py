from playwright.sync_api import sync_playwright
import re
import json
import os

FILE = "products.json"

# 🟢 LOAD EXISTING DATA
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)
else:
    existing = []

# 🟢 REMOVE OLD FESTVAL DATA
existing = [p for p in existing if p.get("store") != "Festval"]

# 🟢 DEDUP TRACKER
seen = set()
new_products = []

def normalize(text):
    return (
        text.lower()
        .strip()
        .replace("\n", " ")
    )

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://superfestval.com.br")
    page.wait_for_timeout(1000)

    # 🟢 AUTO SELECT CITY
    try:
        page.click("text=Cascavel", timeout=500)
    except:
        pass

    page.wait_for_timeout(1000)

    # 🟢 OPEN OFERTAS
    try:
        page.click("text=Ofertas", timeout=500)
    except:
        pass

    page.wait_for_timeout(1000)

    # 🟢 SCROLL
    for _ in range(6):
        page.mouse.wheel(0, 10000)
        page.wait_for_timeout(500)

    # 🟢 EXTRACT
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

            if name and price:

                key = (
                    normalize(name),
                    round(price, 2),
                    "festval"
                )

                # 🟢 REMOVE DUPLICATES HERE
                if key in seen:
                    continue

                seen.add(key)

                new_products.append({
                    "store": "Festval",
                    "name": name.strip(),
                    "price": price
                })

        except:
            pass

    browser.close()

# 🟢 MERGE DATA
final_products = existing + new_products

# 🟢 SAVE JSON
with open(FILE, "w", encoding="utf-8") as f:
    json.dump(final_products, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {len(new_products)} Festval products (no duplicates)")
