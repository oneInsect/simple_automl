/**
 * Created by xu on 2019/5/2.
 */
$(document).ready(
  function createTable(){
        $.ajax({
        url: "/api/v1/automl/task",
        type: "get",
        success: function (tasks_data) {
            var table_rows = tasks_data["data"];
            var code = tasks_data["code"];
            var msg = tasks_data["msg"];
            if (code == 200){
                structure_task_table(table_rows);}
            else {
                alert(msg)
            }
        },
        error: function () {
            alert("failed to obtain table data.")
        }
    });
        function structure_task_table(table_rows) {
            var tableHead = [{"field": "task_id", "title": "Task ID" },
                              {"field": "task_name", "title": "Task Name"},
                              {"field": "model_type", "title": "Model Type" },
                              {"field": "data_name", "title": "Data Name" },
                              {"field": "status", "title": "Status" },
                              {"title": "Operation" }];
            var cellCount = tableHead.length;
            var rowCount = table_rows.length;
            var table = $("<table>");

            table.addClass("table table-hover");
            var trHeader = $("<tr></tr>");
            trHeader.appendTo(table);
            for (var j = 0; j < cellCount; j++) {
                var th = $("<th>" + tableHead[j].title + "</th>");
                th.appendTo(trHeader);
            }
            for (var i = 0; i < rowCount; i++) {
                var tr = $("<tr></tr>");
                tr.appendTo(table);
                for (var k = 0; k < cellCount-1; k++) {
                    var field = tableHead[k].field;
                    var val = table_rows[i][field];
                    var td = $("<td>" + val + "</td>");
                    if (k == 0) {
                        td.addClass("taskID");
                        }
                    td.appendTo(tr);
                }
                var td_bt = $("<td><button type='button' onclick='task_detail(this)' class='btn btn-xs btn-info'>Detail</button>" +
                    //        "<button type='button' onclick='task_editor(this)' class='btn btn-xs btn-warning'>Editor</button>" +
                            "<button type='button' onclick='task_delete(this)' class='btn btn-xs btn-danger'>Delete</button>" +
                            "</td>");
                td_bt.appendTo(tr);
            }
            table.append("</table>");
            table.appendTo($("#task_table"));
        }
    }
);