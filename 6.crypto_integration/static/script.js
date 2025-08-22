let chart;

// Dark Mode Setup
const body = document.body;
const themeSwitch = document.getElementById("themeSwitch");
if (localStorage.getItem("theme") === "dark") {
  body.classList.add("dark-mode");
  themeSwitch.checked = true;
}
themeSwitch.addEventListener("change", () => {
  body.classList.toggle("dark-mode");
  localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
});

// Form submission
document.getElementById("priceForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const crypto = document.getElementById("crypto").value.trim().toLowerCase();
  const currency = document.getElementById("currency").value.trim().toLowerCase();

  if (!crypto || !currency) return;

  fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${crypto}&vs_currencies=${currency}`)
    .then(res => res.json())
    .then(data => {
      const price = data?.[crypto]?.[currency];
      if (price) {
        document.getElementById("priceResult").innerHTML = `Price: <strong>${price} ${currency.toUpperCase()}</strong>`;
        updateChart(crypto, currency);
        saveSearchHistory(`${crypto.toUpperCase()} / ${currency.toUpperCase()}`);
      } else {
        document.getElementById("priceResult").innerHTML = `❌ Invalid crypto or currency`;
      }
    });
});

// Load Chart
function updateChart(crypto, currency) {
  fetch(`/history/${crypto}/${currency}`)
    .then(res => res.json())
    .then(data => {
      if (chart) chart.destroy();
      chart = new Chart(document.getElementById("priceChart"), {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: `${crypto.toUpperCase()} in ${currency.toUpperCase()}`,
            data: data.values,
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13, 110, 253, 0.3)',
            tension: 0.3
          }]
        },
        options: {
          responsive: true
        }
      });
    });
}

// Load Sentiment
fetch("/sentiment")
  .then(res => res.json())
  .then(data => {
    document.getElementById("sentiment").innerHTML = `${data.value} - <strong>${data.classification}</strong>`;
  });

// Load Top Coins
fetch("/top")
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector("#top-coins tbody");
    tbody.innerHTML = "";
    data.forEach((coin, i) => {
      tbody.innerHTML += `
        <tr>
          <td>${i + 1}</td>
          <td>${coin.name} (${coin.symbol.toUpperCase()})</td>
          <td>$${coin.current_price}</td>
          <td>$${coin.market_cap.toLocaleString()}</td>
        </tr>`;
    });
  });

// Search History
function saveSearchHistory(entry) {
  let history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
  if (!history.includes(entry)) {
    history.unshift(entry);
    if (history.length > 10) history.pop();
    localStorage.setItem("searchHistory", JSON.stringify(history));
    loadSearchHistory();
  }
}

function loadSearchHistory() {
  const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
  const list = document.getElementById("search-history");
  list.innerHTML = history.map(h => `<li class="list-group-item">${h}</li>`).join("");
}
loadSearchHistory();
