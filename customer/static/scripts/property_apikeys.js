$(document).ready(function () {
    fetchAPIKeyLogs();
    $("#btnSecret").click(function (e) { 
        e.preventDefault();
        var datasend = {};
        datasend['csrfmiddlewaretoken'] = CSRF;
        $.ajax({
            type: "POST",
            url: $("#frmUpdatePlatformURL").attr('action'), //BASE_URL,
            data: datasend,
            dataType: "json",
            success: function (res) {
                if(res.status == 'success') {
                    $('#inputPropertySecret').attr('type', 'text').val(res.psecret);
                    if (res.log) {
                        var gen_time = new Date(res.log.gen_time);
                        $("#tblLogs tbody tr:first-child").before(
                            '<tr>'+
                                '<td>'+res.log.gen_by+'</td>'+
                                '<td>'+res.log.role+'</td>'+
                                '<td>'+getLongDate(gen_time)+'</td>'+
                            '</tr>'
                        );
                    }
                } else {
                    toastr.error(res.message);
                }
            }
        });
        return false;
    });
});
function fetchAPIKeyLogs() {
    var datasend = {};
    datasend['csrfmiddlewaretoken'] = CSRF;
    $('#tblLogs tbody').html('');
    $.ajax({
        url: $("#api_url_logs").val(),
        type: 'GET',
        dataType: 'json',
        data: datasend,
    })
    .done(function(res) {
        if(res.status == 'success') {
            var logs = res.logs;
            for (var i in logs) {
                //console.log(log);
                var gen_time = new Date(logs[i].gen_time);
                $('#tblLogs tbody').append(
                    '<tr>'+
                        '<td>'+logs[i].gen_by+'</td>'+
                        '<td>'+logs[i].role+'</td>'+
                        '<td>'+getLongDate(gen_time)+'</td>'+
                    '</tr>'
                );
            }
        } else {
            toastr.error(res.message);
        }
    });    
}