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

$(document).ready(function() {
    $('.invite').on('click', function(e) {
        e.preventDefault();
        sendRequestViaMultiFriendSelector();
        return false;
    });

    $.cookie.raw = true;
});
