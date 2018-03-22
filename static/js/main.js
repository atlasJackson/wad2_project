$(document).ready(function(){


    // Make use of the Google Maps API to display maps.
    var map
    function initMap() {
        var mapDisplay = document.getElementById("map-display");

        var latitude = mapDisplay.getAttribute("data-latitude");
        var longitude = mapDisplay.getAttribute("data-longitude");
        var thisLatLng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};

        var mapOptions = {
            center: thisLatLng,
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        map = new google.maps.Map(mapDisplay, mapOptions);

        var marker = new google.maps.Marker({
          position: thisLatLng,
          map: map,
        });
    }

    // Validate login form.
    $("#login_form").validate({
        rules: {
            username: { // Must match the name attribute of the input field.
                required: true,
                minlength: 4
            },
            password: "required"
        },
        messages: {
            username: {
                required: "Please enter your username",
                minlength: "Must be at least 4 characters long"
            },
            password: "Please enter your password"
        }
    });

    // Validate form when editing user details.
    $("#edit_user_form").validate({
        rules: {
            first_name: {required: true, nameFormat: true},
            last_name: {required: true, nameFormat: true},
            email: {required: true, email: true}
        }
    });

    // Validate registration form.
    $("#user_form").validate({
        rules: {
            username: {required: true, alphanumeric: true, minlength: 4},
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
        return value.match(/^[a-zA-ZäöüÄÖÜéàè" "\-]+$/);
    }, 'Please only use letters and dashes.');

    // Validation for create game form.
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

    // Add Sorting and Filtering options to sortable game_table.
    $("#game_sorttable").tablesorter({
        theme : "bootstrap",
        widthFixed: true,
        // widget code contained in the jquery.tablesorter.widgets.js file
        // use the zebra stripe widget if you plan on hiding any rows (filter widget)
        // the uitheme widget is NOT REQUIRED!
        widgets : [ "filter", "zebra" ],
        widgetOptions : {
            // Delay in milliseconds before the filter widget starts searching; This option prevents searching for
            // every character while typing and should make searching large tables faster.
            filter_searchDelay : 300,
            // using the default zebra striping class name, so it actually isn't included in the theme variable above
            // this is ONLY needed for bootstrap theming if you are using the filter widget, because rows are hidden
            zebra : ["even", "odd"],
            // class names added to columns when sorted
            columns: [ "primary", "secondary", "tertiary" ],
            // reset filters button
            filter_reset : ".reset",
            // extra css class name (string or array) added to the filter element (input or select)
            filter_cssFilter: [
                'form-control',
                'form-control',
                'form-control',
                'form-control',
                'form-control',
                'form-control',
                'form-control'
            ],

            // Options for type selection.
            filter_selectSource: {
                4 : [ "Men's Competitive", "Men's Friendly", "Women's Competitive",
                        "Women's Friendly", "Mixed Competitive", "Mixed Friendly" ],
            },

            // function variables: e = exact text from cell, n = normalized value returned by the column parser, f = search filter input value, i = column index.
            filter_functions : {
                2 : {
                    "1 hour" : function(e, n, f, i, $r, c, data) { return $r.find('.time').attr('data-duration') == 1; },
                    "2 hours" : function(e, n, f, i, $r, c, data) { return $r.find('.time').attr('data-duration') == 2; },
                },

                // Options for selection of minimum free spaces.
                3 : {
                    "1" : function(e, n, f, i, $r, c, data) { return n >= 1; },
                    "2" : function(e, n, f, i, $r, c, data) { return n >= 2; },
                    "3" : function(e, n, f, i, $r, c, data) { return n >= 3; },
                    "4" : function(e, n, f, i, $r, c, data) { return n >= 4; },
                    "5" : function(e, n, f, i, $r, c, data) { return n >= 5; },
                    "6" : function(e, n, f, i, $r, c, data) { return n >= 6; },
                    "7" : function(e, n, f, i, $r, c, data) { return n >= 7; },
                    "8" : function(e, n, f, i, $r, c, data) { return n >= 8; },
                    "9" : function(e, n, f, i, $r, c, data) { return n >= 9; },
                },
                // Oprions for selection of maximum price.
                5 : {
                    "Free" : function(e, n, f, i, $r, c, data) { return n == 0; },
                    "3" : function(e, n, f, i, $r, c, data) { return n <= 3; },
                    "5" : function(e, n, f, i, $r, c, data) { return n <= 5; },
                    "10" : function(e, n, f, i, $r, c, data) { return n <= 10; },
                    "20" : function(e, n, f, i, $r, c, data) { return n <= 20; },
                    "50" : function(e, n, f, i, $r, c, data) { return n <= 50; },
                    "100" : function(e, n, f, i, $r, c, data) { return n <= 100; },
                }
            }
        }
    });

});
