$(function () {
    $('#login_form').submit(function () {
        var $name = $('.name_input');
        var $pwd = $('.pass_input');
        var $rember = $('#remberaccount');
        var status = null;
        $name.focus(function () {
            $('.pwd_error').hide();
        });
        $pwd.focus(function () {
            $('.pwd_error').hide();
        });
        /*$.ajax({
            // get请求不安全
            async:false,
            type:'GET',
            url:'/user/checkloginstatus/?username='+$name.val()+'&password='+$pwd.val(),
            dataType:'json',
            success:function (data) {
                if(data.res == 1){
                    status = 1;
                }else{
                    $('.pwd_error').show();
                    status =0;
                }
            },
            error:function () {
                alert('request error');
            }
        });*/
        var key = "csrfmiddlewaretoken";
        var csrf = $('input[name = "csrfmiddlewaretoken"]').val();
        param = {'username': $name.val(),'password': $pwd.val(),
            'rember': $rember.is(':checked'),"csrfmiddlewaretoken":csrf};
       /* $.post('/user/checkloginstatus/',param,function (data) {
            // 无法指定同步（等待执行）
            if(data.res == 1){
                    status = 1;
                }else{
                    $('.pwd_error').show();
                    status =0;
                }
        });*/
       $.ajax({
           'async': false,
           'type': 'POST',
           'url': '/user/checkloginstatus/',
           'data':param,
           'success':function (data) {
               if(data.res == 1){
                    status = 1;
                }else{
                    $('.pwd_error').show();
                    status =0;
                }
           }
       });

        if(status == 1){
            return true;
        }else{
            return false;
        }

    })


});