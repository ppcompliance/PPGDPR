(function () {
    function checkip() {
    var appUrl = $('#AppUrl').val()
    // var end_time_water = $('#exampleInputEmail2').val()
    if (appUrl=="" || appUrl=="undefined"){
        alert('请输入APP URL')
        return false;
    }
    else if(!IsUrl(appUrl)){
        alert('输入正确 APP URL');
        return false;
    }
    else {
        return true;
    }
    return false;
}
function IsUrl(str) {
    var Expression=/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
    var isUrl =Expression.test(str);
    return isUrl;

}


   function showWaiting() {
        $("#btn").enable = false;
        document.body.style.cursor = "wait";  // 沙漏 (等待)
    }

    function closeWaiting() {
        $("#btn").enable = true;
        document.body.style.cursor = "default";  // 箭头 (默认)
    }
   function checkip() {
       var data={};
       var url = $("#AppUrl").val();
       console.log(url);
       data['url'] = url;
       showWaiting();
       var senddata = JSON.stringify(data);
       $.ajax({
           url:"submit",
           type:"POST",
           data:senddata,
           dataType:"json",
           success:function (text_result) {
           },
           error:function (text_result) {
           }
       });


   }
})();