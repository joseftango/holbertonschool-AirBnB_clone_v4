$(document).ready(function () {
	let checked_amenities = {};

	$('input[type=checkbox]').click(function () {

		if ($(this).is(':checked')) {
			checked_amenities[$(this).attr('data-id')] = $(this).attr('data-name');
		} else {
			delete checked_amenities[$(this).attr('data-id')];
		}
    
        const names = Object.values(checked_amenities);
        let display = names.slice(0, 3).join(', ');
        if (display.length > 40) {
            display = display.slice(0, 40)
            display += ' ...';
        }

        $('.amenities > h4').text(display);
    });

    $.get("http://127.0.0.1:5001/api/v1/status/", function(data, textStatus)
	{
		if(data.status == 'OK') {
            $('div#api_status').addClass('available')
        }
        else {
            $('div#api_status').removeClass('available')
        }
	});

    $.ajax({
    url: 'http://127.0.0.1:5001/api/v1/places_search',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({}),
    success: function(places) {
        // console.log(places);
        places.sort((a, b) =>
        a.name.localeCompare(b.name));
        places.forEach(place => {
        const article = $(`
        <article>
          <div class="headline">
            <h2>${place.name}</h2>
            <div class="price_by_night">$${place.price_by_night}</div>
          </div>
          <div class="information">
            <div class="max_guest">
              <div class="guest_icon"></div>
              <p>${place.max_guest} Guests</p>
            </div>
            <div class="number_rooms">
              <div class="bed_icon"></div>
              <p>${place.number_rooms} Bedrooms</p>
            </div>
            <div class="number_bathrooms">
              <div class="bath_icon"></div>
              <p>${place.number_bathrooms} Bathrooms</p>
            </div>
          </div>
          <div class="description">
            <p>${place.description}</p>
          </div>
        </article>`);

        $('.places').append(article);

        });

    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
    });

});
