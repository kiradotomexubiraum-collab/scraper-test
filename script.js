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
    li.className = "product";

    const name = document.createElement("span");
    name.className = "name";
    name.textContent = p.name;

    const price = document.createElement("span");
    price.className = "price";
    price.textContent = `R$ ${Number(p.price).toFixed(2)}`;

    const store = document.createElement("span");
    store.className = "store";
    store.textContent = p.store;

    li.appendChild(name);
    li.appendChild(price);
    li.appendChild(store);

    results.appendChild(li);

  });

}
