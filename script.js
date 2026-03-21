let products = [];

// 🟢 LOAD JSON
fetch("products.json")
.then(res => res.json())
.then(data => {
    products = data;
    window.products = data;
    console.log("Products loaded:", products);
})
.catch(err => console.error("Error loading products:", err));


// 🟢 NORMALIZE FUNCTION (fixes case + spaces + accents)
function normalize(text){
    return text
        .toLowerCase()
        .trim()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}


// 🟢 SEARCH FUNCTION
window.searchProduct = function(){

    const query = document.getElementById("search").value.toLowerCase();
    const storeFilter = document.getElementById("storeFilter").value;
    const results = document.getElementById("results");

    results.innerHTML = "";

    if(!products || products.length === 0){
        results.innerHTML = "<tr><td colspan='3'>No products loaded</td></tr>";
        return;
    }

    let filtered = products.filter(p =>
        p.name.toLowerCase().includes(query)
    );

    const selected = normalize(storeFilter);

    // 🟢 FILTER BY STORE (FIXED)
    if(selected !== "all"){
        filtered = filtered.filter(p =>
            p.store && normalize(p.store) === selected
        );
    }

    // 🟢 SORT BY PRICE
    filtered.sort((a, b) => Number(a.price) - Number(b.price));

    // 🟢 DISPLAY RESULTS
    filtered.forEach((p, i) => {

        const row = document.createElement("tr");

        // highlight cheapest
        if(i === 0){
            row.style.backgroundColor = "#d4ffd4";
        }

        row.innerHTML = `
        <td>${p.name}</td>
        <td>R$ ${Number(p.price).toFixed(2)}</td>
        <td>${p.store}</td>
        `;

        results.appendChild(row);

    });

};
