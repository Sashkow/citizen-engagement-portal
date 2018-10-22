$( document ).ready(function() {

    $(document).on('click', '.change-league', function(){
        var data = {}
        data.id = $(this).attr('legaues_id')
        var url = $(this).attr('get_url')
//        $(this).prop('disabled', true);
        console.log($(this))

        $.ajax({
             url: url,
             type :'GET',
             data:data,
             cache:true,
             success: function(data){
                console.log('OK')
                $('.dynamic-block').empty()
                $(".dynamic-block").html(data.html);
//                $('.change-league:disabled').prop('disabled', false);
             },
             error: function(){
                console.log('error')
             }
         })
    });

    $(document).on('click', '.buy-achieve', function(){
        data = {}
        var csrf_token = $('input[name = "csrfmiddlewaretoken"]').val();
        var url = $(this).attr('post_url');
        var id_achieve = $(this).attr('achieve_id');
        data['csrfmiddlewaretoken'] = csrf_token;
        data.id = id_achieve;


        $.ajax({
             url: url,
             type :'POST',
             data:data,
             cache:true,
             success: function(data){
                console.log('OK')
                console.log(typeof(data))
                var new_data = data[0]
                console.log(new_data)
                if( 'error' in new_data){
                    $('#error-buying').modal()
                    $('p.error-currency').text(new_data.error)
                    $('img.error-currency').attr('src', new_data.url_currency)
                    }else if('success' in new_data){
                        var needed_object = $('.ach-container[achieve_id = '+ id_achieve +' ]')
                        needed_object.empty();
                        needed_object.append(new_data.html);
                        if('new_league' in new_data){
                            console.log(new_data)
                            $('#new-league').modal()
                            $('.new-league').text(new_data.new_league)
                        }
                 }

             },
             error: function(){
                console.log('error')
             }
         })

    })

})