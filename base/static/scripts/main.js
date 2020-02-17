'use strict';

window.chartColors = {
	critical: 'rgb(168, 0, 0)',
	high: 'rgb(255, 67, 67)',
	medium: 'rgb(255, 159, 56)',
	low: 'rgb(89, 233, 142)',
	info: 'rgb(184, 195, 206)',
	gold: 'rgb(255, 231, 0)',
	blue: 'rgb(36, 108, 242)',
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	//blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

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