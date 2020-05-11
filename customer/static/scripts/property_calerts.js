$(document).ready(function() {
	// code goes here
	$(".js-calert-btn").click(function(e) {
		e.preventDefault();
		var thiz = $(this).closest('.card');
		var active = ((thiz.find(".custom-control-input").is(":checked"))?1:0);
		var risk_threshold = thiz.find(".risk_threshold").val();
		var calert_userid = thiz.find(".calert_userid").val();
		if (!risk_threshold) {
			toastr.error("Please select Risk Threshold");
		} else if (!calert_userid) {
			toastr.error("Please enter email");
		} else {
			var datasend = {};
			datasend['track'] = active;
			datasend['username'] = calert_userid;
			datasend['risk_threshold'] = risk_threshold;
			datasend['csrfmiddlewaretoken'] = CSRF;

			$.ajax({
				url: $("#form_url").val(),
				type: 'POST',
				dataType: 'json',
				data: datasend,
			})
			.done(function(res) {
				//console.log(res);
				if (res.status == "success") {
					toastr.success(res.message);
				} else {
					toastr.error(res.message);
				}
			});
		}
		
		return false;
	});
});