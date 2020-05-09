$(document).ready(function() {
	// code goes here
	getDoNotTrackIPs();
	getDoNotTrackEmails();
	$("#formIP").submit(function(e) {
		/* Act on the event */
		e.preventDefault();
		var dnt_ip = $("#dnt_ip").val();
		if(!dnt_ip) {
			toastr.error("Please enter IP Address");
		}
		else {
			var datasend = {};
			datasend['dnt_ip'] = dnt_ip;
			datasend['csrfmiddlewaretoken'] = CSRF;
			$.ajax({
				type: "POST",
				url: $("#formIP").attr('action'), //BASE_URL,
				data: datasend,
				dataType: "json",
				success: function (res) {	
					if(res.status == 'success') {
						toastr.success(res.message);
						$("#listIPs").append(
							'<div class="col-xlg-4 col-lg-6 js-list-item-ip">'+
								'<div class="p-3 as-mb-20p bg-light text-dark as-sel-tag">'+res.data.ip+' <a href="javascript:;" class="as-icon-status as-icon-status-off js-delete-ip" data-ip="'+res.data.id+'"><i class="fa fa-times"></i></a></div>'+
							'</div>'
						);
					} else {
						toastr.error(res.message);
					}
				}
			});
		}
		return false;
	});
	$("#formEmail").submit(function(e) {
		/* Act on the event */
		e.preventDefault();
		var dnt_email = $("#dnt_email").val();
		if(!dnt_email) {
			toastr.error("Please enter IP Address");
		}
		else {
			var datasend = {};
			datasend['dnt_email'] = dnt_email;
			datasend['csrfmiddlewaretoken'] = CSRF;
			$.ajax({
				type: "POST",
				url: $("#formEmail").attr('action'), //BASE_URL,
				data: datasend,
				dataType: "json",
				success: function (res) {
					if(res.status == 'success') {
						toastr.success(res.message);
						$("#listEmails").append(
							'<div class="col-xlg-4 col-lg-6 js-list-item-email">'+
								'<div class="p-3 as-mb-20p bg-light text-dark as-sel-tag">'+res.data.email+' <a href="javascript:;" class="as-icon-status as-icon-status-off js-delete-email" data-email="'+res.data.id+'"><i class="fa fa-times"></i></a></div>'+
							'</div>'
						);
					} else {
						toastr.error(res.message);
					}
				}
			});
		}
		return false;
	});
	$("#listIPs").on('click', '.js-delete-ip', function(event) {
		event.preventDefault();
		/* Act on the event */
		var ip = $(this).data('ip');
		var thiz = $(this);
		if (!ip) {
			toastr.error('There is some error, please refresh and try again.');
		} else {
			var url = replaceLastPartOfURL($("#formIP").attr('action'),ip);
			$.ajax({
				url: url,
				type: 'DELETE',
				dataType: 'json',
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", CSRF);
				},
			})
			.done(function(res) {
				if(res.status == 'success') {
					toastr.success(res.message);
					thiz.closest('.js-list-item-ip').remove();
				} else {
					toastr.error(res.message);
				}
			});
			
		}
	});
	$("#listEmails").on('click', '.js-delete-email', function(event) {
		event.preventDefault();
		/* Act on the event */
		var email = $(this).data('email');
		var thiz = $(this);
		if (!email) {
			toastr.error('There is some error, please refresh and try again.');
		} else {
			var url = replaceLastPartOfURL($("#formEmail").attr('action'),email);
			$.ajax({
				url: url,
				type: 'DELETE',
				dataType: 'json',
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", CSRF);
				},
			})
			.done(function(res) {
				if(res.status == 'success') {
					toastr.success(res.message);
					thiz.closest('.js-list-item-email').remove();
				} else {
					toastr.error(res.message);
				}
			});
			
		}
	});
});
function getDoNotTrackIPs () {
	// body...
	$.ajax({
		url: $("#formIP").attr('action'),
		type: 'GET',
		dataType: 'json'
	})
	.done(function(res) {
		if(res.status == 'success') {
			var logs = res.logs;
			$("#listIPs").html("");
			for (var i = 0; i < logs.length; i++) {
				$("#listIPs").append(
					'<div class="col-xlg-4 col-lg-6 js-list-item-ip">'+
						'<div class="p-3 as-mb-20p bg-light text-dark as-sel-tag">'+logs[i].ip+' <a href="javascript:;" class="as-icon-status as-icon-status-off js-delete-ip" data-ip="'+logs[i].id+'"><i class="fa fa-times"></i></a></div>'+
					'</div>'
				);
			}
		} else {
			toastr.error(res.message);
		}
	});
}
function getDoNotTrackEmails () {
	// body...
	$.ajax({
		url: $("#formEmail").attr('action'),
		type: 'GET',
		dataType: 'json'
	})
	.done(function(res) {
		if(res.status == 'success') {
			var logs = res.logs;
			$("#listEmails").html("");
			for (var i = 0; i < logs.length; i++) {
				$("#listEmails").append(
					'<div class="col-xlg-4 col-lg-6 js-list-item-email">'+
						'<div class="p-3 as-mb-20p bg-light text-dark as-sel-tag">'+logs[i].email+' <a href="javascript:;" class="as-icon-status as-icon-status-off js-delete-email" data-email="'+logs[i].id+'"><i class="fa fa-times"></i></a></div>'+
					'</div>'
				);
			}
		} else {
			toastr.error(res.message);
		}
	});
}