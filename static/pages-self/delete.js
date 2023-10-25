// init
setTimeout(() => {
    // init select2
    $('#selectHashtags').select2();

}, 0);

// function
function DeleteToData(id, table_name) {
    $.ajax({
        url: "/" + table_name + "_delete_" + id,
        type: "POST",
        // data: data,
        // dataType: "json",
        success: function (res) {
            if (res.ok) {
                toastr.success(res.mesg);
                setTimeout(function () {
                    location.href = "/show_database_" + table_name;
                }, 2000);
            } else {
                toastr.error(res.mesg);
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}
