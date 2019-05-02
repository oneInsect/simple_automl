/**
 * Created by xu on 2019/5/2.
 */
$(document).ready(
    function getVersion(){
		$.ajax({
			url: "/api/v1/automl/version",
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
	}
	);