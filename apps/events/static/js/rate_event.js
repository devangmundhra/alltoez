var rating = {
    value: 0,
    comment: ''
};

var controller = {
    init: function(){
        popoverView.init();
        modalView.init();
    },
    getRatingValue: function(){
        return rating.value;
    },
    setRatingValue: function(value){
        rating.value = value;
    },
    renderModalView: function(value){
        modalView.render();
    }
};

var popoverView = {
    elem: $('#done-action'),
    show: false,
    init: function(){
        var self = this;

        // initializing popover
        this.elem.popover({
            position: 'left',
            container: 'body',
            content: '<span class="rateit"></span>',
            html: true,
            show: false
        });

        // adding event listeners for showing popover
        this.elem.mouseenter(function(){
            if(!self.show) self.render();
        });

        // adding event listeners for hiding popover 
        // (Esc button, and click outside the popover and the button)
        $(document).keyup(function (event) {
            if (event.which === 27) {
                self.hide();
            }
        });
        $('body').click(function(event){
            if(event.target.className.indexOf('popover') < 0 &&
              event.target.id !== 'done-action'){
                self.hide();
            }
        });
    },
    render: function(){
        var self = this;
        this.elem.popover('show');

        // initializing rating stars
        var rateitElem = $('.rateit');
        rateitElem.rateit({
            resetable: false
        });

        // getting a rating value
        var value = controller.getRatingValue();

        // setting the rating value
        rateitElem.rateit('value', value);

        // setting an event listener for 'rated' event
        rateitElem.bind('rated', function(){
            var value = $(this).rateit('value');
            controller.setRatingValue(value);
            controller.renderModalView();
            self.hide();
        });
        this.show = true;
    },
    hide: function(){
        this.elem.popover('hide');
        this.show = false;
    }
};

var modalView = {
    elem: $('#modalRating'),
    init: function(){

        // initializing modal 
        this.elem.modal({
            keyboard: true,
            show: false
        });
    },
    render: function(){
        // getting the rating value
        var value = controller.getRatingValue();

        this.elem.modal('show');
        
        // initializing rating stars
        var rateitElem = $('#modalRate');
        rateitElem.rateit({
            resetable: false
        });

        // updating the rating value in the view
        rateitElem.rateit('value', value);
        
        // setting an event listener for 'rated' event
        // (updating the rating value)
        rateitElem.bind('rated', function(){
            var value = $(this).rateit('value');
            controller.setRatingValue(value);
        });
    },
    hide: function(){
        this.elem.modal('hide');
    }
};

window.onload = function(){
    controller.init();
};
