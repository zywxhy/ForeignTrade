var zTreeNodeid = '';
function zTreeOnClick(event,treeId,treeNode) {
    $("#goods_table").empty();
    page=1;
    $("#page").empty();
    $("#page").append('第'+page+'页');
    url={% url 'goods_type_page' %};
    zTreeNodeid =treeNode.id;
    var content='<table class=\'table table-striped table-bordered table-hover table-condensed\'><tr><td>产品id</td><td>产品名称</td><td>产品规格</td></tr>';
    $.getJSON({% url 'goods_get' %},{'id':treeNode.id,'pid':treeNode.pId,},function(data,status){
        $.each(data,function(i,item){
            content += '<tr><td>'+item.fields.goods_id+'</td>'+'<td>'+item.fields.name+'</td>'+'<td>'+item.fields.specifications+'</td></tr>';
        });
           content += '</table>';
          $("#goods_table").html(content);
    });
    $.getJSON({% url 'goods_type_return_page' %},{'id':treeNode.id,'pid':treeNode.pId,},function(data,status){
         page_max =data.page;
         $("#goods_count").empty();
         $("#goods_count").append('共有'+data.page+'页，产品'+data.count+'个');


    });


}

var setting={
    data:{
      simpleData:{
          enable:true,
      },
    },
    callback:{
        //beforeClick:zTreeBeforeClick,
        onClick:zTreeOnClick,
    },
};
var zTreeNode=[
    {% for g in goodsType %}
        { name:'{{ g.type_name }}', id:'{{ g.type_id }}',pId:'{{ g.type_pid }}', isParent:'{{ g.is_parent }}' },
    {% endfor %}
];

$(document).ready(function(){
    $.fn.zTree.init($("#goodsTree"),setting,zTreeNode);
});
</script>
<script>

//页码信息
var page=1;
var url ={% url 'goods_page' %};
var page_max = {{ page }};



$("#page").append('第'+page+'页');
//前一页展示前一页内容，如果首页的话，会弹窗提示。
$('#previous_page').click(function () {
    if(page==1){ alert('第一页')}
    else{page-=1;
    $("#goods_table").empty();
    var content='<table class=\'table table-striped table-bordered table-hover table-condensed\'><tr><td>产品id</td><td>产品名称</td><td>产品规格</td></tr>';
    $.getJSON(url,{'page':page,'zTreeNodeid':zTreeNodeid},function(data,status){
        $.each(data,function(i,item){
            content += '<tr><td>'+item.fields.goods_id+'</td>'+'<td>'+item.fields.name+'</td>'+'<td>'+item.fields.specifications+'</td></tr>';
        });
           content += '</table>';
          $("#goods_table").html(content);
    });
     $("#page").empty();
    $("#page").append('第'+page+'页');}
});
//后一页展示后一页内容，如果尾页的话，会弹窗提示。
$('#next_page').click(function () {
    if(page==page_max){ alert('最后一页') }
    else{page+=1;
    $("#goods_table").empty();
    var content='<table class=\'table table-striped table-bordered table-hover table-condensed\'><tr><td>产品id</td><td>产品名称</td><td>产品规格</td></tr>';
    $.getJSON(url,{'page':page,'zTreeNodeid':zTreeNodeid},function(data,status){
        $.each(data,function(i,item){
            content += '<tr><td>'+item.fields.goods_id+'</td>'+'<td>'+item.fields.name+'</td>'+'<td>'+item.fields.specifications+'</td></tr>';
        });
           content += '</table>';
          $("#goods_table").html(content);
    });
    $("#page").empty();
    $("#page").append('第'+page+'页');}
});
//跳页
    $('#to_page').click(function () {
    if($("#input_page").val()>page_max||$("#input_page").val()< 1){ alert('不存在') }
    else{page=parseInt($("#input_page").val());
    $("#goods_table").empty();
    var content='<table class=\'table table-striped table-bordered table-hover table-condensed\'><tr><td>产品id</td><td>产品名称</td><td>产品规格</td></tr>';
    $.getJSON(url,{'page':page,'zTreeNodeid':zTreeNodeid,},function(data,status){
        $.each(data,function(i,item){
            content += '<tr><td>'+item.fields.goods_id+'</td>'+'<td>'+item.fields.name+'</td>'+'<td>'+item.fields.specifications+'</td></tr>';
        });
           content += '</table>';
          $("#goods_table").html(content);
    });
    $("#page").empty();
    $("#page").append('第'+page+'页');}
    });