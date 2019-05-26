/**
 * Created by xu on 2019/5/19.
 */
$(document).ready(
    function ready_page(){
		$.ajax({
			url: "/api/v1/automl/version",
            type: "get",
			success: function (versionInfo) {
				showVersion(versionInfo);
			},
			error: function () {
                alert("Failed to obtain version information.");
            }
		});
		function showVersion(versionInfo) {
            $("#version").text(versionInfo)
        }

	});