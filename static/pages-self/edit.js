// init
setTimeout(() => {
    // init select2
    $('#selectHashtags').select2();

}, 0);

// function
function SaveToData(table_name) {
    let data;
    if (table_name == 'students') {
        data = {
            'room': $("#room").val(),
            'msv': $("#msv").val(),
            'name': $("#name").val(),
            'address': $("#address").val(),
            'phone': $("#phone").val(),
            'gender': $("#gender").val(),
            'birthday': $("#birthday").val(),
            'day_in': $("#day_in").val(),
            'day_out': $("#day_out").val(),
            'status': $("#status").val(),
        };
    }
    if (table_name == 'rooms') {
        data = {
            'building_id': $("#building_id").val(),
            'name': $("#name").val(),
            'accommodate': $("#accommodate").val(),
            'type': $("#type").val(),
            'capacity': $("#capacity").val(),
            'price': $("#price").val(),
            'status': $("#status").val(),
        };
    }
    if (table_name == 'buildings') {
        data = {
            'name': $("#name").val(),
            'address': $("#address").val(),
        };
    }
    let url = window.location.pathname
    let id = url.split('_').pop()
    $.ajax({
        url: "/" + table_name + "_edit_" + id,
        type: "POST",
        data: data,
        dataType: "json",
        success: function (res) {
            if (res.ok) {
                toastr.success(res.mesg);
                setTimeout(function () {
                    location.href = "/show_database_" + table_name;
                }, 3000);
            } else {
                toastr.error(res.mesg);
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}
