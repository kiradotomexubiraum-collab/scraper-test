from playwright.sync_api import sync_playwright
import json
import re

categories = [
    "https://muffataosupermercado.instabuy.com.br/cat/Frutas-Legumes-e-Verduras",
    "https://muffataosupermercado.instabuy.com.br/cat/Acougue-Aves-e-Peixaria",
    "https://muffataosupermercado.instabuy.com.br/cat/Bebidas",
    "https://muffataosupermercado.instabuy.com.br/cat/Mercearia",
    "https://muffataosupermercado.instabuy.com.br/cat/Laticinios",
    "https://muffataosupermercado.instabuy.com.br/cat/Alimentos-Basicos",
    "https://muffataosupermercado.instabuy.com.br/cat/Bebidas-Nao-Alcoolicas",
    "https://muffataosupermercado.instabuy.com.br/cat/Matinais",
    "https://muffataosupermercado.instabuy.com.br/cat/Frios",
    "https://muffataosupermercado.instabuy.com.br/cat/Padaria"
]

products = []

ignore_words = [
    "ver todos", "ofertas", "categorias",
    "buscar", "menu", "carrinho"
]

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for url in categories:

        print("Scraping:", url)

        page.goto(url)
        page.wait_for_timeout(6000)

        # scroll to load products
        for i in range(6):
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(1500)

        text = page.inner_text("body")
        lines = text.split("\n")

        current_name = None

        for line in lines:

            line = line.strip()

            if not line:
                continue

            lower = line.lower()

            if any(word in lower for word in ignore_words):
                continue

            if "R$" in line and current_name:

                price_text = re.sub(r"[^0-9,]", "", line)

                if price_text:

                    price = float(price_text.replace(",", "."))

                    products.append({
                        "store": "Muffatao",
                        "name": current_name,
                        "price": price
                    })

                    current_name = None

            else:

                if (
                    len(line) > 6
                    and "R$" not in line
                    and not line.isupper()
                ):
                    current_name = line


    browser.close()


# merge with existing products
try:
    with open("products.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
except:
    existing = []

existing.extend(products)

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print("Muffatao categories scraped")
