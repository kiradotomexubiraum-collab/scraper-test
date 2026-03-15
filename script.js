let products = [];

// load JSON
fetch("products.json")
  .then(response => response.json())
  .then(data => {
    products = data;

    // convert price to number just in case
    products.forEach(p => {
      p.price = Number(p.price);
    });

    console.log("Products loaded:", products);
  })
  .catch(err => console.error("JSON load error:", err));


function searchProduct() {

  const query = document.getElementById("search").value.toLowerCase();
  const results = document.getElementById("results");

  results.innerHTML = "";

  if (!products.length) {
    results.innerHTML = "<li>Products not loaded yet...</li>";
    return;
  }

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(query)
  );

  filtered.sort((a,b)=>a.price-b.price);

  filtered.forEach(p => {

    const li = document.createElement("li");
    li.className = "product";

    const name = document.createElement("span");
    name.className = "name";
    name.textContent = p.name;

    const price = document.createElement("span");
    price.className = "price";
    price.textContent = `R$ ${p.price.toFixed(2)}`;

    const store = document.createElement("span");
    store.className = "store";
    store.textContent = p.store;

    li.appendChild(name);
    li.appendChild(price);
    li.appendChild(store);

    results.appendChild(li);

  });

}
