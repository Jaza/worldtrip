var worldtrip = worldtrip || {};

worldtrip.location_map = function() {
    var $ = null;
    var map = null;
    var icon_url = null;

    function add_location_marker(k, loc) {
        var marker = new google.maps.Marker({
            icon: icon_url,
            position: new google.maps.LatLng(loc.lat, loc.lon),
            map: map,
            title: loc.title
        });

        google.maps.event.addListener(marker, 'click', function() {
            window.location.href = loc.url;
        });
    }
    
    return {
        init: function(jq) {
            $ = jq;

            var mapOptions = {
                zoom: 1,
                center: new google.maps.LatLng(40.0, 0.0)
            }

            map = new google.maps.Map(document.getElementById('nodemap'), mapOptions);

            if (typeof countries !== 'undefined') {
                icon_url = 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png';
                $.each(countries, add_location_marker);
            }
            if (typeof cities !== 'undefined') {
                icon_url = 'https://maps.google.com/mapfiles/ms/icons/red-dot.png';
                $.each(cities, add_location_marker);
            }
        }
    }
}();


jQuery(function() {
    worldtrip.location_map.init(jQuery);
});
