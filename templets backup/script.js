document.addEventListener('DOMContentLoaded', function () {

    // Health Monitoring - Interactive Line Chart

    var ctx = document.getElementById('healthChart').getContext('2d');

    var healthData = {

        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],

        datasets: [{

            label: 'Health Trend',

            data: [75, 78, 76, 80, 78, 74, 76],

            borderColor: '#3498db',

            backgroundColor: 'rgba(52, 152, 219, 0.2)',

            fill: true,

            tension: 0.4,

            pointRadius: 5,

            pointBackgroundColor: '#3498db'

        }]

    };



    var options = {

        responsive: true,

        plugins: {

            legend: {

                position: 'top',

            },

            tooltip: {

                enabled: true

            }

        },

        scales: {

            y: {

                beginAtZero: false

            }

        }

    };



    var healthChart = new Chart(ctx, {

        type: 'line',

        data: healthData,

        options: options

    });

});