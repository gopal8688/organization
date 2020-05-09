'use strict';
toastr.options = {
    "closeButton": true,
    "debug": false,
    "positionClass": "toast-top-center",
    "onclick": null,
    "showDuration": "1000",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}
window.chartColors = {
	critical: 'rgb(168, 0, 0)',
	high: 'rgb(255, 67, 67)',
	medium: 'rgb(255, 159, 56)',
	low: 'rgb(89, 233, 142)',
	info: 'rgb(184, 195, 206)',
	gold: 'rgb(255, 231, 0)',
	blue: 'rgb(36, 108, 242)',
	t_blue: 'rgba(36, 108, 242, 0.9)',
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	//blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

window.MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Aug","Sep","Oct","Nov","Dec"];

window.RISK_TYPE = {
	'C': 'critical',
	'R': 'high',
	'Y': 'medium',
	'G': 'low'
}
window.RISK_TYPE_LABEL = {
	'C': '<i class="as-risk-bubble as-bg-critical"></i> Critical',
	'R': '<i class="as-risk-bubble as-bg-high"></i> High',
	'Y': '<i class="as-risk-bubble as-bg-medium"></i> Medium',
	'G': '<i class="as-risk-bubble as-bg-low"></i> Low'
}
window.capitalize = function(str) {
	return str.charAt(0).toUpperCase() + str.substr(1).toLowerCase();
}
window.roundTwoDigits = function(str) {
	return ("0" + str).slice(-2);
}
window.getLongDate = function(timestamp) {
	return MONTHS[timestamp.getMonth()]+' '+roundTwoDigits(timestamp.getDate())+', '+timestamp.getFullYear()+' '+roundTwoDigits(timestamp.getHours())+':'+roundTwoDigits(timestamp.getMinutes())+':'+roundTwoDigits(timestamp.getSeconds());
}
window.getLongDatePipe = function(timestamp) {
	return MONTHS[timestamp.getMonth()]+' '+roundTwoDigits(timestamp.getDate())+', '+timestamp.getFullYear()+' | '+roundTwoDigits(timestamp.getHours())+':'+roundTwoDigits(timestamp.getMinutes());
}
$(document).click(function (event) {
	var clickover = $(event.target);
	var _opened = $(".as-aside.collapse").hasClass("as-aside collapse show");
	if (_opened === true && !clickover.hasClass("navbar-toggler")) {
		$("button.navbar-toggler").click();
	}
});
$(document).mouseup(function(e) {
	var container = $(".as-header");
	// if the target of the click isn't the container nor a descendant of the container
	if (!container.is(e.target) && container.has(e.target).length === 0) 
	{
		$('#navbarProperty').collapse('hide');
		$('#navbarSearch').collapse('hide');
	}
});
$(document).ready(function() {
	$("#btnMiniToggler").click(function(event) {
		/* Act on the event */
		if ($("body").hasClass('as-aside-min')) {
		$("body").removeClass('as-aside-min');
		} else {
		$("body").addClass('as-aside-min');
		}
	});
	$('#navbarSearch').on('show.bs.collapse', function () {
		$('#navbarProperty').collapse('hide');
	});
	$('#navbarProperty').on('show.bs.collapse', function () {
		$('#navbarSearch').collapse('hide');
	});
});
function getDateByDays (datefrom,days) {
	return new Date(datefrom.getTime() - (days * 24 * 60 * 60 * 1000));
}
function getDateString (objDate) {
	return fixTwoDigits(objDate.getDate())+'-'+fixTwoDigits(objDate.getMonth()+1)+'-'+objDate.getFullYear();
}
function fixTwoDigits (dstring) {
	if (dstring<10)
		return '0'+dstring;
	return dstring;
}
var getDataUrl = function (img) {
  var canvas = document.createElement('canvas')
  var ctx = canvas.getContext('2d')

  canvas.width = img.width
  canvas.height = img.height
  ctx.drawImage(img, 0, 0)

  // If the image is not png, the format
  // must be specified here
  return canvas.toDataURL()
}
function getFilterDateRange (duration) {
  var today = new Date();
  switch (duration) {
    case 'filter-7':
      var last = getDateByDays(today,7);
      var fromdate = getDateString(last);
      var todate = getDateString(today);
      return fromdate+':'+todate;
      break;
    case 'filter-30':
      var last = getDateByDays(today,30);
      var fromdate = getDateString(last);
      var todate = getDateString(today);
      return fromdate+':'+todate;
      break;
    case 'filter-365':
      var last = getDateByDays(today,365);
      var fromdate = getDateString(last);
      var todate = getDateString(today);
      return fromdate+':'+todate;
      break;
    default:
      // statements_def
      break;
  }
}
function getOS ($os) {	
	switch ($os) {
		case 'win':
			$os = 'Windows';
			break;

		case 'wnt':
			$os = 'Windows NT';
			break;

		case 'osx':
			$os = 'OS X';
			break;

		case 'deb':
			$os = 'Debian';
			break;

		case 'ubt':
			$os = 'Ubuntu';
			break;

		case 'mac':
			$os = 'Macintosh';
			break;

		case 'bsd':
			$os = 'OpenBSD';
			break;

		case 'lnx':
			$os = 'Linux';
			break;

		case 'crm':
			$os = 'ChromeOS';
			break;
		
		// Mobile OS's

		case 'ard':
			$os = 'AndroidOS';
			break;

		case 'bb':
			$os = 'BlackBerryOS';
			break;

		case 'pal':
			$os = 'PalmOS';
			break;

		case 'sym':
			$os = 'SymbianOS';
			break;

		case 'wim':
			$os = 'WindowsMobileOS';
			break;

		case 'ios':
			$os = 'iOS';
			break;

		case 'meg':
			$os = 'MeeGoOS';
			break;

		case 'mmo':
			$os = 'MaemoOS';
			break;

		case 'jos':
			$os = 'JavaOS';
			break;

		case 'wos':
			$os = 'webOS';
			break;

		case 'bdo':
			$os = 'badaOS';
			break;

		case 'brw':
			$os = 'BREWOS';
			break;

		default:
			$os = "Unknown";
			break;
	}
	return $os;
}
window.getWebkitDevice = function(os) {
	var pc = ['win','wnt','osx','deb','ubt','mac','bsd','lnx','crm'];
	var mobile = ['ard','bb','pal','sym','wim','ios','meg','mmo','jos','wos','bdo','brw'];
	if ($.inArray(os, pc) != -1) {
		return 'PC';
	}
	if ($.inArray(os, mobile) != -1) {
		return 'Mobile';
	}
	return os;
}
function timeSince(date) {

  var seconds = Math.floor((new Date() - date) / 1000);

  var interval = Math.floor(seconds / 31536000);

  if (interval > 1) {
    return interval + " years ago";
  }
  interval = Math.floor(seconds / 2592000);
  if (interval > 1) {
    return interval + " months ago";
  }
  interval = Math.floor(seconds / 86400);
  if (interval > 1) {
    return interval + " days ago";
  }
  interval = Math.floor(seconds / 3600);
  if (interval > 1) {
    return interval + " hours ago";
  }
  interval = Math.floor(seconds / 60);
  if (interval > 1) {
    return interval + " minutes ago";
  }
  return Math.floor(seconds) + " seconds ago";
}
window.getMaxVal = function(maxVal,maxData) {
	//var maxVal = 0;
	for (var i = 0; i < maxData.length; i++) {
		if (maxData[i]>maxVal) {
			maxVal = maxData[i];
		}
	}
	return maxVal;
}
window.getMaxStepRange = function(maxNum,stepSize) {
	var m5 = maxNum%stepSize;
	return (maxNum+stepSize-m5);
}
window.textCapitalize = function(str) {
	return str.substr(0,1).toUpperCase()+str.substr(1);
}
window.replaceLastPartOfURL = function(surl,rstr) {
	surl = surl.split("/");
	surl[surl.length - 1] = rstr;
	surl = surl.join("/");
	return surl;
}