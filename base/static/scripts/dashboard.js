$(document).ready(function () {
  var datasend = {};
  datasend['key'] = API_KEY;
  datasend['pid'] = PID;
  fetchDS(datasend);
  fetchHRU(datasend);
  fetchSA(datasend);
  fetchLA(datasend);
  fetchSAA(datasend);
  fetchRRD(datasend);
});
var randomScalingFactor = function() {
  return Math.floor((Math.random() * 100000) + 1);
};
var randomScalingFactorPer = function() {
  return Math.round(Math.random() * 100);
};
function fetchDS(datasend) {  
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.ds,
    data: datasend,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setStatsDS(response);
      } else {
        alert(response.message);
      }
    }
  });
}
function fetchHRU(datasend) {  
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.hru,
    data: datasend,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setTableHru(response.users_scores);
      } else {
        alert(response.message);
      }
    }
  });
}
function fetchSA(datasend) {  
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.sa,
    data: datasend,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setTableSA(response.usr_scr_cat_det);
      } else {
        alert(response.message);
      }
    }
  });
}
function fetchLA(datasend) {  
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.la,
    data: datasend,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        var config1 = setConfigLA(response);
        var ctx1 = document.getElementById('attemptsChart').getContext('2d');
        window.myLine = new Chart(ctx1, config1);
      } else {
        alert(response.message);
      }
    }
  });
}
function fetchSAA(datasend) {  
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.saa,
    data: datasend,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        var config2 = setConfigSAA(response);
        var ctx2 = document.getElementById('secAlertsChart').getContext('2d');
        window.myLine = new Chart(ctx2, config2);
      } else {
        alert(response.message);
      }
    }
  });
}
function fetchRRD(datasend) {  
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.rrd,
    data: datasend,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        var config3 = setConfigRRD(response);
        var ctx3 = document.getElementById('locationChart').getContext('2d');
        window.myHorizontalBar = new Chart(ctx3, config3);
      } else {
        alert(response.message);
      }
    }
  });
}
function setStatsDS(data) {
  $("#monVisitors").text(data.monitored_users);
  $("#authUsers").text(data.authenticated_users);
  $("#hrUsers").text(data.high_risk_users);
  $("#notEvents").text(data.notable_events);
  $("#susDevices").text(data.suspicious_device);
  $("#watchUsers").text(data.watchlist);
}
function setTableHru(data) {
  //alert(data.length);
  if(data.length>0) {
    $("#tblHRU tbody").html("");
    for (let i = 0; i < data.length; i++) {
      $("#tblHRU tbody").append(
        '<tr>'+
            '<td><i class="as-risk-bubble as-bg-high"></i> High</td>'+
            '<td><i class="as-icon as-icon-risk-graph"></i></td>'+
            '<td>'+data[i].user+'</td>'+
            '<td><div class="as-btn-risk-score as-bg-light-critical as-border-critical as-text-critical">'+data[i].score+'</div></td>'+
            '<td><a href="javascript:;" class="as-tbl-v"><i class="fa fa-eye"></i></a></td>'+
          '</tr>'
      );
    }
  } else {
    $("#tblHRU tbody").append('<tr><td colspan="5" class="as-lh-30">No Users</td></tr>');
  }
  $("#tblHRU tbody").append(
    '<tr>'+
        '<td colspan="5">'+
          '<div class="as-grid-justified as-tfoot-tools">'+
            '<div class="as-tfoot-filter">'+
              '<select name="" id="" class="form-control">'+
                '<option value="">Last 7 days</option>'+
                '<option value="">Last 30 days</option>'+
                '<option value="">Last Year</option>'+
              '</select>'+
            '</div>'+
            '<div class="">'+
              '<a href="javascript:;" class="as-tbl-v-all"><span class="as-as">View All</span> <i class="as-icon-chevron-right"></i></a>'+
            '</div>'+
          '</div>'+
        '</td>'+
      '</tr>'
  );
}
function setTableSA(data) {
  //alert(data.length);
  if(data.length>0) {
    $("#tblSA tbody").html("");
    for (let i = 0; i < data.length; i++) {
      $("#tblSA tbody").append(
        '<tr>'+
            '<td>'+RISK_TYPE[data[0].cat]+'</td>'+
            '<td>Credential Stuffing</td>'+
            '<td>'+data[0].user+'</td>'+
            '<td><div class="as-btn-risk-score as-bg-light-high as-border-high as-text-high">'+data[0].score+'</div></td>'+
            '<td><a href="javascript:;" class="as-tbl-v"><i class="fa fa-eye"></i></a></td>'+
          '</tr>'
      );
    }
  } else {
    $("#tblSA tbody").append('<tr><td colspan="5" class="as-lh-30">No Alerts</td></tr>');
  }
  $("#tblSA tbody").append(
    '<tr>'+
        '<td colspan="5">'+
          '<div class="as-grid-justified as-tfoot-tools">'+
            '<div class="as-tfoot-filter">'+
              '<select name="" id="" class="form-control">'+
                '<option value="">Last 7 days</option>'+
                '<option value="">Last 30 days</option>'+
                '<option value="">Last Year</option>'+
              '</select>'+
            '</div>'+
            '<div class="">'+
              '<a href="javascript:;" class="as-tbl-v-all"><span class="as-as">View All</span> <i class="as-icon-chevron-right"></i></a>'+
            '</div>'+
          '</div>'+
        '</td>'+
      '</tr>'
  );
}
function setConfigLA(data) {
  return {
    type: 'line',
    data: {
      labels: data.date,
      datasets: [{
        label: 'Successful Logins',
        backgroundColor: window.chartColors.low,
        borderColor: window.chartColors.low,
        data: data.f_count,
        fill: false,
      }, {
        label: 'Failed Logins',
        fill: false,
        backgroundColor: window.chartColors.high,
        borderColor: window.chartColors.high,
        data: data.s_count,
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
            max: 150,
  
            // forces step size to be 5 units
            stepSize: 30
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
}
/* var config1 = {
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
}; */
function setConfigSAA(data) {
  return {
    type: 'line',
    data: {
      labels: data.date,
      datasets: [{
        label: 'Safe Users',
        backgroundColor: window.chartColors.low,
        borderColor: window.chartColors.low,
        data: data.g_count,
        fill: false,
      }, {
        label: 'Suspicious Users',
        fill: false,
        backgroundColor: window.chartColors.gold,
        borderColor: window.chartColors.gold,
        data: data.y_count,
      }, {
        label: 'High Risk Users',
        fill: false,
        backgroundColor: window.chartColors.high,
        borderColor: window.chartColors.high,
        data: data.r_count,
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
            max: 25,

            // forces step size to be 5 units
            stepSize: 5
          }
        }]
      }
    }
  };
}

/*var config2 = {
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
};*/

function setConfigRRD(data) {
  return {
    type: 'horizontalBar',
    data: {
      labels: data.country,
      datasets: [{
        label: 'Good Users',
        backgroundColor: window.chartColors.blue,
        borderColor: window.chartColors.blue,
        borderWidth: 1,
        data: data.good_users
      }, {
        label: 'Bad Users',
        backgroundColor: window.chartColors.high,
        borderColor: window.chartColors.high,
        data: data.bad_users
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
}
/*var config3 = {
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
};*/

/*window.onload = function() {
  var ctx1 = document.getElementById('attemptsChart').getContext('2d');
  window.myLine = new Chart(ctx1, config1);
  var ctx2 = document.getElementById('secAlertsChart').getContext('2d');
  window.myLine = new Chart(ctx2, config2);
  /*var ctx3 = document.getElementById('locationChart').getContext('2d');
  window.myHorizontalBar = new Chart(ctx3, config3);
};*/