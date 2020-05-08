var randomDataTen = function() {
  var data = [];
  for (var i = 0; i < 10; i++) {
    data[i] = Math.floor((Math.random() * 100) + 1);
  }
  return data;
};
var setUsersMap = function(data,max) {
  var ctx = document.getElementById('chartContainer').getContext('2d');

  ctx.canvas.width  = document.getElementById('chart1').clientWidth;

  var distance_from_x = 50;
  var distance_from_y = 20;

  var canvas_width = ctx.canvas.width-distance_from_x;
  var canvas_height = ctx.canvas.height-distance_from_y;

  x1 = (canvas_height-distance_from_y)/3;
  y1 = (canvas_width+distance_from_x-20)/3;

  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#DB3736";
  ctx.moveTo(distance_from_x, 0);
  ctx.lineTo(distance_from_x, x1);
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#F29D49";
  ctx.moveTo(distance_from_x, x1);
  ctx.lineTo(distance_from_x, x1*2);
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#65BD6E";
  ctx.moveTo(distance_from_x, x1*2);
  ctx.lineTo(distance_from_x, x1*3);
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#65BD6E";
  ctx.moveTo(distance_from_x, canvas_height-distance_from_y);
  ctx.lineTo(y1, canvas_height-distance_from_y);
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#F29D49";
  ctx.moveTo(y1, canvas_height-distance_from_y);
  ctx.lineTo(y1*2, canvas_height-distance_from_y);
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#DB3736";
  ctx.moveTo(y1*2, canvas_height-distance_from_y);
  ctx.lineTo(y1*3, canvas_height-distance_from_y);
  ctx.stroke();

  // Draw X axis
  var grid_x = canvas_width/11;
  ctx.font = "13px Roboto";
  ctx.fillStyle = "#B0BAC9";
  ctx.fillText("0", distance_from_x, canvas_height-distance_from_y+15);
  for (var i = 1; i <= 10; i++) {
    ctx.font = "13px Roboto";
    ctx.fillStyle = "#B0BAC9";
    //console.log((grid_x*i));
    ctx.fillText(i*10, (grid_x*i)+distance_from_x, canvas_height-distance_from_y+15);
    //ctx.fillText("TEXT", X POS, Y POS, maxWidth{optional);
  }

  // Draw Y axis
  var grid_y = canvas_height/11;
  ctx.font = "13px Roboto";
  ctx.fillStyle = "#B0BAC9";
  ctx.fillText("0", 38, canvas_height-distance_from_y);
  var currX;
  max = getM10(max);
  var xStep = parseInt(max/10);
  for (var i = 1; i <= 10; i++) {
    currX = getCX(i*xStep);//30;
    ctx.font = "13px Roboto";
    ctx.fillStyle = "#B0BAC9";
    /*if(i==10) {
      currX = 25;
    }*/
    ctx.fillText(i*xStep, currX, canvas_height-distance_from_y-(grid_y*i));
    //ctx.fillText("TEXT", X POS, Y POS, maxWidth{optional);
  }

  ctx.textAlign="center";
  ctx.textBaseline="middle";
  ctx.translate(15,150);
  ctx.rotate(-Math.PI/2);
  ctx.font="16px Roboto";
  ctx.fillStyle = "#B0BAC9";
  ctx.fillText("User count",0,0);

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.textAlign="center";
  ctx.textBaseline="middle";
  //ctx.translate(15,150);
  //ctx.rotate(Math.PI/2);
  ctx.font="16px Roboto";
  ctx.fillStyle = "#B0BAC9";
  ctx.fillText("Risk Score",Math.floor((canvas_width)/2)+distance_from_y,canvas_height-distance_from_y+30);
  /*var datasetx = [];
  for (var i = 0; i < 10; i++) {
    datasetx = [10,20,30,40,50,60,70,80,90,100];
  }
  var datasety = [];
  for (var i = 0; i < 10; i++) {
    datasety[i] = randomDataTen();
  }
  for (var i = 0; i < datasety.length; i++) {
    for (var j = 0; j < datasety[i].length; j++) {
      ctx.beginPath();
      ctx.arc(Math.floor(((datasetx[i]/10)*grid_x)+distance_from_x), canvas_height-distance_from_y-((datasety[i][j]/10)*grid_y), 5, 0, 2 * Math.PI);
      ctx.fillStyle = "rgba(36, 108, 242, 0.76)";
      ctx.fill();
    }
  }*/
  //var userScores = [0,85,10,50,60,26,25,35,43,57];
  var dataset = [];
  var i=0;
  /*for (var i = 0; i < 100; i++) {
    dataset[i] = randomScalingFactor();
  }*/
  Object.keys(data).forEach(function (item) {
    dataset[i++] = {'x':parseInt(item),'y':parseInt(data[item])}; // value
  });
  //console.log(dataset);
  for (var i = 0; i < dataset.length; i++) {
    //console.log(dataset[i]);
    ctx.beginPath();
    ctx.arc(Math.floor(((dataset[i].x/10)*grid_x)+distance_from_x), canvas_height-distance_from_y-((dataset[i].y/xStep)*grid_y), 5, 0, 2 * Math.PI);
    ctx.fillStyle = "rgba(36, 108, 242, 0.76)";
    ctx.fill();
  }
}

var randomScalingFactor = function() {
  return {x:Math.floor((Math.random() * 100) + 1),y:Math.floor((Math.random() * 100) + 1)};
};
function fetchUserStats (datasend) {
  var duration = $("#duration").val();
  if (!duration) {
    toastr.error("Please select a duration");
  } else {
    var duration = getFilterDateRange(duration);
    fetchUsersMap(datasend,duration);
    fetchUsersList(datasend,duration);
  }
}
$(document).ready(function() {
  var datasend = {};
  //datasend['pid'] = PID;
  //datasend['dur'] = getFilterDateRange('filter-365');
  //datasend['limit'] = 25;
  fetchUserStats(datasend);
  $(".js-duration").change(function(event) {
    $(".js-duration").val($(this).val());
    /* Act on the event */
    fetchUserStats(datasend);
  });
});
function fetchUsersMap(datasend,duration) {
  delete datasend['limit'];
  var params = datasend;
  params.dur = duration;
  $.ajax({
    type: "GET",
    url: RF_API_URLs.rm,
    data: params,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setUsersMap(response.data,response.max);
      } else {
        toastr.error(response.message);
      }
    }
  });
}
function fetchUsersList(datasend,duration) {
  var params = datasend;
  params.dur = duration;
  params.limit = 25;
  $.ajax({
    type: "GET",
    url: RF_API_URLs.ul,
    data: params,
    dataType: "json",
    success: function (response) {
      if(response.status == 'success') {
        setUsersList(response.data);
      } else {
        toastr.error(response.message);
      }
    }
  });
}
function setUsersList (data) {
  if(Object.keys(data).length>0) {
    var showUsers = parseInt($(".js-show-users").text());
    $(".js-show-users").text(showUsers+Object.keys(data).length);
    $(".js-total-users").text(showUsers+Object.keys(data).length);
    $("#tblUsers tbody").html("");
    //console.log(Object.keys(data).length);
    for (let i = 0; i < Object.keys(data).length; i++) {
      var firstKey = Object.keys(data)[i];
      var device = Object.keys(data[firstKey]['dvc'])[0];
      var dos = Object.keys(data[firstKey]['os'])[0];
      if (device == 'WebKit') {
        device = getWebkitDevice(dos);
      }
      //console.log(data[firstKey]);
      $("#tblUsers tbody").append(
        '<tr>'+
            '<td>'+
              '<div class="as-bor-risk as-border-'+RISK_TYPE[data[firstKey]['rec_flag']]+'">'+
                '<div class="as-tbl-2-td">'+
                  '<div class="as-tbl-2-tc as-tbl-li-usr">'+
                    '<span class="as-usr-1">'+
                      '<span class="as-usr-risk as-bg-'+RISK_TYPE[data[firstKey]['rec_flag']]+'">'+data[firstKey]['rec_score']+'</span>'+
                      '<span class="as-usr-1-info">'+
                        '<a href="'+window.location.href+Object.keys(data)[i]+'" class="as-usr-name">'+$.trim(Object.keys(data)[i])+'</a>'+
                        '<span class="as-list-rslerts-wrap">'+
                          '<ul class="as-list-rslerts">'+
                            '<li><a href="javascript:;" title="'+device+'"><i class="as-icon as-icon-windows"></i></a></li>'+
                            '<li><a href="javascript:;" title="'+data[firstKey]['locn']+'"><i class="as-icon as-icon-loc"></i></a></li>'+
                            '<li><a href="javascript:;" title="'+getOS(dos)+'"><i class="as-icon as-icon-mobile"></i></a></li>'+
                            '<li><a href="javascript:;" title="'+data[firstKey]['rec_ip']+'"><i class="as-icon as-icon-wifi"></i></a></li>'+
                          '</ul>'+
                        '</span>'+
                      '</span>'+
                    '</span>'+
                  '</div>'+
                '</div>'+
              '</div>'+
            '</td>'+
            '<td><div class="as-tbl-2-td"><div class="as-tbl-2-tc light-text-1">'+timeSince(new Date(data[firstKey]['rec_time']))+'</div></div></td>'+
            '<td>'+
              '<div class="as-tbl-2-td">'+
                '<div class="as-tbl-2-tc">'+
                  '<div class="as-ato-status" title="'+textCapitalize(data[firstKey]['obs'])+'">'+
                    '<div class="as-ato-icon"><i class="as-icon as-icon-'+data[firstKey]['obs']+'"></i></div>'+
                    '<div class="as-ato-c">'+
                      '<div class="as-ato-t">'+data[firstKey]['rec_threat']+'</div>'+
                      '<div class="light-text-1">'+getLongDatePipe(new Date(data[firstKey]['rec_time']))+'</div>'+
                    '</div>'+
                  '</div>'+
                '</div>'+
              '</div>'+
            '</td>'+
          '</tr>'
      );
    }    
    $('#tblUsers').DataTable({
      aaSorting: [[0, 'asc']],
      bPaginate: false,
      bFilter: false,
      bInfo: false,
      bSortable: true,
      bRetrieve: true,
      aoColumnDefs: [
          { "aTargets": [ 0 ], "bSortable": true },
          { "aTargets": [ 1 ], "bSortable": true },
          { "aTargets": [ 2 ], "bSortable": true },
          //{ "aTargets": [ 3 ], "bSortable": false }
      ]
    });
  }
}
function getM10 (mv) {
  var sb10 = String(mv).substr(-1);
  if (sb10 == '0') {
    return parseInt(mv);
  }
  sb10 = 10-parseInt(sb10);
  return parseInt(mv)+sb10;
}
function getCX (tx) {
  var ltx = tx.toString().length;
  if (ltx == 1) {
    return 38;
  } else if (ltx == 2) {
    return 30;
  } else {
    return 25;
  }
}