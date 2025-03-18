const searchField = document.querySelector("#searchField");
const tableSearch = document.querySelector(".table-search");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tBody = document.querySelector(".table-body");
const noResults = document.querySelector(".no-results");

tableSearch.style.display = "none";
searchField.addEventListener("keyup", (e) => {
  searchValue = e.target.value;
  console.log(searchValue);
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tBody.innerHTML = "";
    fetch("search_expenses", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        tableSearch.style.display = "block";
        if (data.length === 0) {
          noResults.style.display = "block";
          tableSearch.style.display = "none";
        } else {
          data.forEach((item) => {
            tBody.innerHTML += `   
             <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
              </tr>`;
          });
        }
      });
  } else {
    tableSearch.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
