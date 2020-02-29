$(document).ready(function () {
    $("#frmUpdatePlatformURL").submit(function (e) { 
        e.preventDefault();
        var pu = $("#inputPropertyURL").val();
        if(!pu) {
            alert("Please enter property name");
        } else {
            var datasend = {};
            datasend['pu'] = pu;
            datasend['csrfmiddlewaretoken'] = CSRF;
            $.ajax({
                type: "POST",
                url: $("#frmUpdatePlatformURL").attr('action'), //BASE_URL,
                data: datasend,
                dataType: "json",
                success: function (res) {
                    if(res.status == 'success') {
                        alert(res.message);
                    } else {
                        alert(res.message);
                    }
                }
            });
        }
        return false;
    });
});