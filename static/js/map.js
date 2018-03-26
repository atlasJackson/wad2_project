/* javascript used to show a map. */

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
