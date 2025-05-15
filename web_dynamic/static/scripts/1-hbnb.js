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
});
