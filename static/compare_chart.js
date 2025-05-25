Chart.defaults.font.family = "Georgia, 'Times New Roman', Times, serif";

document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('CompareChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['2022 & 2023', '2012 & 2013'],
            datasets: [{
                label: `Avg Hours Spent on ${compareData.activity}`,
                data: [compareData.hours_0, compareData.hours_1],
                backgroundColor: ['rgba(55,20,88, 0.7)', 'rgba(146, 183, 150,0.7)']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Average Hours'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Years'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: `Activity Comparison for Age ${compareData.age}`
                },
                legend: {
                    display: false
                }
            }
        }
    });
});
