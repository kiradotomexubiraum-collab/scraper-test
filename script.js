let data = []

fetch("./products.json")
.then(response => response.json())
.then(json => {
    data = json
})
.catch(err => console.error("Error loading products:", err))


function parsePrice(price){

    if(typeof price === "number") return price

    return Number(
        price
        .replace("R$","")
        .replace(",",".")
        .trim()
    )
}


function searchProduct(){

    const query = document
        .getElementById("search")
        .value
        .toLowerCase()

    const list = document.getElementById("results")

    list.innerHTML = ""

    if(!query) return


    const results = data
        .filter(p => p.name.toLowerCase().includes(query))
        .sort((a,b) => parsePrice(a.price) - parsePrice(b.price))


    results.forEach(p => {

        const li = document.createElement("li")

        li.textContent =
        `${p.name} — ${p.price} (${p.store})`

        list.appendChild(li)

    })

}
