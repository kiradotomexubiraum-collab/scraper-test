let products = [];

// 🟢 LOAD JSON
fetch("products.json")
.then(res => res.json())
.then(data => {
    products = data;
    window.products = data;
})
.catch(err => console.error("Error loading products:", err));


// 🟢 NORMALIZE FUNCTION
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

    // =====================================================
    // 🟢 CASE 1: GROUPED VIEW (ALL STORES)
    // =====================================================
if(selected === "all"){

    const grouped = {};

    filtered.forEach(p => {
        const key = normalize(p.name);

        if(!grouped[key]){
            grouped[key] = [];
        }

        grouped[key].push(p);
    });

    Object.values(grouped).forEach(group => {

        group.sort((a, b) => Number(a.price) - Number(b.price));

        const bestPrice = Number(group[0].price);

        group.forEach((p, i) => {

            const row = document.createElement("tr");

            let extra = "";

            if(i > 0){
                const diff = ((Number(p.price) - bestPrice) / bestPrice) * 100;
                extra = ` (+${diff.toFixed(0)}%)`;
            }

            let displayName = p.name;

            if(i > 0){
                displayName = "↳ " + p.name;
            }

            if(i === 0){
                row.style.backgroundColor = "#d4ffd4";
            }

            row.innerHTML = `
                <td>${displayName}</td>
                <td>R$ ${Number(p.price).toFixed(2)}${extra}</td>
                <td>${p.store}</td>
            `;

            results.appendChild(row);
        });

    });
}
    // =====================================================
    // 🟢 CASE 2: NORMAL VIEW (ONE STORE)
    // =====================================================
    else{

        filtered.sort((a, b) => Number(a.price) - Number(b.price));

        filtered.forEach((p, i) => {

            const row = document.createElement("tr");

            if(i === 0){
                row.style.backgroundColor = "#d4ffd4";
            }

            row.innerHTML = `
                <td>${p.name.replace(/\s+/g, " ").trim()}</td>
                <td>R$ ${Number(p.price).toFixed(2)}</td>
                <td>${p.store}</td>
            `;

            results.appendChild(row);
        });
    }

};
