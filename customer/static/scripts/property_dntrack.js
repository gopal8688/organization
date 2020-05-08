$(document).ready(function() {
	// code goes here
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
						toastr.success(res.items);
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
						toastr.success(res.items);
					} else {
						toastr.error(res.message);
					}
				}
			});
		}
		return false;
	});
});