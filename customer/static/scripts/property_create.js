$(document).ready(function () {
    $("#frmAddProperty").submit(function (e) { 
        e.preventDefault();
        var pn = $("#inputPropertyName").val();
        if(!pn) {
            toastr.error("Please enter property name");
        } else {
            var datasend = {};
            datasend['pn'] = pn;
            datasend['csrfmiddlewaretoken'] = CSRF;
            $.ajax({
                type: "POST",
                //url: "{{form_url}}", //BASE_URL,
                data: datasend,
                dataType: "json",
                success: function (res) {
                    if(res.status == 'success') {
                        window.location = res.red_url;
                    } else {
                        toastr.error(res.message);
                    }
                }
            });
        }
        return false;
    });
});