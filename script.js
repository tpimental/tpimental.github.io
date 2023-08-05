document.addEventListener("DOMContentLoaded", function () {
  fetch("sorted_names.json")
    .then((response) => response.json())
    .then((data) => {
      const dataContainer = document.getElementById("dataContainer");

      data.forEach((item) => {
        const dataItem = document.createElement("div");
        dataItem.classList.add("data-item");
        dataItem.textContent = item;
        dataContainer.appendChild(dataItem);
      });
    })
    .catch((error) => console.error("Error fetching data:", error));
});
