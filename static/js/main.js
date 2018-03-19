$(document).ready(function(){

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
    // Add validation for time, make sure there is no conflict with other games.
    //$.validator.addMethod('time', function(value, element, param) {

    //    return value.match(/^([01][0-9]|2[0-3]):[0-5][0-9]$/);
    //}, 'It appears you already have a game scheduled during this time.');

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
