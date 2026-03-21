let products = [];
let selectedStore = "all";

// 🟢 LOAD PRODUCTS
fetch("products.json")
.then(res => res.json())
.then(data => {
    products = data;
})
.catch(err => console.error("Error loading products:", err));


// 🟢 NORMALIZE
function normalize(text){
    return text
        .toLowerCase()
        .trim()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}


// 🟢 DROPDOWN TOGGLE
function toggleDropdown(){
    document.querySelector(".dropdown").classList.toggle("open");
}


// 🟢 SELECT STORE
function selectStore(store){

    selectedStore = store;

    document.querySelector(".dropdown-selected").innerText =
        store === "all" ? "All Stores" : store;

    document.querySelector(".dropdown").classList.remove("open");

    searchProduct();
}


// 🟢 CLOSE DROPDOWN ON OUTSIDE CLICK
document.addEventListener("click", (e) => {
    const dropdown = document.querySelector(".dropdown");

    if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("open");
    }
});


// 🟢 SEARCH FUNCTION
window.searchProduct = function(){

    const query = document.getElementById("search").value;
    const results = document.getElementById("results");

    results.innerHTML = "";

    if(!products || products.length === 0){
        results.innerHTML = "<tr><td colspan='3'>No products loaded</td></tr>";
        return;
    }

    const selected = normalize(selectedStore);

    let filtered = products.filter(p =>
        normalize(p.name).includes(normalize(query))
    );

    if(selected !== "all"){
        filtered = filtered.filter(p =>
            p.store && normalize(p.store) === selected
        );
    }

    filtered.sort((a, b) => Number(a.price) - Number(b.price));

    // 🟢 REMOVE DUPES (frontend safety)
    const seen = new Set();
    filtered = filtered.filter(p => {
        const key = `${normalize(p.name)}-${normalize(p.store)}-${p.price}`;
        if(seen.has(key)) return false;
        seen.add(key);
        return true;
    });

    filtered.forEach((p, i) => {

        const row = document.createElement("tr");

        if(i === 0){
            row.style.backgroundColor = "#1e3a2f";
        }

        const cleanName = p.name.replace(/\s+/g, " ").trim();

        row.innerHTML = `
            <td>${cleanName}</td>
            <td>R$ ${Number(p.price).toFixed(2)}</td>
            <td>${p.store}</td>
        `;

        results.appendChild(row);
    });

};
