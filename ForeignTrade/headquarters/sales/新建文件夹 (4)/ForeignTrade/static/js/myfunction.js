//将如2008-01-01格式的时间转换为1970-01-01到此时间过去的秒数
function dateToNum(date) {
   var strDate=date.replace(/-/g,'/');
   var num = parseInt(Date.parse(strDate)/1000);
   return num
}

//将1970-01-01到现在的13位毫秒数或者10位秒数转换为2008-01-01的时间
function numToDate(dateNum){
    dateNum=parseInt(dateNum);
    var strDateNum = String(dateNum);
    if(strDateNum.length==13){dateNum=dateNum}
    else if(strDateNum.length==10){dateNum=dateNum*1000}
    var date = new Date(dateNum);
    var year = date.getFullYear();
    var month = date.getMonth()+1;
    if(month<10){month = '0'+month}
    var day = date.getDate();
    if(day<10){day = '0'+ day}
    return year+'-'+month+'-'+day
}

//天数转换成秒数
function dayToSec(day) {
    return parseInt(day)*24*60*60*1000
}



//bootstrap.pagination 翻页函数（）
function classPagination(page,page_group,now_page,now_page_group,url,id) {

    if(page<=5){
        var content = '<li><a href="#">&laquo;</a></li>\n' ;
        for(var i=1;i<=page;i++){
           content += '<li><a hidden=false href="'+url+'?page='+i+'" id="page'+i+'">'+i+'</a></li>'
        }
        content += '<li><a href="#">&raquo;</a></li>';
        $('#'+id).append(content);
        for(var i=now_page_group*5-4;i<=now_page_group*5;i++){
                $('#page'+i).prop('hidden',false);
            }
            $('#page'+now_page).css('color','white').css('background-color','black');
    }
    else{
        var content = '<li><a href="#" id="previous_page_group">&laquo;</a></li>\n' ;
        for(var i=1;i<=page;i++){

              content += '<li><a hidden="hidden" href="'+url+'?page='+i+'" id="page'+i+'">'+i+'</a></li>'

        }
        content += '<li><a href="#" id="next_page_group">&raquo;</a></li>\n';
        $('#'+id).append(content);
        for(var i=now_page_group*5-4;i<=now_page_group*5;i++){
                $('#page'+i).prop('hidden',false);
            }
            $('#page'+now_page).css('color','white').css('background-color','black');
}




    $('#previous_page_group').click(function () {
        if (now_page_group == 1) {
            return false
        }
        else{
            for(var i=now_page_group*5-4;i<=now_page_group*5;i++){
                $('#page'+i).prop('hidden',true);
            }
            now_page_group -=1;

            for(var i=now_page_group*5-4;i<=now_page_group*5;i++){
                $('#page'+i).prop('hidden',false)
            }
        }

    });
    $('#next_page_group').click(function () {
        if (now_page_group == page_group) {
            return false
        }
        else{
            for(var i=now_page_group*5-4;i<=now_page_group*5;i++){

                $('#page'+i).prop('hidden',true);
            }
            now_page_group +=1;
            for(var i=now_page_group*5-4;i<=now_page_group*5;i++){
                $('#page'+i).prop('hidden',false)
            }
        }

    });
}


//表单遍历提交函数，formId,返回data_dict
function form_submit(formId) {
    let t = $(formId).serializeArray();
    let data_dict = {};
    $.each(t,function () {
        data_dict[this.name] = this.value
    });
    return data_dict
}



//
