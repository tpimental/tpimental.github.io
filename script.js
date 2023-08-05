document.addEventListener("DOMContentLoaded", function () {
  fetch("sorted_names.json")
    .then((response) => response.json())
    .then((data) => {
      const dataContainer = document.getElementById("dataContainer");

      data.forEach((item) => {
        const dataItem = document.createElement("div");
        dataItem.classList.add("data-item");

        const textContainer = document.createElement("span");
        textContainer.textContent = item;
        dataItem.appendChild(textContainer);

        const heartButton = document.createElement("button");
        heartButton.textContent = "❤";
        heartButton.classList.add("heart-button");
        heartButton.addEventListener("click", () => {
          increaseCounter(item);
        });
        dataItem.appendChild(heartButton);

        dataContainer.appendChild(dataItem);
      });
    })
    .catch((error) => console.error("Error fetching data:", error));
});

const counterMap = {};

function increaseCounter(value) {
  if (counterMap[value]) {
    counterMap[value]++;
  } else {
    counterMap[value] = 1;
  }

  updateCounters();
}

function updateCounters() {
  const dataItems = document.querySelectorAll(".data-item");

  dataItems.forEach((dataItem) => {
    const textContainer = dataItem.querySelector("span");
    const value = textContainer.textContent;

    const counter = counterMap[value] || 0;
    textContainer.textContent = `${value} (${counter} ❤)`;
  });
}
