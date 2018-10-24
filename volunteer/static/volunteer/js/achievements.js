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
                if( 'error' in data){
                    $('#error-buying').modal()
                    $('p.error-currency').text(data.error)
                    $('img.error-currency').attr('src', data.url_currency)
                    }else if('success' in data){
                        var needed_object = $('.ach-container[achieve_id = '+ id_achieve +' ]')
                        needed_object.empty();
                        needed_object.append(data.html);
                        if('new_league' in data){
                            console.log(data)
                            console.log(data.all_info.background_color)

                            var b_image = "url(" + data.all_info.background_image + ")"
                            var curr_bord = data.all_info.color_current_border

                            $('#sidebar').css({"background-color": data.all_info.background_color , "background-image" : b_image })

                            var b_image = data.all_info.background_image

                            $("head").append('<style type="text/css"></style>');
                            var newStyleElement = $("head").children(':last');
                            newStyleElement.html('.current-menu-item{border-left: 1.3vh solid '+ data.all_info.color_current_border +';}');
                            newStyleElement.append('.current-menu-item{background-image: linear-gradient( 120deg, '+ data.all_info.color_current_grad1 +', ' + data.all_info.color_current_grad2 + ', ' +data.all_info.color_current_grad1 +');}');
                            newStyleElement.append('p.ribbon{ color: '+ data.all_info.color_league_txt +';}');
                            newStyleElement.append('.volunteer-name{ color: '+ data.all_info.color_volunteer_name +';}');
                            newStyleElement.append('.curr_quat{ color: '+ data.all_info.color_menu_item +';}');
                            newStyleElement.append('div.current-menu-item p.item-menu{ '+ data.all_info.color_current_text +'!important;}');
                            newStyleElement.append(' .photo-user{ width:'+ data.all_info.img_user_width +';}');
                            newStyleElement.append(' .photo-user{ right:'+ data.all_info.img_user_height +';}');
                            newStyleElement.append(' .photo-user{ height:'+ data.all_info.img_user_height_corr +';}');
                            newStyleElement.append('.notif-col{ color:'+ data.all_info.color_not_text +';}');
                            newStyleElement.append('.item-menu{ color:'+ data.all_info.color_menu_item +';}');

                            $('p.ribbon').text(data.new_league)
                            $('.league-logo').attr('src', data.all_info.league_image)
                            $('.photo-frame').attr('src', data.all_info.user_frame)

                            $('#new-league').modal()
                            $('.new-league').text(data.new_league)
                        }
                 }

             },
             error: function(){
                console.log('error')
             }
         })

    })

})