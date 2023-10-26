// init
setTimeout(() => {
    // init select2
    $('#selectHashtags').select2();

}, 0);

// function
function SentQuery() {
    let data = {
            'query': $("#query").val(),
        };
    $.ajax({
        url: "/free_query",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (res) {
            if (!res.ok) {
                toastr.error(res.mesg);
            } else {
                $("#query_result").html(res.data);
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}
