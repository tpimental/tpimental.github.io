document.addEventListener("DOMContentLoaded", function () {
  fetch("sorted_names.json")
    .then(response => response.json())
    .then(data => displayItems(data));
});

function displayItems(items) {
  const itemRow = document.getElementById("itemRow");

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    const itemCard = document.createElement("div");
    itemCard.classList.add("col-md-4", "mb-4");
    itemCard.innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${item.name}</h5>
          <p class="card-text">${item.description}</p>
        </div>
      </div>
    `;

    itemRow.appendChild(itemCard);
  }
}
