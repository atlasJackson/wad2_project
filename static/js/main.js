$(document).ready(function(){
    $("#joinBtn").on("click", function(e) {
        
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "join_game/",
            data: {
                "gameid": $(this).attr("data-gameid"),
                "user": $(this).attr("data-username"),
                "csrfmiddlewaretoken": "{{ csrftoken }}", 
            },
            dataType: "json",
            success: function(data) {
                if (data.player_added) {
                    // Do something here
                } else {
                    // Do something else here
                    alert("Oh no...");
                }
            },
            error: function (rs, e) {
                console.log( document.csrftoken )
                alert('Sorry, there was an error.');
            }
        });
    });
});