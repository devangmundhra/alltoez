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
});
