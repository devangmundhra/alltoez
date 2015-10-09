(function(){
    // rating model
    var rating = {
        // initial rating value
        value: myevent.review ? myevent.review.rating : 0,
        //initial rating comment
        comment: myevent.review ? myevent.review.comment : '',

        // saving the rating to the backend
        save: function(){
            var self = this;
            $.ajax({
                type: myevent.review ? "PUT" : "POST",
                url: myevent.review ? "/api/v1/review/" + myevent.review.id +"/.json" : "/api/v1/review/.json",

                // NOTE: this code relies on the 'myevent' variable
                data: JSON.stringify({
                    event: "" + myevent.pk,

                    // user id is attached to the window in the
                    // events/templates/events/event_details.html
                    user: "" + window.user,
                    comment: self.comment,
                    rating: self.value
                }),
                contentType: "application/json",
                dataType: "html",
                processData: false,
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("" + textStatus + " in adding review " + errorThrown);
                },
                success: function(data, textStatus, jqXHR) {
                  var review;
                  review = JSON.parse(data);
                  return myevent.review = review;
                }
            });
        }
      };

    var controller = {
        init: function(){
            modalView.init();
        },
        getRatingComment: function(){
            return rating.comment;
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

        }
    };

    var modalView = {
        $elem: $('#modalRating'),
        $target: $('#review-action'),
        init: function(){
            var self = this;
            // initializing modal for review creation
            this.$elem.modal({
                keyboard: true,
                show: false
            });

            // binding event listener to Review action, which
            // shows the modal
            this.$target.on('click', function(){
              var isLoggedIn = window.isLoggedIn;
              if (isLoggedIn) {
                self.render();
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
            var $textarea = $('#modalRating textarea');
            if (controller.getRatingComment()){
              $textarea.val(controller.getRatingComment());
            }
            var value = controller.getRatingValue();
            if (!value){
              $('#reviewSubmit').attr('disabled', 'disabled');
            }
            else {
              $('#reviewSubmit').removeAttr('disabled');
            }
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
        // hiding the modal
        hide: function(){
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
        }
    };

    // initialize the controller if the user is authenticated
    $(document).ready(function(){
        if(window.isLoggedIn) controller.init();
    });

})();
