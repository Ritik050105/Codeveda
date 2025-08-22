document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    const chartSection = document.getElementById("chartSection");

    // Theme toggle
    if (localStorage.getItem("theme") === "light") {
        body.classList.remove("bg-dark", "text-white");
        themeToggle.checked = true;
    }

    themeToggle.addEventListener("change", function () {
        if (this.checked) {
            body.classList.remove("bg-dark", "text-white");
            localStorage.setItem("theme", "light");
        } else {
            body.classList.add("bg-dark", "text-white");
            localStorage.setItem("theme", "dark");
        }
    });

    // Search history
    const searchHistory = JSON.parse(localStorage.getItem("searchHistory") || "[]");
    const historyBox = document.getElementById("search-history");
    if (historyBox) {
        historyBox.innerHTML = searchHistory.map(h => `<li>${h}</li>`).join("");
    }

    // Auto price refresh
    setInterval(() => {
        const priceBox = document.getElementById("live-price");
        if (priceBox && priceBox.dataset.api) {
            fetch(priceBox.dataset.api)
                .then(res => res.json())
                .then(data => {
                    const value = data?.[Object.keys(data)[0]]?.usd;
                    if (value) priceBox.innerText = `$${value}`;
                });
        }
    }, 30000);

    // Sentiment fetch
    fetch("/sentiment").then(res => res.json()).then(data => {
        document.getElementById("sentiment").innerText =
            `${data.value} – ${data.value_classification}`;
    });

    // Historical chart
    const crypto = document.getElementById("priceChart")?.dataset.crypto;
    const currency = document.getElementById("priceChart")?.dataset.currency;
    if (crypto && currency) {
        fetch(`/history/${crypto}/${currency}`)
            .then(res => res.json())
            .then(data => {
                chartSection.style.display = "block";
                new Chart(document.getElementById("priceChart"), {
                    type: "line",
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: `${crypto.toUpperCase()} in ${currency.toUpperCase()}`,
                            data: data.values,
                            borderColor: 'rgb(255, 99, 132)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            tension: 0.4
                        }]
                    }
                });
            });
    }

    // Alerts
    const alertBox = document.getElementById("price-alert");
    const alertTarget = localStorage.getItem("alertTarget");
    const alertCrypto = localStorage.getItem("alertCrypto");

    if (alertBox && alertCrypto === crypto) {
        setInterval(() => {
            fetch(`/history/${crypto}/${currency}`).then(res => res.json()).then(data => {
                const latest = data.values.slice(-1)[0];
                if (latest >= alertTarget) {
                    alert(`🚨 Alert! ${crypto.toUpperCase()} crossed ${alertTarget}`);
                    localStorage.removeItem("alertTarget");
                    localStorage.removeItem("alertCrypto");
                }
            });
        }, 10000);
    }

    // Save alert
    document.getElementById("set-alert-btn")?.addEventListener("click", () => {
        const target = prompt("Enter price alert threshold:");
        if (target) {
            localStorage.setItem("alertTarget", target);
            localStorage.setItem("alertCrypto", crypto);
            alert("Alert set successfully!");
        }
    });
});
