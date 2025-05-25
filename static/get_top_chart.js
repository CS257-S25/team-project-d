document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('topActivityChart').getContext('2d');

    const labels = JSON.parse(document.getElementById('get_top-data').dataset.labels);
    const times = JSON.parse(document.getElementById('get_top-data').dataset.times);

    const topActivityChart = new Chart(ctx, {
        type: 'bar',
        data: { 
            labels: labels,
            datasets: [{
                label: 'Average Hours Spent Doing This Activity',
                data: times,
                backgroundColor: ['rgba(55,20,88, 0.7)', 'rgba(146, 183, 150,0.7)', 'rgba(148, 199, 188, 0.7)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Average Hours Spent"
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Activity"
                    },
                    ticks: {
                        maxRotation: 0,
                        minRotation: 0
                    }
                }
            }
        }
    });
});
