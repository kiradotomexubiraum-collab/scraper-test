let data = []

fetch("./products.json")
.then(res => res.json())
.then(json => data = json)

function searchProduct() {

    const query = document
        .getElementById("search")
        .value
        .toLowerCase()

    const results = data
        .filter(p => p.name.toLowerCase().includes(query))
        .sort((a,b) => a.price - b.price)

    const list = document.getElementById("results")

    list.innerHTML = ""

    results.forEach(p => {

        const li = document.createElement("li")

        li.textContent =
            `${p.name} — R$ ${p.price.toFixed(2)} (${p.store})`

        list.appendChild(li)

    })

}
