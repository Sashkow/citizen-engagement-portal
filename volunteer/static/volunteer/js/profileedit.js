$( document ).ready(function() {
    $('.btn-send').click(function(){
        data = {}
        fname = $("input[name='fname']").val()
        lname = $("input[name='lname']").val()
        data.fname = fname
        data.lname = lname
        $("input[type='checkbox']").each(function(index){
            type_id = $(this).attr('type_id')
            data[String(type_id)] = $(this).is(':checked')
        })
        var url = $('.adding-info').attr('post_url')
        var csrf_token = $('input[name = "csrfmiddlewaretoken"]').val();
        data['csrfmiddlewaretoken'] = csrf_token;
        console.log(data)
        $.ajax({
             url: url,
             type :'POST',
             data:data,
             cache:true,
             success: function(data){
                console.log('OK')

             },
             error: function(){
                console.log('error')
             }
         })

    })
})