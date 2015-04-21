var model = {
    period: 15,
    setVisit: function(visit){
        $.cookie('visit', visit, {expires: 1, path: '/'});
    },
    setShowed: function(showed){
        $.cookie('showed', showed, {expires: 1, path: '/'});
    },
    getVisit: function(){
        var visit = $.cookie('visit');
        if(visit){
            return new Number(visit);
        }
        return null;
    },
    getShowed: function(){
        var showed = $.cookie('showed');
        if(showed){
            return showed == 'true';
        }
        return false;
    },
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
    init: function(){
        var isLoggedIn = window.isLoggedIn;
        var showed = model.getShowed();
        if(!isLoggedIn && !showed){
            var visit = model.getVisit();
            if(!visit){
                model.setVisit(Date.now());
                model.setShowed(false);
            }
            this.checkState();
        }

    },
    checkState: function(){
        if(model.isDue()){
            view.render();
            model.setShowed(true);
        } else {
            setTimeout(controller.checkState, 1000);
        }
    }
};

var view = {
    render: function(){
        var elem = $(template);
        elem.dialog({
            modal: true,
            buttons: {
                Ok: function(){
                    $(this).dialog('close');
                }
            }
        });
    }
};

var template = '<div id="dialog-message" title="Like what you see?">' +
   '<p>Login using <a href="/accounts/facebook/login/?process=login">Facebook</a> or <a href="/accounts/signup/">Signup</a> with your email</p>' +
   '<p>See something missing, let us know.</p>' +
'</div>';

window.onload = function(){
    controller.init();
};
