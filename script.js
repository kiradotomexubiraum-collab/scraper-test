// GLOBAL variable
let products = [];

// load products.json
async function loadProducts() {
    try {
        const response = await fetch("products.json");
        products = await response.json();

        // ensure price is numeric
        products.forEach(p => {
            p.price = Number(p.price);
        });

        console.log("Products loaded:", products);

    } catch (error) {
        console.error("Failed to load JSON:", error);
    }
}

// search function
function searchProduct() {

    const query = document.getElementById("search").value.toLowerCase();
    const results = document.getElementById("results");

    results.innerHTML = "";

    if (!products.length) {
        results.innerHTML = "<li>Products not loaded yet</li>";
        return;
    }

    const filtered = products.filter(p =>
        p.name.toLowerCase().includes(query)
    );

    filtered.sort((a,b)=>a.price-b.price);

    filtered.forEach(p => {

        const li = document.createElement("li");

        li.textContent =
            `${p.name} — R$ ${p.price.toFixed(2)} (${p.store})`;

        results.appendChild(li);

    });
}

// load data when page opens
loadProducts();
