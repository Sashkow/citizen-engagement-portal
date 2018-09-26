console.log('running tester')

function make_notification() {
    var r = new XMLHttpRequest();
    r.open("GET", '/test_make/', true);
    r.send();
}

function mark_all_as_read() {
    var r = new XMLHttpRequest();
    r.open("GET", '/mark_all_as_read/', true);
    r.send();

    data = {}
    console.log('notnotnot')
    var url = '/notifications/'
    $.ajax({
     url: url,
     type :'GET',
     data:data,
     cache:true,
     success: function(data){
         console.log('OK');
            $(".dynamic-block").empty()
            $(".dynamic-block").html(data.html)
         },
     error: function(){
        console.log('error')
     }
     })



}


