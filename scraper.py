import requests
from bs4 import BeautifulSoup
import json

url = "https://example.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

titles = []

for title in soup.find_all("h2"):
    titles.append(title.text.strip())

data = {
    "titles": titles
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Scraping finished.")
