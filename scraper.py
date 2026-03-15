from playwright.sync_api import sync_playwright

base_url = "https://irani.delivery/pacaembu/ofertas-clube?page={}"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    max_pages = 21

    for page_number in range(1, max_pages + 1):

        print(f"\n--- PAGE {page_number} ---\n")

        page.goto(base_url.format(page_number))

        page.wait_for_timeout(5000)

        text = page.inner_text("body")
        lines = text.split("\n")

        current_name = None

        for line in lines:

            if "R$" in line:
                if current_name:
                    print(f"{current_name} — {line}")

            else:
                if len(line) > 3 and "OFF" not in line and "Add" not in line:
                    current_name = line

    browser.close()
