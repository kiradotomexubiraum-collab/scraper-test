from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Opening Festval...")
    page.goto("https://superfestval.com.br")
    page.wait_for_timeout(1000)

    # 🟢 AUTO SELECT CITY
    print("Selecting city automatically...")
    try:
        page.click("text=Cascavel", timeout=1000)
    except:
        try:
            page.locator("button").first.click()
        except:
            print("⚠️ Could not auto-select city, continuing...")

    page.wait_for_timeout(2000)

    # 🟢 OPEN OFERTAS (IMPORTANT: click, don't goto)
    print("Opening offers...")
    try:
        page.click("text=Ofertas", timeout=2000)
    except:
        print("⚠️ Could not find 'Ofertas' button")

    page.wait_for_timeout(2000)

    # 🟢 SCROLL
    print("Scrolling...")
    for _ in range(6):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1000)

    print("\n--- PRODUCTS ---\n")

    cards = page.locator("*:has-text('R$')")
    count = cards.count()

    found = 0

    for i in range(count):
        try:
            text = cards.nth(i).inner_text().strip()

            # ❌ skip garbage blocks
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

            # 🧹 FILTER BAD DATA
            if name and price:

                if (
                    len(name) < 5 or
                    name.isupper() or
                    "OFERTA" in name.upper()
                ):
                    continue

                print(f"{name} → R$ {price:.2f}")
                print("--------")
                found += 1

        except:
            pass

    if found == 0:
        print("⚠️ No clean products found (site is tricky)")

    browser.close()