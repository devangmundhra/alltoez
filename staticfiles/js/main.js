function resizeHeader() {
	var wHeight = $(window).height();
	$("#above-the-fold").height(wHeight - 210);
	$("body.home h1").css('margin-top', ($("#above-the-fold").height()/2)-140);
}

function sendRequestViaMultiFriendSelector() {
        FB.ui({method: 'apprequests', message: 'Events for kids and parents at alltoez.com' }, requestCallback);
}

function shareLinkOnFb(link) {
    FB.ui({method: 'share', href: link }, requestCallback);
}

function shareEventLinkViaEmail(title, link) {
    window.location.href = "mailto:?subject="+title+"&body=I think you will like the event "+title+" at "+link
}

function requestCallback(request) {
    
}

function filterAutoCompleteResults(parsedResponse) {
    return parsedResponse.results;
}

$(document).ready(function() {
//	resizeHeader();

//	$(window).on('resize', function(){
//		resizeHeader();
//	});

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

//    $('.invite').on('click', function(e) {
//        e.preventDefault();
//        sendRequestViaMultiFriendSelector();
//        return false;
//    });

    $('.no-invite').on('click', function(e) {
        e.preventDefault();
        $('#no-more-invites-modal').modal()
        return false;
    });

    $.cookie.raw = true;
});
