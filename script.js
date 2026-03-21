let products = [];

// 🟢 LOAD PRODUCTS
fetch("products.json")
.then(res => res.json())
.then(data => {
    products = data;
    window.products = data;
    console.log("Loaded products:", products);
})
.catch(err => console.error("Error loading products:", err));


// 🟢 NORMALIZE FUNCTION (fix case, accents, spaces)
function normalize(text){
    return text
        .toLowerCase()
        .trim()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}


// 🟢 MAIN SEARCH FUNCTION
window.searchProduct = function(){

    const query = document.getElementById("search").value;
    const storeFilter = document.getElementById("storeFilter").value;
    const results = document.getElementById("results");

    results.innerHTML = "";

    if(!products || products.length === 0){
        results.innerHTML = "<tr><td colspan='3'>No products loaded</td></tr>";
        return;
    }

    const selected = normalize(storeFilter);

    // 🟢 FILTER BY NAME
    let filtered = products.filter(p =>
        normalize(p.name).includes(normalize(query))
    );

    // 🟢 FILTER BY STORE
    if(selected !== "all"){
        filtered = filtered.filter(p =>
            p.store && normalize(p.store) === selected
        );
    }

    // 🟢 SORT BY PRICE (cheapest first)
    filtered.sort((a, b) => Number(a.price) - Number(b.price));

    // 🟢 REMOVE DUPLICATES (frontend safety)
    const seen = new Set();
    filtered = filtered.filter(p => {
        const key = `${normalize(p.name)}-${normalize(p.store)}-${Number(p.price)}`;
        if(seen.has(key)) return false;
        seen.add(key);
        return true;
    });

    // 🟢 DISPLAY RESULTS
    filtered.forEach((p, i) => {

        const row = document.createElement("tr");

        // highlight cheapest overall
        if(i === 0){
            row.style.backgroundColor = "#d4ffd4";
        }

        // clean product name (fix broken spacing)
        const cleanName = p.name.replace(/\s+/g, " ").trim();

        row.innerHTML = `
            <td>${cleanName}</td>
            <td>R$ ${Number(p.price).toFixed(2)}</td>
            <td>${p.store}</td>
        `;

        results.appendChild(row);
    });

};
