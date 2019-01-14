$(function () {

    // user_center_site.html  主要处理表单提交前的校验
    var $formSub = $('#add_address');
    var $name = $('input[name="recipient_name"]');
    var $addr = $('textarea[name="recipient_addr"]');
    var $zipCode = $('input[name="zip_code"]');
    var $zipCodeError = $('#zip_code_error');
    var $phoneId = $('input[name="recipient_phone"]');
    var $phoneIdError = $('#phone_id_error');
    // 当这四个变量均为true时方可提交表单
    var flag_name,flag_addr,flag_code,flag_phone;
    flag_name=flag_addr=flagcod=flag_phone = false;

    $name.blur(function() {
        if($name.val().length>0){
            flag_name = true;
        }
    })
    $addr.blur(function(){
        if($addr.val().length>0){
            flag_addr = true;
        }
    })
    $zipCode.blur(function() {
        var value = $zipCode.val();
        var re = /^\d{6}$/;
        if(!re.test(value)){
            $zipCodeError.show();
        }else{
            flag_code = true;
        }
    });
    $zipCode.focus(function() {
        $zipCodeError.hide();
    });

    $phoneId.blur(function() {
        var value = $phoneId.val();
        var re = /^\d{11}$/;
        if(!re.test(value)){
            $phoneIdError.show();
        }else{
            flag_phone = true;
        }
    });
    $phoneId.focus(function() {
        $phoneIdError.hide();
    });

    $formSub.submit(function() {
        if(flag_name==true&&flag_phone==true&&flag_code==true&&flag_addr==true){
            return true;
        }else{
            return false;
        }
    })


    // user_center_site.html 主要用于动态获取用户的地址填充到select标签
    var $select = $('select[name = select_addr]');
    // var $current_addr = $('.site_con').find('dd');
    $select.change(function() {
        var index = $(this).children('option:selected').index() - 1;
        // if(int(index)<0){
        //     return ;
        // }
        $.get('/user/changedefaultaddr/?index='+index, function(data){
            if(data.res == 1){
                location.href = '/user/address/';
                // $current_addr.html(value);
            }
        })
    })


})
