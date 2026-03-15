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
        .replace("R$", "")
        .replace(",", ".")
        .trim()
    )
}


function searchProduct(){

    const query = document
        .getElementById("search")
        .value
        .toLowerCase()

    const table = document.getElementById("results")

    table.innerHTML = ""

    if(!query) return


    const results = data
        .filter(p => p.name.toLowerCase().includes(query))
        .sort((a,b) => parsePrice(a.price) - parsePrice(b.price))


    results.forEach((p,index) => {

        const row = document.createElement("tr")

        if(index === 0){
            row.style.background = "#d4ffd4"
        }

        row.innerHTML = `
        <td>${p.name}</td>
        <td>R$ ${p.price.toFixed(2)}</td>
        <td>${p.store}</td>
        `

        table.appendChild(row)

    })

}
