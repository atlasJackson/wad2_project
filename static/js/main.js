$(document).ready(function(){

    $(".game-player-static").on("click", "#joinBtn", function(e) {
        
        e.preventDefault();
        buttonJoinLeave($(this), "join_game/");
    });


    $(".game-player-static").on("click", "#leaveBtn", function(e) {
        
        e.preventDefault();
        buttonJoinLeave($(this), "leave_game/");
    });
});    

function buttonJoinLeave(button, urlLink) {
    $.ajax({
        type: "POST",
        url: urlLink,
        data: {
            "gameid": button.attr("data-gameid"),
            "user": button.attr("data-username"),
            "csrfmiddlewaretoken": "{{ csrftoken }}", 
        },
        dataType: "json",
        success: function(data) {
            if (data.player_added || data.player_removed) {
                // Refresh player list and button options on success.
                $(".game-player-list").load(" .game-player-list", function(){button.children().unwrap()});
                $(".game-player-buttons").load(" .game-player-buttons", function(){button.children().unwrap()});
            } else {
                // This should not be reached.
                alert("Oh no...");
            }
        },
        error: function (rs, e) {
            console.log( document.csrftoken )
            alert('Sorry, there was an error.');
        }
    });
}

/*
function loadDoc(url,cFunction) {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            cFunction(this);
        }
    }
}
*/

