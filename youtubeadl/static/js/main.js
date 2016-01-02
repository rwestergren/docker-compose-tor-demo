/* Main JavaScript file used throughout the YouTubeADL app */

function resetResultDiv() {
    $('#result').html("");
    $('#result').removeClass();
}

$(document).ajaxStart(function() {
    $('#result').removeClass();
    $('#result').addClass('alert');
    $('#result').html("<center><i class=\"fa fa-spinner fa-3x fa-spin\"></i><br><br>Converting video to MP3, please wait, this could take a few minutes...</center>");
});

$(document).ajaxStop(function() {
    $('#result').html();
    $('#convertButton').prop('disabled', false);
});

var downloadForm = $('#downloadForm');
downloadForm.submit(function () {
    // Disable convert button to prevent multiple submissions.
    $('#convertButton').prop('disabled', true);

    $.ajax({
        type: downloadForm.attr('method'),
        url: downloadForm.attr('data-url'),
        data: downloadForm.serialize(),
        success: function (data, textStatus, xhr) {
            if (textStatus == 'success') {
                if (data['is_ready'] == true) {
                    $('#result').addClass("alert-success");
                    $('#result').html("<p>&quot;"+ data['title'] + "&quot; successfully converted!"
                        + "<br><center><strong><u><a href=" + data['download_link'] + " target=_self>"
                        + "Download MP3 File</a></u></strong></center></p>");
                } else {
                    $('#result').addClass("alert-danger");
                    $('#result').html(data['message']);
                }
            } else {
                resetResultDiv();
                alert(data['message']);
            }
        },
        error: function(data) {
            resetResultDiv();
            alert("Sorry, something went wrong. Please try again.");
        }
    });
    return false;
});