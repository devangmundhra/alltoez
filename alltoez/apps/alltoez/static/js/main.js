function resizeHeader() {
	var wHeight = $(window).height();
	$("#above-the-fold").height(wHeight - 210);
	$("body.home h1").css('margin-top', ($("#above-the-fold").height()/2)-140);
}

$(document).ready(function() {
	resizeHeader();

	$(window).on('resize', function(){
		resizeHeader();
	});

	$("#filter-category").on('click', function(e) {
		e.preventDefault();
		$("#filter-header").toggleClass('visible');
	});

    $('.sort-events').on('change', function(e) {
//        $(".events-list").animate({opacity: 0}, 500, function(){
            var sortBy = $(".sort-events").find(":selected").attr('value')
            document.location.href = window.location.pathname + '?sort='+sortBy;

//            $.get("/events/sort/", {'sort': sortBy}, function(data) {
//                console.log(data);
//                $(".events-list").html(data);
//                $(".events-list").animate({opacity: 1});
//            });
    });
});
