$(document).ready(function(){


    // Edit the  pitch booking entry when button is clicked.
    $(".col-4").on("click", "#editBooking", function(e){

        e.preventDefault();

        // Get url and gameid from element tag IDs.
        $.ajax({
            type:"POST",
            url: "edit_booking/",
            data: {
                "gameid": $(this).data("gameid"),
                csrfmiddlewaretoken: $(this).data("csrf_token"),
            },
            dataType: "json",
            success: function(data) {
                // Refresh game info on success.
                $(".game-pitch-booked").load(" .game-pitch-booked", function(){$(this).children().unwrap()});
            },
            error: function (rs, e) {
                alert('Sorry, there was an error.');
            }
        });
    });

    // Filter the game when filter button is clicked. Collects the necessary data from select element tags.
    $(".game-list-static").on("click", "#filterBtn", function(e){

        e.preventDefault();

        $.ajax({
            type:"POST",
            url: $(this).data("url"),
            data: {
                "game_type": $("#filter-game_type").val(),
                "duration": $("#filter-duration").val(),
                "free_slots": $("#filter-free_slots").val(),
                "price": $("#filter-price").val(),
                csrfmiddlewaretoken: $(this).data("csrf_token"),
            },
            dataType: "html",
            success: function(data) {
                // Refresh game list and filter options on success.
                $(".game-list-filters").load(" .game-list-filters", function(){$(this).children().unwrap()});
                $('.game-players-wrapper').html(data);
            },
            error: function (rs, e) {
                alert('Sorry, there was an error.');
            }
        });
    });

    $(".index-content").on("click", "#redirect", function() {

        window.location.href = $(this).data("url");
    });

    $(".game-list-content, .game-player-table").on("click", " .game-player-link", function() {

        window.location.href = $(this).data("url");
    });

    $(".col-7").on("click", "#edit-account", function() {

        window.location.href = $(this).data("url");
    });

    $( "#account-redirect" ).click(function() {

        window.location.href = $(this).data("url");
    });

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
            "gameid": button.data("gameid"),
            "user": button.data("username"),
            csrfmiddlewaretoken: button.data("csrf_token"),
        },
        dataType: "json",
        success: function(data) {
            if (data.player_added || data.player_removed) {

                // Refresh player list and button options on success.
                $(".game-player-table").load(" .game-player-table", function(){button.children().unwrap()});
                $(".game-player-buttons").load(" .game-player-buttons", function(){button.children().unwrap()});
                $(".span-free-slots").load(" .span-free-slots", function(){button.children().unwrap()});

            } else if (data.game_deleted) {
                window.location.replace("/");
            } else if (data.game_conflict) {
                alert("It appears you already have a game scheduled during this time. Unable to join.");
            } else {
                alert("Unable to process request. There may not be free spaces left for this game.");
            }
        },
        error: function (rs, e) {
            alert('Sorry, there was an error.');
        }
    });
}
