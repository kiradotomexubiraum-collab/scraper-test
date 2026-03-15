let data = []

fetch("./products.json")
.then(res => res.json())
.then(json => data = json)

function parsePrice(price) {
    return Number(
        price
        .replace("R$", "")
        .replace(",", ".")
        .trim()
    )
}

function searchProduct() {

    const query = document
        .getElementById("search")
        .value
        .toLowerCase()

    const results = data
        .filter(p => p.name.toLowerCase().includes(query))
        .sort((a,b) => parsePrice(a.price) - parsePrice(b.price))

    const list = document.getElementById("results")

    list.innerHTML = ""

    results.forEach(p => {

        const li = document.createElement("li")

        li.textContent =
            `${p.name} — ${p.price} (${p.store})`

        list.appendChild(li)

    })
}
