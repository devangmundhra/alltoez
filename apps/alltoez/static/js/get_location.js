$(document).ready(function() {
    // if the browser supports the w3c geo api
    if (navigator.geolocation){
      // get the current position
      navigator.geolocation.watchPosition(
          // if this was successful, get the latitude and longitude
          function(position){
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            $.cookie('latitude', lat, { expires: 7, path: '/' });
            $.cookie('longitude', lon, { expires: 7, path: '/' });
          },
          // if there was an error, track it
          function(error){
            ga('send', 'event', 'error', 'geolocation', error.code);
      });
    }
});
