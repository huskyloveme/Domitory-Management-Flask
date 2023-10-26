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
            'building': $("#building").val(),
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
    if (table_name == 'motorbikes') {
        data = {
            'msv': $("#msv").val(),
            'name': $("#name").val(),
            'license_plate': $("#license_plate").val(),
            'time_registration': $("#time_registration").val(),
            'status': $("#status").val(),
        };
    }
    if (table_name == 'visitors') {
        data = {
            'cccd': $("#cccd").val(),
            'name': $("#name").val(),
            'phone': $("#phone").val(),
            'gender': $("#gender").val(),
            'time_in': $("#time_in").val(),
            'time_out': $("#time_out").val(),
            'friend_of_msv': $("#friend_of_msv").val(),
        };
    }
    if (table_name == 'parking_histories') {
        data = {
            'license_plate': $("#license_plate").val(),
            'time_in': $("#time_in").val(),
            'time_out': $("#time_out").val(),
        };
    }
    if (table_name == 'services') {
        data = {
            'name': $("#name").val(),
            'price': $("#price").val(),
            'unit': $("#unit").val(),
            'description': $("#description").val(),
        };
    }
    if (table_name == 'student_service') {
        data = {
            'msv': $("#msv").val(),
            'service': $("#service").val(),
            'time_use': $("#time_use").val(),
            'time_end': $("#time_end").val(),
        };
    }
    // let table_name =
    $.ajax({
        url: "/" + table_name + "_add",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (res) {
            if (res.ok) {
                toastr.success(res.mesg);
                setTimeout(function () {
                    location.href = "/show_database_" + table_name;
                }, 1000);
            } else {
                toastr.error(res.mesg);
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}
