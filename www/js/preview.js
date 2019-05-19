/**
 * Created by xu on 2019/5/19.
 */
function getParam(paramName) {
    paramValue = "", isFound = !1;
    if (this.location.search.indexOf("?") == 0 && this.location.search.indexOf("=") > 1) {
        arrSource = unescape(this.location.search).substring(1, this.location.search.length).split("&"), i = 0;
        while (i < arrSource.length && !isFound) arrSource[i].indexOf("=") > 0 && arrSource[i].split("=")[0].toLowerCase() == paramName.toLowerCase() && (paramValue = arrSource[i].split("=")[1], isFound = !0), i++
    }
    return paramValue == "" && (paramValue = null), paramValue
}

function jsonShowFn(json){
    if (!json.match("^\{(.+:.+,*){1,}\}$")) {
        return json           //判断是否是json数据，不是直接返回
    }

    if (typeof json != 'string') {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

$(document).ready(
    function preview() {
        var task_id = getParam("task_id");
        $.ajax({
            url: "/api/v1/automl/task/" + task_id,
            type: "get",
            success: function (request) {
            var task_info = request["data"];
            var code = request["code"];
            var msg = request["msg"];
                showTaskStatus(task_info);
            },
            error: function () {
                alert("failed to obtain task detail.")
            }
        });
        function showTaskStatus(task_info) {
            var show_list = ['task_id', 'task_name', 'create_time',
                'start_time', 'end_time', 'data_name', 'status', 'model_type'];
            for(var i=0; i < show_list.length; i++){
                if (show_list[i].endsWith("time")){
                    var time_format = "";
                    if (task_info[show_list[i]] != null){
                        var date = new Date(parseInt(task_info[show_list[i]]) * 1000);
                        var y = date.getFullYear();
                        var m = date.getMonth() + 1;
                        var d = date.getDate();
                        var h = date.getHours();
                        var mm = date.getMinutes();
                        var s = date.getSeconds();
                        time_format = y + '-' + m + '-' + d + ' ' + h + ':' + mm + ':' + s;
                    }
                    // if (task_info[show_list[i]] != null)
                    //     time_format = new Date(parseInt(task_info[show_list[i]]) * 1000).toLocaleString();
                    $("#"+ show_list[i]).text(time_format)
                }
                else
                    $("#"+ show_list[i]).text(task_info[show_list[i]])
            }
            if (task_info["status"] != "ready"){
                $("#start").addClass("disabled")
            }
            $('#hyper_parameters').html(jsonShowFn(task_info["hyper_parameters"]))
        }
    }
);
