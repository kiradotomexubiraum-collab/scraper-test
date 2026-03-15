// GLOBAL products variable
let products = [];

// load JSON when page loads
fetch("products.json")
.then(response => response.json())
.then(data => {

    products = data;

    // make sure prices are numbers
    products.forEach(p => {
        p.price = Number(p.price);
    });

    console.log("Products loaded:", products);

})
.catch(error => {
    console.error("Failed to load products.json", error);
});


function searchProduct() {

    const query = document.getElementById("search").value.toLowerCase();
    const results = document.getElementById("results");

    results.innerHTML = "";

    if (products.length === 0) {
        results.innerHTML = "<tr><td colspan='3'>Products not loaded yet</td></tr>";
        return;
    }

    const filtered = products.filter(p =>
        p.name.toLowerCase().includes(query)
    );

    filtered.sort((a,b)=>a.price-b.price);

    filtered.forEach(p => {

        const row = document.createElement("tr");

        row.innerHTML = `
        <td>${p.name}</td>
        <td>R$ ${p.price.toFixed(2)}</td>
        <td>${p.store}</td>
        `;

        results.appendChild(row);

    });

}
