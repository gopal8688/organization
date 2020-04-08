function fetchAllStats (datasend) {
  var duration = $("#duration").val();
  if (!duration) {
    alert("Please select a duration");
  } else {
    var duration = getFilterDateRange(duration);
    fetchDS(datasend,duration);
    fetchHRU(datasend,duration);
    fetchSA(datasend,duration);
    fetchLA(datasend,duration);
    fetchSAA(datasend,duration);
    fetchRRD(datasend,duration);
  }
}
$(document).ready(function () {
  var datasend = {};
  datasend['key'] = API_KEY;
  datasend['pid'] = PID;
  fetchAllStats(datasend);
  $(".js-duration").change(function(event) {
    $(".js-duration").val($(this).val());
    /* Act on the event */
    fetchAllStats(datasend);
  });
});
var randomScalingFactor = function() {
  return Math.floor((Math.random() * 100000) + 1);
};
var randomScalingFactorPer = function() {
  return Math.round(Math.random() * 100);
};
function fetchDS(datasend,duration) {
  delete datasend.limit;
  var paramsDS = datasend;
  paramsDS.dur = duration;
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.ds,
    data: paramsDS,
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
function fetchHRU(datasend,duration) {
  delete datasend.limit;
  var paramsHRU = datasend;
  paramsHRU.dur = duration;
  paramsHRU.limit = 8;
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.hru,
    data: paramsHRU,
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
function fetchSA(datasend,duration) {
  delete datasend.limit;
  var paramsSA = datasend;
  paramsSA.dur = duration;
  paramsSA.limit = 8;
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.sa,
    data: paramsSA,
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
function fetchLA(datasend,duration) {
  delete datasend.limit;
  var paramsLA = datasend;
  paramsLA.dur = duration;
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.la,
    data: paramsLA,
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
function fetchSAA(datasend,duration) {
  delete datasend.limit;
  var paramsSAA = datasend;
  paramsSAA.dur = duration;
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.saa,
    data: paramsSAA,
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
function fetchRRD(datasend,duration) {
  delete datasend.limit;
  var paramsRRD = datasend;
  paramsRRD.dur = duration;
  $.ajax({
    type: "GET",
    url: ML_SERVER_API+RF_API_URLs.rrd,
    data: paramsRRD,
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
            '<td><i class="as-risk-bubble as-bg-'+RISK_TYPE[data[i].cat]+'"></i> '+capitalize(RISK_TYPE[data[i].cat])+'</td>'+
            '<td><i class="as-icon as-icon-risk-graph"></i></td>'+
            '<td>'+data[i].user+'</td>'+
            '<td><div class="as-btn-risk-score as-bg-light-critical as-border-critical as-text-critical">'+Math.floor(data[i].score)+'</div></td>'+
            '<td><a href="javascript:;" class="as-tbl-v"><i class="fa fa-eye"></i></a></td>'+
          '</tr>'
      );
    }
  } else {
    $("#tblHRU tbody").append('<tr><td colspan="5" class="as-lh-30">No Users</td></tr>');
  }
}
function setTableSA(data) {
  //alert(data.length);
  if(data.length>0) {
    $("#tblSA tbody").html("");
    for (let i = 0; i < data.length; i++) {
      $("#tblSA tbody").append(
        '<tr>'+
            '<td><i class="as-risk-bubble as-bg-'+RISK_TYPE[data[i].cat]+'"></i> '+capitalize(RISK_TYPE[data[i].cat])+'</td>'+
            '<td>'+((data[i].det==null)?'Behavioral Threat':data[i].det)+'</td>'+
            '<td>'+data[i].user+'</td>'+
            '<td><div class="as-btn-risk-score as-bg-light-'+RISK_TYPE[data[i].cat]+' as-border-'+RISK_TYPE[data[i].cat]+' as-text-'+RISK_TYPE[data[i].cat]+'">'+Math.floor(data[i].score)+'</div></td>'+
            '<td><a href="javascript:;" class="as-tbl-v"><i class="fa fa-eye"></i></a></td>'+
          '</tr>'
      );
    }
  } else {
    $("#tblSA tbody").append('<tr><td colspan="5" class="as-lh-30">No Alerts</td></tr>');
  }
}
function setConfigLA(data) {
  var maxVal = 0;
  var maxVal = getMaxVal(maxVal,data.f_count);
  var maxVal = getMaxVal(maxVal,data.s_count);
  maxVal = getMaxStepRange(maxVal,30);
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
          },
        }],
        yAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Attempts'
          },
          ticks: {
            min: 0,
            max: maxVal,
  
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
function setConfigSAA(data) {
  var maxVal = 0;
  var maxVal = getMaxVal(maxVal,data.g_count);
  var maxVal = getMaxVal(maxVal,data.y_count);
  var maxVal = getMaxVal(maxVal,data.r_count);
  maxVal = getMaxStepRange(maxVal,5);
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
            max: maxVal,

            // forces step size to be 5 units
            stepSize: 5
          }
        }]
      }
    }
  };
}

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
      maintainAspectRatio: false,
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