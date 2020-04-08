var randomScalingFactor = function() {
	return Math.round(Math.random() * 100);
};

var color = Chart.helpers.color;
var config = {
	type: 'radar',
	data: {
		labels: ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight'],
		datasets: [{
			label: 'My First dataset',
			backgroundColor: color(window.chartColors.red).alpha(0.2).rgbString(),
			borderColor: window.chartColors.red,
			pointBackgroundColor: window.chartColors.red,
			data: [
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor()
			]
		}, {
			label: 'My Second dataset',
			backgroundColor: color(window.chartColors.blue).alpha(0.2).rgbString(),
			borderColor: window.chartColors.blue,
			pointBackgroundColor: window.chartColors.blue,
			data: [
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor()
			]
		}]
	},
	options: {
		legend: {
			position: 'top',
		},
		title: {
			display: false,
			text: 'Chart.js Radar Chart'
		},
		scale: {
			ticks: {
				beginAtZero: true
			}
		}
	}
};

window.onload = function() {
	window.myRadar = new Chart(document.getElementById('canvas'), config);
};

var colorNames = Object.keys(window.chartColors);

$(document).ready(function() {
	var datasend = {};
	datasend['key'] = API_KEY;
	datasend['pid'] = PID;
	datasend['user'] = UID;
	datasend['limit'] = 25;
	fetchUserStats(datasend);
});
function fetchUserStats (datasend) {
	fetchUserBasic(datasend);
	fetchUserActivities(datasend);
	fetchUserLocations(datasend);
}
function fetchUserBasic (datasend) {
	delete datasend['limit'];
	var params = datasend;
	$.ajax({
		type: "GET",
		url: ML_SERVER_API+RF_API_URLs.bud,
		data: params,
		dataType: "json",
		success: function (response) {
			if(response.status == 'success') {
				setUserBasic(response.data);
			} else {
				alert(response.message);
			}
		}
	});
}
function fetchUserActivities (datasend) {
	//delete datasend['limit'];
	var params = datasend;
	params.limit = 25;
	$.ajax({
		type: "GET",
		url: ML_SERVER_API+RF_API_URLs.rua,
		data: params,
		dataType: "json",
		success: function (response) {
			if(response.status == 'success') {
				setUserActivities(response.data);
			} else {
				alert(response.message);
			}
		}
	});
}
function fetchUserLocations (datasend) {
	delete datasend['limit'];
	var params = datasend;
	$.ajax({
		type: "GET",
		url: ML_SERVER_API+RF_API_URLs.ulo,
		data: params,
		dataType: "json",
		success: function (response) {
			if(response.status == 'success') {
				setUserLocations(response.data);
			} else {
				alert(response.message);
			}
		}
	});
}
function setUserBasic (data) {
	$("#userName").html(data.user);
	if (data.rec_dt) {
		$("#lastActivity").html('Last Activity: '+timeSince(new Date(data.rec_dt)));
	}
	if (data.rec_loc) {
		$("#recLocation").html(data.rec_loc);
	}
	$("#userRiskScore").html(Math.floor(data.final_score)).addClass('as-bg-'+RISK_TYPE[data.flag]);
}
function setUserActivities (data) {
	if(Object.keys(data).length>0) {
		$("#userTimeline").html("");
		for (var i = 0; i < Object.keys(data).length; i++) {
      		var firstKey = Object.keys(data)[i];
			$("#userTimeline").append(
				'<div class="as-activity-item as-activity-'+data[firstKey]['obs']+'">'+
					'<div class="as-activity-line"></div>'+
					'<h4 class="as-activity-title">'+getLongDatePipe(new Date(data[firstKey]['datetime']))+'</h4>'+
					'<ul class="as-activity-meta">'+
						'<li>'+
							'<div class="as-icon-wrap"><i class="fa fa-map-marker"></i></div>'+data[firstKey]['loc']+
						'</li>'+
						/*'<li>'+
							'<div class="as-icon-wrap"><i class="as-icon as-icon-isp"></i></div>127.0.0.1 Gazon Communication ISP, '+
						'</li>'+*/
						'<li>'+
							'<div class="as-icon-wrap"><i class="fa fa-mobile"></i></div>'+data[firstKey]['dvc']+
						'</li>'+
						'<li>'+
							'<div class="as-icon-wrap"><i class="fa fa-windows"></i></div>'+getOS(data[firstKey]['os'])+
						'</li>'+
						/*'<li>'+
							'<div class="as-icon-wrap"><i class="fa fa-wifi"></i></div>Sample text'+                      
						'</li>'+*/
					'</ul>'+
				'</div>'
			);
		}
	}
}
function setUserLocations (data) {
	alert(Object.keys(data).length);
}