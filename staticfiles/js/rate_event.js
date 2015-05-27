(function(){
    // rating model
    var rating = {
        // initial rating value
        value: 0,
        //initial rating comment
        comment: '',

        // saving the rating to the backend
        save: function(){
            var self = this;
            console.log(window.user);
            $.ajax({
                type: "POST",
                url: "/api/v1/review/.json",

                // NOTE: this code relies on the 'myevent' variable
                data: JSON.stringify({
                    event: "" + myevent.pk,

                    // user id is attached to the window in the
                    // events/templates/events/event_details.html
                    user: window.user.id,
                    comment: self.comment,
                    rating: self.value
                }),
                contentType: "application/json",
                dataType: "html",
                processData: false,
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("" + textStatus + " in adding review " + errorThrown);
                }
            });
        },
        delete: function(){
            if (myevent.done) {
                return $.ajax({
                    type: "DELETE",
                    url: myevent.done,
                    contentType: "application/json",
                    dataType: "html",
                    processData: false,
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("" + textStatus + " in marking event undone " + errorThrown);
                    },
                    success: function(data, textStatus, jqXHR) {
                        $('#done-action').button("toggle");
                        $('#done-action').removeClass("active");
                        return myevent.done = "";
                    }
                });
            } 
        }
    };

    var controller = {
        init: function(){
            modalView.init();
        },
        getRatingValue: function(){
            return rating.value;
        },
        setRatingComment: function(comment){
            rating.comment = comment;
        },
        setRatingValue: function(value){
            rating.value = value;
        },
        addReview: function(){
            var self = this;
            rating.save();
        
        },
        deleteDone: function(){
            rating.delete();
        }
    };

    var modalView = {
        $elem: $('#modalRating'),
        $warn: $('#modalRatingWarn'),
        $target: $('#done-action'),
        init: function(){
            var self = this;
            // initializing modal for review creation 
            this.$elem.modal({
                keyboard: true,
                show: false
            });

            // initializing the modal for notifying the user
            // about review deletion (upon undone action)
            this.$warn.modal({
                keyboard: true,
                show: false
            });

            // binding event listener to Done action, which
            // either shows the modal or the warning
            this.$target.on('click', function(){
                if(this.className.indexOf('active') == -1){
                    $(this).button("toggle");
                    $(this).addClass("active");
                    self.render();
                } else {
                    self.warn();
                }
            });

            // binding event listener to submit event action
            $('#reviewSubmit').on('click', function(){
                self.submit();
            });
            // binding event listener to submit event action
            $('#reviewDelete').on('click', function(){
                self.deleteReview();
            });
        },
        // rendering the modal for review creation
        render: function(){
            // getting the rating value
            var value = controller.getRatingValue();

            $('#reviewSubmit').attr('disabled', 'disabled');
            this.$elem.modal('show');

            // if the modal has error class for the comment input, then remove it
            /*
            var $textarea = this.$elem.find('textarea');
            $textarea.parent().removeClass('has-error');
            */
            
            // initializing rating stars
            this.$rateit = $('#modalRate');
            this.$rateit.rateit({
                resetable: false,
                min: 0,
                max: 5,
                step: 1
            });

            // updating the rating value in the view
            this.$rateit.rateit('value', value);
            
            // setting an event listener for 'rated' event
            // (updating the rating value)
            this.$rateit.bind('rated', function(){
                var value = $(this).rateit('value');
                controller.setRatingValue(value);
                $('#reviewSubmit').removeAttr('disabled');
            });
        },
        // render warning modal (undone action)
        warn: function(){
            this.$warn.modal('show');
        },
        // hiding the modal
        hide: function(){
            this.$warn.modal('hide');
            this.$elem.modal('hide');
        },

        // submitting the review to the controller
        submit: function(){

            var $textarea = $('#modalRating textarea');
            var comment = $textarea.val();
            /*
            if(!comment){
                $textarea.parent().addClass('has-error');
                return;
            }
            */
            this.hide();
            controller.setRatingComment(comment);
            
            var value = this.$rateit.rateit('value');
            controller.setRatingValue(value);
            
            controller.addReview();
        },
        deleteReview: function(){
            this.hide();
            controller.setRatingValue(0);
            controller.setRatingComment('');
            controller.deleteDone();
        }
    };

    // initialize the controller if the user is authenticated
    $(document).ready(function(){
        if(window.isLoggedIn) controller.init();
    });

})();
