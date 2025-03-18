const ctx = document.getElementById("myChart");
const renderChart = (data, labels) => {
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "6 oylik ko'rsatkich",
          data: data,
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses per category",
      },
      font: {
        size: 18,
      },
    },
  });
};
const getChartData = () => {
  console.log("fetching");
  fetch("/expense_category_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("result", results);
      const category_data = results.expense_category_date;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
      renderChart(data, labels);
    });
};
document.addEventListener("DOMContentLoaded", getChartData);
