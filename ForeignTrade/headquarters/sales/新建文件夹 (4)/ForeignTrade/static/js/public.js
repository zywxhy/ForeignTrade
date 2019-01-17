var obj = {
    init: function (data) {
        var data = data;
        this.bind(data);
    },
    subdact:function(){ //     判断是否有减数
        var amount = $("#id_total_amount").val();
        var subtraction = $('#id_bill_amount').val();
        var remain = parseInt(amount - subtraction);
        if(subtraction===undefined){
            
        }else if(remain >= 0){
            $("#id_not_bill_amount").val(remain);
        }else{
            alert("请注意！");
            $('#id_bill_amount').val(0);
            $("#id_not_bill_amount").val(amount);
        }
    },
    callback: function (data) {
        var list = {};
        var map = new Map();
        $.each(data, function (index, item) {
            var key = $(item).prop("name");
            var value = $(item).val();
            list[key] = value;
        });
        return list;
    },
    get_exrate:function(){
            var currency = $("#id_currency").val();
            $.getJSON("/finance/get_exchange_rate/", {'currency': currency}, function (index, status) {
                $('#id_exrate').val(index);
            })
    },
    bind: function (data) {
        var self = this;
        var formdata;
        layui.use(['table', 'layer'], function () {
            var table = layui.table;
            var $ = layui.$;
            var layer = layui.layer;
            table.render({              //父页面的table
                elem: '#layuiDemo'
                , data: data
                , toolbar: '#toolbarDemo'
                , page: true
                ,defaultToolbar:[]
                , id: 'testReload'
                , cols: [[
                    {type: 'checkbox', align: "center"}
                    , {field: "product_id", title: "产品代码", align: "center"}
                    , {field: "name", title: "名字", align: "center"}
                    , {field: "spec", title: "规格", align: "center"}
                    , {field: "remark", title: "备注", align: "center", edit: 'text'}
                    , {field: "mesu_unit", title: "单位", align: "center"}
                    , {field: "volume", title: "体积", align: "center"}
                    , {field: "unit_price", title: "单价", align: "center", edit: 'text'}
                    , {field: "count", title: "数量", align: "center", edit: 'text'}
                    , {field: "amount", title: "金额", align: "center"}
                ]]
            });
            table.render({             //子页面的table
                elem: '#firstBlood'
                , url: '/product/product_select'
                , page: true
                , id: 'testchange'
                , cols: [[
                    {field: "product_id", title: "产品id", align: "center", width: 100}
                    , {field: "name", title: "产品名称", align: "center", width: 100}
                    , {field: "spec", title: "产品规格", align: "center", width: 200}
                    , {field: "mesu", title: "计量单位", align: "center", width: 200}
                    , {field: "volume", title: "体积", align: "center", width: 100}
                    , {title: "操作", toolbar: '#titleTpl', align: "center", width: 100}
                ]]
                , parseData: function (res) { //res 即为原始返回的数据
                    return {
                        "code": res.status, //解析接口状态
                        "msg": res.message, //解析提示文本
                        "count": res.total, //解析数据长度
                        "data": res.data //解析数据列表
                    };
                },
            });
            table.on('edit(test)', function (obj) {        //  监听开启编辑，计算金额和总金额
                var data = obj.data;
                active.calculat(data);
            });
            table.on('tool(demo)', function (obj) {            //  监听子页面的tool操作
                var data = obj.data;
                var arr = [];
                var self = this;
                layEvent = obj.event; //获得 lay-event 对应的值
                var getdata = table.cache.testReload;

                $.each(getdata, function (index, item) {
                    arr.push(item.product_id);
                });
                var number = arr.findIndex(function (value) {
                    return value == data.product_id
                });
                console.log(number);
                if (number === -1) {
                    var othis = $(this), method = othis.data('method');
                    active[method] ? active[method].call(this, getdata) : '';

                    if (layEvent === 'add') {
                        $.ajax({
                            type: 'get',
                            data: {'product_id': data.product_id},
                            url: '/product/get_product',
                            success: function (res) {
                                console.log(res);
                                getdata.push({
                                    'product_id': res.data[0].product_id,
                                    'name': res.data[0].name,
                                    'spec': res.data[0].spec,
                                    'mesu': res.data[0].mesu_unit,
                                    'volume': res.data[0].volume
                                })
                                table.reload('testReload', {
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                    , data: getdata
                                });
                            }
                        })
                    }
                }
            });

            table.on('toolbar(test)', function (obj) {         //table头部事件监听
                var checkStatus = table.checkStatus(obj.config.id);
                switch (obj.event) {
                    case 'add':
                        var othis = $(this), method = othis.data('method');
                        active[method] ? active[method].call(this, othis) : '';
                        break;
                    case 'delete':
                        var arr = [];
                        var id_arr = [];
                        var getdata = table.cache.testReload;

                        $.each(checkStatus.data, function (index, item) {
                            id_arr.push(item.product_id);
                        });
                        for (var value of getdata) {
                            if (id_arr.indexOf(value.product_id) === -1) {
                                arr.push(value);
                            }
                        }
                        ;
                        var count_num = 0;
                        $.each(arr, function (index, item) {
                            count_num += parseInt(item.amount);
                        });
                        //input框
                        var data1 = $("#sales_order_add input.changeable");
                        $.each(data1, function (index, item) {
                            count_num = count_num + parseInt($(item).val());
                        });
                        $("#id_total_amount").val(count_num);
                        self.subdact();

                        table.reload('testReload', {
                            page: {
                                curr: 1 //重新从第 1 页开始
                            }
                            , data: arr
                        });
                        break;
                }
                ;
            });
            var active = {
                setTop: function () {            //  监听按钮add 开启弹出层
                    var that = this;
                    layer.open({
                        type: 1
                        , content: $('#infoDemo')
                        , title: '添加产品'
                        , area: ['auto','auto']
                        , shadeClose: true
                        , shade: .3
                        , zIndex: layer.zIndex //重点1
                        , success: function (layero) {
                            $('#demoReload').val("");
                            active.reloadchild();
                        }
                        , btn: ['全部关闭'] //只是为了演示
                        , yes: function () {
                            layer.closeAll();
                            $('#demoReload').val("");
                        }
                    })
                },
                reload: function (data) {             //重载
                    //执行重载
                    table.reload('testReload', {
                        page: {
                            curr: 1 //重新从第 1 页开始
                        }
                        , data: data
                    });
                },
                reloadchild: function () {               //子页面搜索
                    var demoReload = $('#demoReload');
                    //执行重载
                    table.reload('testchange', {
                        // page: {
                        //     curr: 1 //重新从第 1 页开始
                        // }
                        request: {
                            page: 'curr' //页码的参数名称，默认：page
                            , limit: 'nums' //每页数据量的参数名，默认：limit
                        }
                        , where: {
                            search: demoReload.val()
                        }
                    });
                },
                calculat: function (data) {            //计算金额，重载页面
                    var count_num = 0;
                    var total = table.cache.testReload;
                    $.each(total, function (index, item) {
                        if (item.product_id === data.product_id) {
                            item.amount = data.unit_price * data.count;
                        }
                        ;
                        count_num += parseInt(item.amount);
                    })
                    var data1 = $("#sales_order_add input.changeable");
                    $.each(data1, function (index, item) {
                        count_num = count_num + parseInt($(item).val());
                    });

                    $("#id_total_amount").val(count_num);
                    self.subdact();
                    active["reload"].call(this, total);
                },
                submit: function () {                  //提交按钮
                    //first table
                    var inputAll = $("#sales_order_add").find("input");
                    var selectAll = $("#sales_order_add").find("select");
                    var obj1 = self.callback(inputAll);
                    var obj2 = self.callback(selectAll);
                    var data = $.extend({}, obj1, obj2);

                    var tableData = table.cache.testReload;
                    //third table
                    var tableAll = $("#collection").find("input[type!='checkbox']");
                    var tabSelect = $("#collection").find("select");
                    var len = $("#collection tr").length;
                    var array = [];
                    if (len) {
                        for (var i = 0; i < len; i++) {
                            array.push({
                                'receipt_type': $('[name="id_form-' + i + '-receipt_type"]').val(),
                                'receipt_time': $('[name="id_form-' + i + '-receipt_time"]').val(),
                                'receipt': $('[name="id_form-' + i + '-receipt"]').val(),
                                'remark': $('[name="id_form-' + i + '-remark"]').val()
                            })
                        }
                        data.sales_collection = JSON.stringify(array);
                    }
                    //data.csrfmiddlewaretoken = '{{ csrf_token }}';
                    data.sales_product = JSON.stringify(tableData);
                    console.log(JSON.stringify(data));
                    $.post("/sales/add/", data, function (a, b) {
                        alert(a);
                    });
                },
                examine:function(){
                    console.log('1')
                    $.post(url,{result:2},function(){

                    })
                },
                counterTrial:function(){
                    $.post(url,{result:1},function(){})
                }
            };
            $(document).on('change', 'input.changeable', function () {            //产品列表中的金额计算
                var count_num = 0;
                var total = table.cache.testReload;
                $.each(total, function (index, item) {
                    count_num += parseInt(item.amount);
                })
                var data1 = $("#sales_order_add input.changeable");
                $.each(data1, function (index, item) {
                    count_num = count_num + parseInt($(item).val());
                });

                $("#id_total_amount").val(count_num);
                self.subdact();
                active.calculat(total);
            });
            $('#infoDemo .layui-btn').on('click', function () {               //子页面的搜索按钮
                var othis = $(this), method = othis.data('method');
                active[method] ? active[method].call(this) : '';
            });
            $('.pull-right .layui-btn').on('click', function () {             //提交监听
                var othis = $(this), method = othis.data('method');
                active[method] ? active[method].call(this) : '';
            });
        });

        $("#id_currency").change(function () {
            self.get_exrate()
        });
        $('#id_bill_amount').on('change',function(){
            self.subdact();
        });
        //get_exrate();
    }
};
