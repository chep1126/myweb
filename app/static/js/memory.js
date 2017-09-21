/**
 * Created by cep on 2017/9/19.
 */
$('#tb_departments').bootstrapTable({
    sortable: false,                     //是否启用排序
    sortOrder: "asc"
})
var xmlhttp
function handle(url,fun) {
    if (window.XMLHttpRequest)
      {// IE7+, Firefox, Chrome, Opera, Safari 代码
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// IE6, IE5 代码
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
    xmlhttp.onreadystatechange=fun;
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}

function del_item(item_id) {
    handle('/memory/del/'+item_id,function () {
        if(xmlhttp.readyState==4&&xmlhttp.status==200){
            var tr=document.getElementById("tr-"+item_id)
            tr.parentNode.removeChild(tr)
        }
    });
}
function recover_item(item_id) {
    handle('/memory/recovery/'+item_id,function () {
        if(xmlhttp.readyState==4&&xmlhttp.status==200){
            var tr=document.getElementById("tr-"+item_id)
            tr.parentNode.removeChild(tr)
        }
    });
}

function show_today_items() {
    var myDate = new Date()
    var year = myDate.getFullYear()
    var month = myDate.getMonth()
    var day = myDate.getDate()
    var date ;
    if(month<9){
        month="0"+String(month+1)
    }else {
        month=String(month+1)
    }
    if(day<10){
        day=String("0"+day)
    }else {
        day=String(day)
    }
    date=String(year)+"-"+month+"-"+day
    handle('/memory/query',function () {
        if(xmlhttp.readyState==4&&xmlhttp.status==200){
            var json_data = JSON.parse(xmlhttp.response)
            var table = document.getElementById("items-table")
            var data = "<tr><th width='10%' class='bg-success'>创建日期</th><th width='10%' class='bg-success'>执行日期</th><th class='bg-success'>内容</th><th class='bg-success'>操作</th></tr>"
            for(var i = 0;i<json_data.length;i++){
                var d = json_data[i]
                if (d.do_time== date){
                    data = data+"<tr id='tr-"+d.id+"'>"+"<td width='10%' class='bg-success'>"+d.create_time+"</td>"+"<td width='10%' class='bg-success'>"+d.do_time+"</td>"+"<td  class='bg-success'>"+d.content+"</td>"+"<td width='10%' class='bg-success'><button onclick='del_item("+d.id+")'  class='btn  btn-danger'>删除</button></td>"+"</tr>"
                }
            }
            table.innerHTML=data
        }
    })

}
function show_not_done_items() {

    handle('/memory/query',function () {
        if(xmlhttp.readyState==4&&xmlhttp.status==200){
            var json_data = JSON.parse(xmlhttp.response)
            var table = document.getElementById("items-table")
            var data = "<tr><th width='10%' class='bg-success'>创建日期</th><th width='10%' class='bg-success'>执行日期</th><th class='bg-success'>内容</th><th class='bg-success'>操作</th></tr>"
            for(var i = 0;i<json_data.length;i++){
                var d = json_data[i]
                if (!d.is_done){
                    data = data+"<tr id='tr-"+d.id+"'>"+"<td width='10%' class='bg-success'>"+d.create_time+"</td>"+"<td width='10%' class='bg-success'>"+d.do_time+"</td>"+"<td  class='bg-success'>"+d.content+"</td>"+"<td width='10%' class='bg-success'><button onclick='del_item("+d.id+")'  class='btn  btn-danger'>删除</button></td>"+"</tr>"
                }
            }
            table.innerHTML=data
        }
    })

}

function show_done_items() {
    
    handle('/memory/query',function () {
        if(xmlhttp.readyState==4&&xmlhttp.status==200){
            var json_data = JSON.parse(xmlhttp.response)
            var table = document.getElementById("items-table")
            var data = "<tr><th width='10%' class='bg-success'>创建日期</th><th width='10%' class='bg-success'>执行日期</th><th class='bg-success'>内容</th><th class='bg-success'>操作</th></tr>"
            for(var i = 0;i<json_data.length;i++){
                var d = json_data[i]
                if (d.is_done){
                    data = data+"<tr id='tr-"+d.id+"'>"+"<td width='10%' class='bg-success'>"+d.create_time+"</td>"+"<td width='10%' class='bg-success'>"+d.do_time+"</td>"+"<td  class='bg-success'>"+d.content+"</td>"+"<td width='10%' class='bg-success'><button onclick='recover_item("+d.id+")'  class='btn  btn-danger'>恢复</button></td>"+"</tr>"
                }

            }
            table.innerHTML=data
        }
    })
    
}


