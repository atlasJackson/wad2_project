$(document).ready(function(){

    $('.game-info').on("click", "#span-pitch-label", function() {
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "update_pitch/",
            data: {
                "gameid": $(this).data("gameid"),
                csrfmiddlewaretoken: $(this).data("csrf_token"),
            },
            success: function(data) {
                if (data.pitch_updated) {
                    //$("#span-pitch-label").html({{ game.booked }});
                    //$(".game-info").load(" #span-pitch-label", function(){
                    //    $(this).children().unwrap();
                    //});
                    //$("#span-pitch-label").html(data.pitch_status)
                    /*$("#span-pitch-label").fadeOut(800, function(){
                            $("#span-pitch-label").html(data.pitch_status).fadeIn().delay(2000);

                    });*/
                } else {
                    alert("Unable to process request.");
                }
            },
            error: function (rs, e) {
                alert('Sorry, there was an error.');
            }
        });
    });
});
