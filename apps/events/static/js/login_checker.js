var model = {
    // wait period in seconds
    period: 15,
    // setting visit time in cookies
    // Note: the cookie is expired in 1 day, i.e. the popup 
    // will be shown only the next day
    setVisit: function(visit){
        $.cookie('visit', visit, {expires: 1, path: '/'});
    },
    // setting popup status (showed/not showed) in cookies
    // Note: the cookie is expired in 1 day, i.e. the popup 
    // will be shown only the next day
    setShowed: function(showed){
        $.cookie('showed', showed, {expires: 1, path: '/'});
    },
    // getting the visit time and converting it in a Number
    getVisit: function(){
        var visit = $.cookie('visit');
        if(visit){
            return new Number(visit);
        }
        return null;
    },
    // getting popup status
    getShowed: function(){
        var showed = $.cookie('showed');
        if(showed){
            return showed == 'true';
        }
        return false;
    },
    // checking whether the right time period has passed and
    // we could show the popup
    isDue: function(){
        var visit = this.getVisit();
        if(visit) {
            var difference = Date.now() - visit;
            return this.period * 1000 < difference;
        };
        return false;
    }
};

var controller = {
    // initializing the controller
    init: function(){
        var isLoggedIn = window.isLoggedIn;
        var showed = model.getShowed();

        // if the user is not logged in and
        // the popup hasn't been showed today
        if(!isLoggedIn && !showed){
            view.init();
            var visit = model.getVisit();
            if(!visit){
                model.setVisit(Date.now());
                model.setShowed(false);
            }
            // performing checks whether we could
            // show the popup
            this.checkState();
        }

    },
    checkState: function(){
        if(model.isDue()){
            // show the popup and change its status
            view.render();
            model.setShowed(true);
        } else {
            // wait 1 sec and perform the check once again
            setTimeout(controller.checkState, 1000);
        }
    }
};

var view = {
    // initializing the loginModal
    init: function(){
        this.elem = $('#loginModal');
        this.elem.modal({
           keyboard: true,
           show: false
        });
    },
    // rendering the popup
    render: function(){
        this.elem.modal('show');
    }
};

window.onload = function(){
    controller.init();
};
