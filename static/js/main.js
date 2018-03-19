$(document).ready(function(){
    $(".index-content").on("click", "#redirect", function() {

        window.location.href = $(this).data("url");
    });

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

    $(".game-list-content, .game-player-table").on("click", " .game-player-link", function() {

        window.location.href = $(this).data("url");
    });

    $(".player-tables-wrapper").on("click", "#account-redirect", function() {

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


    // Scripts for create_game template
    $("#game_form").validate({
        rules: {
            date: {},
            time: {required: true, time: true},
            street: {required: true, maxlength: 128},
            place: {required: true, maxlength: 128},
            postcode: {required: true, minlength: 5, maxlength: 8},
            price: {required: true, range: [0, 99]},
            booked: {required: false},
        },
        messages: {
            postcode: {
                minlength: "Please enter a valid postcode.",
                maxlength: "Please enter a valid postcode."
            },
        }
    });

    // Add validation for time, makes sure it's a valid time in the correct format.
    $.validator.addMethod('time', function(value, element, param) {
        return value.match(/^([01][0-9]|2[0-3]):[0-5][0-9]$/);
    }, 'Enter a valid time (hh:mm)');

    $("#id_date").datepicker({
        minDate: 0, // Can't select dates in the past.
        maxDate: 30, // Can only select dates within 30 days from today.
        dateFormat: "yy-mm-dd",
    });

    $("#id_date").datepicker({
        minDate: 0, // Can't select dates in the past.
        maxDate: 30, // Can only select dates within 30 days from today.
        dateFormat: "yy-mm-dd",
    });
    $('#id_date').datepicker('setDate', new Date()); // .datepicker('setDate', date) sets the current date for the datepicker.

    // Checks if date lies in the past, if so, set date to today.
    $("#id_date").datepicker().change(evt => {
        var selectedDate = $("#id_date").datepicker('getDate');
        var today = new Date();
        var maxDate = new Date(today).setDate(today.getDate()+30);
        today.setHours(0,0,0,0);
        if (selectedDate < today || selectedDate > maxDate) {
            $('#id_date').datepicker('setDate', new Date());
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
            } else {
                alert("Unable to process request. There may not be free spaces left for this game.");
            }
        },
        error: function (rs, e) {
            alert('Sorry, there was an error.');
        }
    });
}
