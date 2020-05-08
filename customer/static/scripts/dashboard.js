function fetchAllStats (datasend) {
  var duration = $("#duration").val();
  if (!duration) {
    toastr.error("Please select a duration");
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
var tableHRU,tableSA;
$(document).ready(function () {
  var datasend = {};
  //datasend['key'] = API_KEY;
  //datasend['pid'] = PID;
  fetchAllStats(datasend);
  $("#duration").change(function(event) {
    $(".js-duration").val($(this).val());
    /* Act on the event */
    fetchAllStats(datasend);
  });
  $(".js-duration").change(function(event) {
    var dataType = $(this).data('type');
    var duration = getFilterDateRange($(this).val());
    switch (dataType) {
      case 'hru':
        fetchHRU(datasend,duration);
        break;
      case 'sa':
        fetchSA(datasend,duration);
        break;
      case 'la':
        fetchLA(datasend,duration);
        break;
      case 'ura':
        fetchSAA(datasend,duration);
        break;
      case 'rrd':
        fetchRRD(datasend,duration);
        break;
      default:
        // statements_def
        break;
    }
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
    url: RF_API_URLs.ds,
    data: paramsDS,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setStatsDS(response);
      } else {
        toastr.error(response.message);
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
    url: RF_API_URLs.hru,
    data: paramsHRU,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setTableHru(response.users_scores,response.user_url);
      } else {
        toastr.error(response.message);
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
    url: RF_API_URLs.sa,
    data: paramsSA,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setTableSA(response.usr_scr_cat_det,response.user_url);
      } else {
        toastr.error(response.message);
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
    url: RF_API_URLs.la,
    data: paramsLA,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        if (window.myLine1) {
          window.myLine1.destroy();
        }
        var config1 = setConfigLA(response);
        var ctx1 = document.getElementById('attemptsChart').getContext('2d');
        window.myLine1 = new Chart(ctx1, config1);
      } else {
        toastr.error(response.message);
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
    url: RF_API_URLs.ura,
    data: paramsSAA,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        if (window.myLine2) {
          window.myLine2.destroy();
        }
        var config2 = setConfigSAA(response);
        var ctx2 = document.getElementById('secAlertsChart').getContext('2d');
        window.myLine2 = new Chart(ctx2, config2);
      } else {
        toastr.error(response.message);
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
    url: RF_API_URLs.rrd,
    data: paramsRRD,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        if (window.myHorizontalBar) {
          window.myHorizontalBar.destroy();
        }
        var config3 = setConfigRRD(response.data);
        var ctx3 = document.getElementById('locationChart').getContext('2d');
        window.myHorizontalBar = new Chart(ctx3, config3);
      } else {
        toastr.error(response.message);
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
function setTableHru(data,user_url) {
  //toastr.error(data.length);
  $("#tblHRU tbody").html("");
  if(data.length>0) {
    for (let i = 0; i < data.length; i++) {
      $("#tblHRU tbody").append(
        '<tr>'+
            '<td><div class="as-tbl-risk-cover"><i class="as-risk-bubble as-bg-'+RISK_TYPE[data[i].cat]+'"></i> '+capitalize(RISK_TYPE[data[i].cat])+'</div></td>'+
            //'<td><i class="as-icon as-icon-risk-graph"></i></td>'+
            '<td>'+data[i].user+'</td>'+
            '<td><div class="as-btn-risk-score as-bg-light-'+RISK_TYPE[data[i].cat]+' as-border-'+RISK_TYPE[data[i].cat]+' as-text-'+RISK_TYPE[data[i].cat]+'">'+Math.floor(data[i].score)+'</div></td>'+
            '<td><a href="'+user_url+data[i].user+'/'+'" class="as-tbl-v"><i class="fa fa-eye"></i></a></td>'+
          '</tr>'
      );
    }
    if ( $.fn.dataTable.isDataTable( '#tblHRU' ) ) {
      tableHRU.destroy();
    }
    tableHRU = $('#tblHRU').DataTable( {
        "scrollY":        "300px",
        "scrollCollapse": true,
        "paging":         false,
        "searching": false,
        "bInfo" : false,
        aoColumnDefs: [
            { "aTargets": [ 0 ], "bSortable": true },
            { "aTargets": [ 1 ], "bSortable": true },
            { "aTargets": [ 2 ], "bSortable": true },
            { "aTargets": [ 3 ], "bSortable": false }
        ]
    } );
  } else {
    $("#tblHRU tbody").append('<tr><td colspan="5" class="as-lh-30">No Users</td></tr>');
  }
}
function setTableSA(data,user_url) {
  //toastr.error(data.length);
  $("#tblSA tbody").html("");
  if(data.length>0) {
    for (let i = 0; i < data.length; i++) {
      $("#tblSA tbody").append(
        '<tr>'+
            '<td><div class="as-tbl-risk-cover"><i class="as-risk-bubble as-bg-'+RISK_TYPE[data[i].cat]+'"></i> '+capitalize(RISK_TYPE[data[i].cat])+'</div></td>'+
            '<td>'+((data[i].det==null)?'Behavioral Threat':data[i].det)+'</td>'+
            '<td>'+data[i].user+'</td>'+
            '<td><div class="as-btn-risk-score as-bg-light-'+RISK_TYPE[data[i].cat]+' as-border-'+RISK_TYPE[data[i].cat]+' as-text-'+RISK_TYPE[data[i].cat]+'">'+Math.floor(data[i].score)+'</div></td>'+
            '<td><a href="'+user_url+data[i].user+'/'+'" class="as-tbl-v"><i class="fa fa-eye"></i></a></td>'+
          '</tr>'
      );
    }
    if ( $.fn.dataTable.isDataTable( '#tblSA' ) ) {
      tableSA.destroy();
    }
    tableSA = $('#tblSA').DataTable( {
        "scrollY":        "300px",
        "scrollCollapse": true,
        "paging":         false,
        "searching": false,
        "bInfo" : false,
        aoColumnDefs: [
            { "aTargets": [ 0 ], "bSortable": true },
            { "aTargets": [ 1 ], "bSortable": true },
            { "aTargets": [ 2 ], "bSortable": true },
            { "aTargets": [ 3 ], "bSortable": true },
            { "aTargets": [ 4 ], "bSortable": false }
        ]
    } );
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