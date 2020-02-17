$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "url",
    data: $("pid").val(),
    dataType: "json",
    success: function (response) {
      
    }
  });
});
var randomScalingFactor = function() {
  return Math.floor((Math.random() * 100000) + 1);
};
var randomScalingFactorPer = function() {
  return Math.round(Math.random() * 100);
};

var config1 = {
  type: 'line',
  data: {
    labels: ['Nov 1', 'Nov 2', 'Nov 3', 'Nov 4', 'Nov 5', 'Nov 6', 'Nov 7'],
    datasets: [{
      label: 'Successful Logins',
      backgroundColor: window.chartColors.low,
      borderColor: window.chartColors.low,
      data: [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
      ],
      fill: false,
    }, {
      label: 'Failed Logins',
      fill: false,
      backgroundColor: window.chartColors.high,
      borderColor: window.chartColors.high,
      data: [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
      ],
    }]
  },
  options: {
    responsive: true,
    title: {
      display: false,
      //text: 'Chart.js Line Chart'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Date'
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Attempts'
        },
        ticks: {
          min: 0,
          max: 100000,

          // forces step size to be 5 units
          stepSize: 20000
        }
      }]
    },
    elements: {
      line: {
        tension: 0
      }
    }
  }
};

var config2 = {
  type: 'line',
  data: {
    labels: ['Nov 1', 'Nov 2', 'Nov 3', 'Nov 4', 'Nov 5', 'Nov 6', 'Nov 7'],
    datasets: [{
      label: 'Others',
      backgroundColor: window.chartColors.gold,
      borderColor: window.chartColors.gold,
      data: [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
      ],
      fill: false,
    }, {
      label: 'Brute Force',
      fill: false,
      backgroundColor: window.chartColors.low,
      borderColor: window.chartColors.low,
      data: [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
      ],
    }, {
      label: 'Credential Stuffing',
      fill: false,
      backgroundColor: window.chartColors.high,
      borderColor: window.chartColors.high,
      data: [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
      ],
    }]
  },
  options: {
    responsive: true,
    title: {
      display: false,
      //text: 'Chart.js Line Chart'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Date'
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Attempts'
        },
        ticks: {
          min: 0,
          max: 100000,

          // forces step size to be 5 units
          stepSize: 20000
        }
      }]
    }
  }
};

var config3 = {
  type: 'horizontalBar',
  data: {
    labels: ['India', 'United States', 'United Arab Emirates', 'United Kingdom', 'Finland'],
    datasets: [{
      label: 'Good Users',
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      borderWidth: 1,
      data: [
        randomScalingFactorPer(),
        randomScalingFactorPer(),
        randomScalingFactorPer(),
        randomScalingFactorPer(),
        randomScalingFactorPer()
      ]
    }, {
      label: 'Bad Users',
      backgroundColor: window.chartColors.high,
      borderColor: window.chartColors.high,
      data: [
        randomScalingFactorPer(),
        randomScalingFactorPer(),
        randomScalingFactorPer(),
        randomScalingFactorPer(),
        randomScalingFactorPer()
      ]
    }]

  },
  options: {
    // Elements options apply to all of the options unless overridden in a dataset
    // In this case, we are setting the border of each horizontal bar to be 2px wide
    elements: {
      rectangle: {
        borderWidth: 2,
      }
    },
    responsive: true,
    legend: {
      position: 'right',
    },
    title: {
      display: false,
      //text: 'Chart.js Horizontal Bar Chart'
    },
    scales: {
      xAxes: [{
        display: true,
        ticks: {
          min: 0,
          max: 100,

          // forces step size to be 5 units
          stepSize: 20,
          callback: function (value) {
            return value + '%'; // convert it to percentage
          },
        },
        scaleLabel: {
          display: true,
          labelString: 'Percentage'
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Countries'
        }
      }]
    }
  }
};

/* window.onload = function() {
  var ctx1 = document.getElementById('attemptsChart').getContext('2d');
  window.myLine = new Chart(ctx1, config1);
  var ctx2 = document.getElementById('secAlertsChart').getContext('2d');
  window.myLine = new Chart(ctx2, config2);
  var ctx3 = document.getElementById('locationChart').getContext('2d');
  window.myHorizontalBar = new Chart(ctx3, config3);

}; */