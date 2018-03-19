$(document).ready(function(){

    // Scripts for sign_up template
    $("#user_form").validate({
        rules: {
            username: {required: true, alphanumeric: true},
            email: {required: true, email: true},
            first_name: {required: true, nameFormat: true},
            last_name: {required: true, nameFormat: true},
            password: {required: true, minlength: 5},
            password_confirm: {required: true, minlength: 5, equalTo: "#id_password"},
        },
        messages: {
            password_confirm: {
                equalTo: "The passwords don't match."
            },
        }
    });

    // Add validation for username, allow only alphanumeric values.
    $.validator.addMethod('alphanumeric', function(value, element, param) {
        return value.match(/^[a-zA-Z0-9]+$/);
    }, 'Please only use letters and numbers.');
    // Add validation for name and surname.
    $.validator.addMethod('nameFormat', function(value, element, param) {
        return value.match(/^[a-zA-ZäöüÄÖÜéàè\-]+$/);
    }, 'Please only use letters and dashes.');

    // Scripts for create_game template
    $("#game_form").validate({
        rules: {
            date: {},
            time: {required: true, time: true},
            street: {required: true, maxlength: 128},
            place: {required: true, maxlength: 128},
            postcode: {required: true, minlength: 5, maxlength: 8},
            price: {required: true, range: [0, 20]},
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
