let products = [];

fetch("products.json")
  .then(res => res.json())
  .then(data => {
    products = data;

    // convert price to number just in case
    products.forEach(p => {
      p.price = parseFloat(p.price);
    });

    console.log("Products loaded:", products);
  });


function searchProduct() {

  const query = document.getElementById("search").value.toLowerCase();

  const results = document.getElementById("results");

  results.innerHTML = "";

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
