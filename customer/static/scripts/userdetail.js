/*var randomScalingFactor = function() {
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

var colorNames = Object.keys(window.chartColors);*/

$(document).ready(function() {
	var datasend = {};
	//datasend['key'] = API_KEY;
	//datasend['pid'] = PID;
	datasend['user'] = UID;
	//datasend['limit'] = 25;
	fetchUserStats(datasend);
});
function fetchUserStats (datasend) {
	fetchUserBasic(datasend);
	fetchUserLinked(datasend);
	fetchUserActivities(datasend);
	fetchUserLocations(datasend);
}
function fetchUserBasic (datasend) {
	delete datasend['limit'];
	var params = datasend;
	$.ajax({
		type: "GET",
		url: RF_API_URLs.bud,
		data: params,
		dataType: "json",
		success: function (response) {
			if(response.status == 'success') {
				setUserBasic(response.data);
			} else {
				toastr.error(response.message);
			}
		}
	});
}
function fetchUserLinked (datasend) {
	var params = datasend;
	params.limit = 12;
	$.ajax({
		type: "GET",
		url: RF_API_URLs.lus,
		data: params,
		dataType: "json",
		success: function (response) {
			if(response.status == 'success') {
				setUserLinked(response.data);
			} else {
				toastr.error(response.message);
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
		url: RF_API_URLs.rua,
		data: params,
		dataType: "json",
		success: function (response) {
			if(response.status == 'success') {
				setUserActivities(response.data);
			} else {
				toastr.error(response.message);
			}
		}
	});
}
function fetchUserLocations (datasend) {
	delete datasend['limit'];
	var params = datasend;
	$.ajax({
		type: "GET",
		url: RF_API_URLs.ulo,
		data: params,
		dataType: "json",
		success: function (response) {
			if(response.status == 'success') {
				setUserLocations(response.data);
			} else {
				toastr.error(response.message);
			}
		}
	});
}
function setUserBasic (data) {
	$("#userName").html(data.uid);
	if (data.rec_dt) {
		$("#lastActivity").html('Last Activity: '+timeSince(new Date(data.rec_dt)));
	}
	if (data.rec_loc) {
		$("#recLocation").html(data.rec_loc);
	}
	if (data.final_score) {
		$("#userRiskScore").html(Math.floor(data.final_score));
	}
	if (data.flag) {
		$("#userRiskScore").addClass('as-bg-'+RISK_TYPE[data.flag]);
	} else {
		$("#userRiskScore").addClass('as-bg-low');
	}
	if (data.obs == 'unsafe') {
		$("#accountStatus").html('<button class="btn btn-orange btn-icon">Compromised <span class="as-icon-wrap"><i class="as-icon as-icon-clock"></i></span></button>');
	} else {
		$("#accountStatus").html('<button class="btn btn-success btn-icon">Safe <span class="as-icon-wrap"><i class="as-icon as-icon-clock-green"></i></span></button>');
	}
}
function setUserLinked (data) {
	if (Object.keys(data).length>0) {
		$("#linkedUsers").html('<div class="owl-carousel owl-theme"></div>');
		for (var i = 0; i < Object.keys(data).length; i++) {
			if (i%6 == 0) {
				$("#linkedUsers .owl-theme").append('<div class="item"><div class="row">');
			}
			$("#linkedUsers .item:last-child .row:last-child").append(
				'<div class="col-md-6">'+
					'<span class="as-usr-2 mb-2">'+
						'<span class="as-usr-risk as-bg-'+RISK_TYPE[data[i].flag]+'">'+data[i].score+'</span>'+
						'<span class="as-usr-2-info">'+
							'<a href="javascript:;" class="as-usr-name">'+data[i].uid+'</a>'+
						'</span>'+
					'</span>'+
				'</div>');
			if (i%6 == 5 || i == Object.keys(data).length) {
				$("#linkedUsers .owl-theme").append('</div></div>');
			}
		}
		$('.owl-carousel').owlCarousel({
			loop:false,
			margin:0,
			nav:true,
			items:1,
			navContainer:'#luNavs',
			navText:['<a href="javascript:;" class="as-pg-nav"><i class="fa fa-angle-left" aria-hidden="true"></i></a>','<a href="javascript:;" class="as-pg-nav"><i class="fa fa-angle-right" aria-hidden="true"></i></a>'],
			navElement: 'span'
		});
	} else {
		$("#linkedUsers").html('<p>There are no linked users to this user.</p>');
	}
}
function setUserActivities (data) {
	if(Object.keys(data).length>0) {
		$("#userTimeline").html("");
		for (var i = 0; i < Object.keys(data).length; i++) {
			var firstKey = Object.keys(data)[i];
			var device = data[firstKey]['dvc'];
			var dos = data[firstKey]['os'];
			if (device == 'WebKit') {
				device = getWebkitDevice(dos);
			}
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
							'<div class="as-icon-wrap"><i class="fa fa-mobile"></i></div>'+device+
						'</li>'+
						'<li>'+
							'<div class="as-icon-wrap"><i class="fa fa-windows"></i></div>'+getOS(dos)+
						'</li>'+
						'<li>'+
							'<div class="as-icon-wrap"><i class="fa fa-wifi"></i></div>'+data[firstKey]['ip']+
						'</li>'+
					'</ul>'+
				'</div>'
			);
		}
	}
}
function setUserLocations (data) {
	//toastr.error(Object.keys(data).length);
	//console.log(events);
	if (data.length) {
		var locations = [];
		for (var i = 0; i < data.length; i++) {
			//console.log(events[i]);
			locations[i] = [];
			locations[i][0] = data[i].ci+', '+data[i].st+', '+data[i].co;
			locations[i][1] = data[i].la;
			locations[i][2] = data[i].lo;
			locations[i][3] = "Location score is "+data[i]['pd'].score+" and marked as "+data[i]['pd'].obs+".";
		}
		initializeMap(locations);
		//console.log(locations);
	} else {
		$("#map").html('<p>No known user locations yet.</p>').parent('.as-portlet-body').removeClass('p-0');
		//toastr.info("No locations");
	}
};
function initializeMap(locations) {

	var myOptions = {
		center: new google.maps.LatLng(21.146940, 79.089664),
		zoom: 5,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map"), myOptions);
	setMarkers(map,locations);
}

function setMarkers(map,locations){

	var marker, i
	var contentString = [];
	for (i = 0; i < locations.length; i++)
	{
		var title	= locations[i][0];
		var lat		= locations[i][1];
		var long	= locations[i][2];
		var desc	= locations[i][3];

		latlngset = new google.maps.LatLng(lat, long);

		var marker = new google.maps.Marker({  
		    map: map, title: title, position: latlngset  
		});
		//map.setCenter(marker.getPosition());
		map.setCenter(latlngset);


		//var content = "Loan Number: " + title + '</h3>' + "Address: " + desc;
		contentString[title] = '<div class="map-marker">'+
			'<h2 class="map-heading">' + title + '</h2>'+
			'<div class="map-content">'+ desc + '</div>'+
		'</div>';

		//console.log(content);

		var infowindow = new google.maps.InfoWindow()

		google.maps.event.addListener(marker, "click", (function(marker) {
			return function(evt) {
				//var content = marker.getTitle();
				var content = '<div class="map-marker">'+
					'<h2 class="map-heading">' + marker.getTitle() + '</h2>'+
				'</div>';
				/*console.log(marker);
				console.log(map);*/
				infowindow.setContent(contentString[marker.getTitle()]);
				infowindow.open(map, marker);
			}
		})(marker));
	}
}