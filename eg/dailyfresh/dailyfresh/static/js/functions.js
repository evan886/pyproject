$(function () {
    var $after_login = $('.login_info');
    var $before_login = $('.login_btn');
    /*$.get('/user/loginstatus/',function (data) {
        if(data.res == 1){
            $before_login.hide();
            $after_login.show();
            alert('complete 1');
        }else{
            $before_login.show();
            $after_login.hide();
            alert('complete 0');
        }
    });
    // 由于前端能够直接拿到后台返回的request所以就不必用ajax去后台
    // 验证session里是否留有用户登录信息了
    */

    var $quit_login = $('#quitlogin');
    $quit_login.click(function () {
        $.get('/user/quitlogin/',function (data) {
            if(data.res == 1){
                $before_login.show();
                $after_login.hide();
            }else{
                alert('quit login failure');
            }
        })
    });

});
