var loginPrompt = new function(){
    var that = this;

    this.model = {
        // wait period in seconds
        period: 30,
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

    this.controller = {
        // initializing the controller
        init: function(){
            var isLoggedIn = window.isLoggedIn;
            var showed = that.model.getShowed();
            that.view.init();

            // if the user is not logged in and
            // the popup hasn't been showed today
            if(!isLoggedIn && !showed){
                var visit = that.model.getVisit();
                if(!visit){
                    that.model.setVisit(Date.now());
                    that.model.setShowed(false);
                }
                // performing checks whether we could
                // show the popup
                this.checkState();
            }

        },
        checkState: function(){
            if(that.model.isDue()){
                // show the popup and change its status
                that.view.render();
                that.model.setShowed(true);
            } else {
                // wait 1 sec and perform the check once again
                setTimeout(that.controller.checkState, 1000);
            }
        },
        renderOnAction: function(){
            that.view.renderOnAction();
        }
    };

    this.view = {
        // initializing the loginModal
        init: function(){
            var self = this;
            this.elem = $('#loginModal');
            this.elem.modal({
               keyboard: true,
               show: false
            });

            this.elemActions = $('#loginModalActions');
            this.elemActions.modal({
               keyboard: true,
               show: false
            });

            // get Done and Bookmark buttons
            var doneButton = $('#done-action');
            var bookmarkButton = $('#bookmark-action');
            var reviewButton = $('#review-action');

            // if the buttons are on the page,
            // attach an event on click, on this event
            // a login prompt should be done -- renderOnAction
            if(doneButton){
                doneButton.on('click', function(){
                    if(!isLoggedIn){
                        self.renderOnAction();
                    };
                });
            }
            if(bookmarkButton){
                bookmarkButton.on('click', function(){
                    if(!isLoggedIn){
                        self.renderOnAction();
                    };
                });
            }
            if(reviewButton){
              reviewButton.on('click', function(){
                    if(!isLoggedIn){
                        self.renderOnAction();
                    };
                });
            }
        },
        // rendering the popup
        render: function(){
            this.elem.modal('show');
        },
        // rendering the modal which prompts signing in
        // to perform the action (Done or Bookmark)
        renderOnAction: function(){
            this.elemActions.modal('show');
        }
    };
}
$(document).ready(function(){
    loginPrompt.controller.init();
});
