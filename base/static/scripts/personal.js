$(document).ready(function() {
	$("#frmProfilePersonal").submit(function(event) {
		/* Act on the event */
		var first_name = $("#first_name").val();
		var last_name = $("#last_name").val();
		var sex = $("#sex").val();
		var email = $("#cemail").val();
		var phone = $("#cphone").val();
		if (!first_name) {
			toastr.error("Please enter first name!");
		} else if (!last_name) {
			toastr.error("Please enter last name!");
		} else if (!sex) {
			toastr.error("Please select gender!");
		} else if (!email) {
			toastr.error("Please enter email!");
		} else {
			$.ajax({
				url: $("#frmProfilePersonal").attr('action'),
				type: 'POST',
				dataType: 'json',
				data: $("#frmProfilePersonal").serialize(),
			})
			.done(function(res) {
				if (res.status == "success") {
					toastr.success("Successfully Updated!");
				} else {
					toastr.error(res.message);
				}
			})
			.fail(function() {
				console.log("error");
			});
			
		}
		return false;
	});
	$("#frmProfilePassword").submit(function(event) {
		/* Act on the event */
		var password = $("#password").val();
		var cpassword = $("#cpassword").val();
		if (!password) {
			toastr.error("Please enter password!");
		} else if (password != cpassword) {
			toastr.error("Both passwords do not match!");
		} else {
			$.ajax({
				url: $("#frmProfilePassword").attr('action'),
				type: 'POST',
				dataType: 'json',
				data: $("#frmProfilePassword").serialize(),
			})
			.done(function(res) {
				if (res.status == "success") {
					toastr.success("Successfully Updated!");
				} else {
					toastr.error(res.message);
				}
			})
			.fail(function() {
				console.log("error");
			});
			
		}
		return false;
	});
	$("#frmProfileCompany").submit(function(event) {
		/* Act on the event */
		var org_name = $("#org_name").val();
		var brand_url = $("#brand_url").val();
		var brand_name = $("#brand_name").val();
		var brand_logo = $("#brand_logo").val();
		if (!org_name) {
			toastr.error("Please enter company name!");
		} else {
			var options = { 
				target:        '#output2',   // target element(s) to be updated with server response 
				beforeSubmit:  showRequest,  // pre-submit callback 
				success:       showResponse,  // post-submit callback
				type:      'POST',
				dataType: 'json',
				timeout:   10000 
		    };
			$(this).ajaxSubmit(options);
			/*$.ajax({
				url: $("#frmProfileCompany").attr('action'),
				type: 'POST',
				dataType: 'json',
				data: $("#frmProfileCompany").serialize(),
			})
			.done(function(res) {
				if (res.status == "success") {
					alert("Successfully Updated!");
				} else {
					alert(res.message);
				}
			})
			.fail(function() {
				console.log("error");
			});*/
			
		}
		return false;
	});
}); 
// pre-submit callback 
function showRequest(formData, jqForm, options) {
    var queryString = $.param(formData);
    return true; 
} 
// post-submit callback 
function showResponse(responseText, statusText, xhr, $form)  {
    if (responseText.status == "success") {
		toastr.success("Successfully Updated!");
	} else {
		toastr.error(responseText.message);
	}
} 