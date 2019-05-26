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

function showTime(time_int) {
    var date = new Date(parseInt(time_int) * 1000);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    var d = date.getDate();
    var h = date.getHours();
    var mm = date.getMinutes();
    var s = date.getSeconds();
    return y + '-' + m + '-' + d + ' ' + h + ':' + mm + ':' + s;
}


function startTask() {
    var task_id = getParam("task_id");
    $.ajax({
            url: "/api/v1/automl/task/" + task_id + "/start",
            type: "get",
            success: function (request) {
            var task_info = request["data"];
            var code = request["code"];
            var msg = request["msg"];
            if (code==200){
                $("#start").addClass("disabled").text("running");
                $("#start_time").text(showTime(task_info["start_time"]));
                alert(task_info["status"]);
            }
            else
                alert(msg)
            },
            error: function () {
                alert("failed to obtain task detail.")
            }
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
            var show_list = ['task_id', 'task_name', 'create_time', "time_max",
                'start_time', 'end_time', 'data_name', 'status', 'model_type'];
            for(var i=0; i < show_list.length; i++){
                if (show_list[i].endsWith("time")){
                    var time_format = "";
                    if (task_info[show_list[i]] != null){
                        time_format = showTime(task_info[show_list[i]]);
                    }
                    $("#"+ show_list[i]).text(time_format)
                }
                else
                    if (show_list[i] == "time_max")
                        $("#"+ show_list[i]).text(task_info[show_list[i]] + "s");
                    else
                        $("#"+ show_list[i]).text(task_info[show_list[i]])
            }
            if  (task_info["status"] == "done"){
                $("#start").remove()
            }
            else if (task_info["status"] != "ready"){
                $("#start").addClass("disabled").text(task_info["status"])
            }
            if  (task_info["model_type"] == "Classification"){
                $("#metrics").text("Best Accuracy")
            }
            else if (task_info["model_type"] == "Regression"){
                $("#metrics").text("Best MSE")
            }
            else
                $("#metrics").text("Best Metrics");
            $('#hyper_parameters').val(JSON.stringify(
                JSON.parse(task_info["hyper_parameters"]), null, 4));
        }
    }
);
