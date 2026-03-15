// make products global
window.products = [];

// load the JSON
fetch("products.json")
.then(res => res.json())
.then(data => {

    window.products = data;

    window.products.forEach(p=>{
        p.price = Number(p.price);
    });

    console.log("Products loaded:", window.products);

})
.catch(err => console.error("JSON load error:", err));


// make search function global
window.searchProduct = function(){

    const query = document.getElementById("search").value.toLowerCase();
    const results = document.getElementById("results");

    results.innerHTML = "";

    if(!window.products || window.products.length === 0){
        results.innerHTML = "<tr><td colspan='3'>Products not loaded yet</td></tr>";
        return;
    }

    const filtered = window.products.filter(p =>
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

        if(i === 0){
        row.style.backgroundColor = "#d4ffd4";
        }

    });

};
