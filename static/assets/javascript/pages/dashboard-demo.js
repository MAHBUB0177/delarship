"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var data_url = '/sales-dashboard-apidata/'
var stock_sales_stock_data = []
var stock_sales_sales_data = []
var stock_sales_labels = [];
$.ajax({
  method: "GET",
  url: data_url,
  success: function (data) {
    stock_sales_labels = data.stock_sales_labels;
    stock_sales_stock_data = data.stock_sales_stock_data;
    stock_sales_sales_data = data.stock_sales_sales_data;
    new SalesData();
    new StockData();
  },
  error: function (error_data) {
    console.log("error")
    console.log(error_data)
  }
})


// Dashboard Demo
// =============================================================
var SalesData =
  /*#__PURE__*/
  function () {
    function SalesData() {
      _classCallCheck(this, SalesData);

      this.init();
    }

    _createClass(SalesData, [{
      key: "init",
      value: function init() {
        // event handlers
        this.completionTasksChart();
      }
    }, {
      key: "completionTasksChart",
      value: function completionTasksChart() {
        var data = {
          labels: stock_sales_labels,
          datasets: [{
            backgroundColor: Looper.getColors('brand').indigo,
            borderColor: Looper.getColors('brand').indigo,
            data: stock_sales_sales_data
          }] // init chart bar

        };
        var canvas = $('#completion-tasks')[0].getContext('2d');
        var chart = new Chart(canvas, {
          type: 'bar',
          data: data,
          options: {
            responsive: true,
            legend: {
              display: false
            },
            title: {
              display: false
            },
            scales: {
              xAxes: [{
                gridLines: {
                  display: true,
                  drawBorder: false,
                  drawOnChartArea: false
                },
                ticks: {
                  maxRotation: 0,
                  maxTicksLimit: 3
                }
              }],
              yAxes: [{
                gridLines: {
                  display: true,
                  drawBorder: false
                },
                ticks: {
                  beginAtZero: true,
                  stepSize: 100
                }
              }]
            }
          }
        });
      }
    }]);

    return SalesData;
  }();


var StockData =
  /*#__PURE__*/
  function () {
    function StockData() {
      _classCallCheck(this, StockData);

      this.init();
    }

    _createClass(StockData, [{
      key: "init",
      value: function init() {
        // event handlers
        this.completionTasksChart();
      }
    }, {
      key: "completionTasksChart",
      value: function completionTasksChart() {
        var data = {
          labels: stock_sales_labels,
          datasets: [{
            backgroundColor: Looper.getColors('brand').indigo,
            borderColor: Looper.getColors('brand').indigo,
            data: stock_sales_stock_data
          }] // init chart bar

        };
        var canvas = $('#sales-graph')[0].getContext('2d');
        var chart = new Chart(canvas, {
          type: 'doughnut',
          data: data,
          options: {
            responsive: true,
            legend: {
              display: false
            },
            title: {
              display: false
            },
            scales: {
              xAxes: [{
                gridLines: {
                  display: true,
                  drawBorder: false,
                  drawOnChartArea: false
                },
                ticks: {
                  maxRotation: 0,
                  maxTicksLimit: 3
                }
              }],
              yAxes: [{
                gridLines: {
                  display: true,
                  drawBorder: false
                },
                ticks: {
                  beginAtZero: true,
                  stepSize: 100
                }
              }]
            }
          }
        });
      }
    }]);

    return StockData;
  }();

/**
 * Keep in mind that your scripts may not always be executed after the theme is completely ready,
 * you might need to observe the `theme:load` event to make sure your scripts are executed after the theme is ready.
 */

function setSalesGraph() {
  var data = {
    labels: stock_sales_labels,
    datasets: [{
      backgroundColor: Looper.getColors('brand').indigo,
      borderColor: Looper.getColors('brand').indigo,
      data: stock_sales_sales_data
    }] // init chart bar

  };
  var canvas = $('#sales-graph')[0].getContext('2d');
  var chart = new Chart(canvas, {
    type: 'bar',
    data: data,
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(255, 206, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(255, 159, 64, 0.2)'
    ],
    borderColor: [
      'rgba(255,99,132,1)',
      'rgba(54, 162, 235, 1)',
      'rgba(255, 206, 86, 1)',
      'rgba(75, 192, 192, 1)',
      'rgba(153, 102, 255, 1)',
      'rgba(255, 159, 64, 1)'
    ],
    options: {
      responsive: true,
      legend: {
        display: false
      },
      title: {
        display: false
      },
      scales: {
        xAxes: [{
          gridLines: {
            display: true,
            drawBorder: false,
            drawOnChartArea: false
          },
          ticks: {
            maxRotation: 0,
            maxTicksLimit: 3
          }
        }],
        yAxes: [{
          gridLines: {
            display: true,
            drawBorder: false
          },
          ticks: {
            beginAtZero: true,
            stepSize: 100
          }
        }]
      }
    }
  });
}

var endpoint = '/sales-dashboard-api/'
var defaultData = []
var labels = [];
$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    labels = data.labels
    defaultData = data.default
    setChart()
  },
  error: function (error_data) {
    console.log("error")
    console.log(error_data)
  }
})

function setChart() {
  var ctx = document.getElementById("myChart");
  var ctx2 = document.getElementById("myChart2");
  var myChart = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '# of Votes',
        data: defaultData,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          'rgba(255,99,132,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });

  var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        label: '# of Votes',
        data: defaultData,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          'rgba(255,99,132,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });
}