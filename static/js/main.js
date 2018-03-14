$(document).ready(function(){

    $(".game-player-table").on("click", "#game-link", function() {

        window.location.href = $(this).data("url");
    });

    $(".game-player-table").on("click", "#player-link", function() {

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
            start_time: {required: true, time: true},
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
    }, 'Enter a valid time: hh:mm');

    $("#id_start").datepicker({
        minDate: 0, // Can't select dates in the past.
        maxDate: 30, // Can only select dates within 30 days from today.
        dateFormat: "mm/dd/yy",
    });
    $('#id_start').datepicker('setDate', new Date()); // .datepicker('setDate', date) sets the current date for the datepicker.

    // Checks if date lies in the past, if so, set date to today.
    $("#id_start").datepicker().change(evt => {
        var selectedDate = $("#id_start").datepicker('getDate');
        var today = new Date();
        today.setHours(0,0,0,0);
        if (selectedDate < today) {
            $('#id_start').datepicker('setDate', new Date());
        }
    });



    time_choices: ["8:30", "9:30", "10:30", "11:30", "12:30"]

    $("#id_start_time").time_picker({});

    $("#id_start_time").innerhtml(time_choices);

});


function buttonJoinLeaveDelete(button, urlLink) {
    $.ajax({
        type: "POST",
        url: urlLink,
        data: {
            "gameid": button.attr("data-gameid"),
            "user": button.attr("data-username"),
            csrfmiddlewaretoken: "{{ csrftoken }}",
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
            console.log( document.csrftoken )
            alert('Sorry, there was an error.');
        }
    });
}
