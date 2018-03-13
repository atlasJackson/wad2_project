$(document).ready(function(){

    $(".game-player-static").on("click", "#joinBtn", function(e) {

        e.preventDefault();
        buttonJoinLeaveDelete($(this), "join_game/");
    });

    $(".game-player-static").on("click", "#leaveBtn", function(e) {

        e.preventDefault();
        buttonJoinLeaveDelete($(this), "leave_game/");
    });

    $(".game-player-table").on("click", "#removeBtn", function(e) {
        
        e.preventDefault();
        buttonJoinLeaveDelete($(this), "leave_game/");
    });

    $(".game-player-static").on("click", "#deleteBtn", function(e) {
        var confirmDelete = confirm("Are you sure you want to delete this game?");
        if (confirmDelete) {
            e.preventDefault();
            buttonJoinLeaveDelete($(this), "delete_game/");
        }
    });
});

function buttonJoinLeaveDelete(button, urlLink) {
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
                $(".game-player-table").load(" .game-player-table", function(){button.children().unwrap()});
                $(".game-player-buttons").load(" .game-player-buttons", function(){button.children().unwrap()});
            } else if (data.game_deleted) {
                window.location.replace("/");

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

