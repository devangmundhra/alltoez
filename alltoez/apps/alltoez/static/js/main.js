function resizeHeader() {
	var wHeight = $(window).height();
	$("#above-the-fold").height(wHeight - 210);
	$("body.home h1").css('margin-top', ($("#above-the-fold").height()/2)-140);
}

FB.init({
    appId : '436853689787509', status : true, cookie : true, oauth: true
});

function sendReqeustViaMultiFriendSelector() {
        FB.ui({method: 'apprequests', message: 'Hey! Check out Alltoez.com' }, requestCallback);
}

function requestCallback(request) {
    
}

stLight.options({
		publisher:'30d160e5-ade8-4bce-9178-16fb2e401fcf',
	});

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

    $('.invite').on('click', function(e) {
        e.preventDefault();
        sendReqeustViaMultiFriendSelector();
        return false;
    });

    $('.share-buttom').on('click', function(e) {
        e.preventDefault();
    });

});
