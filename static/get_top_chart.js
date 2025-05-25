document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('topActivityChart').getContext('2d');

    const labels = JSON.parse(document.getElementById('chart-data').dataset.labels);
    const times = JSON.parse(document.getElementById('chart-data').dataset.times);

    const topActivityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Hours Spent',
                data: times,
                backgroundColor: 'rgba(50, 7, 63, 0.7)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Average Hours Spent Doing This Activity"
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Activity"
                    }
                }
            }
        }
    });
});
