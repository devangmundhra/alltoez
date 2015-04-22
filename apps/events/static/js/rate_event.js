var rating = {
    value: 0,
    comment: ''
};

var controller = {
    init: function(){
        popoverView.init();
        modalView.init();
    },
    initialRatingSelected: function(value){
        rating.value = value;
        modalView.updateStars();
        modalView.render();
    },
    getRatingValue: function(){
        return rating.value;
    },
    renderModalView: function(){
    }
};

var popoverView = {
    elem: $('#done-action'),
    init: function(){
        var self = this;
        $('#input-id').rating();
        var ratingHTML = $('#input-id')[0].outerHTML;
        //initialize the popover
        //var ratingHTML = $('#starRating')[0].outerHTML;
        this.elem.popover({
            content: ratingHTML,
            html: true
        });

        //bind events
        this.elem.mouseenter(function(){
            self.popover();
        });
        $('body').on('click', '.rating', function(e){
            self.initialRatingSelected(e);
        });
    },
    popover: function(){
        this.elem.popover('show');
    },
    initialRatingSelected: function(e){
        var value = $(e.target).val();
        controller.initialRatingSelected(value);
        this.hide();
    },
    hide: function(){
        this.elem.popover('hide');
    }
};

var modalView = {
    elem: $('#modalRating'),
    init: function(){
        this.elem.modal({
            keyboard: true,
            show: false
        });
    },
    render: function(value){
        this.elem.modal('show');
    },
    hide: function(){
        this.elem.modal('hide');
    },
    updateStars: function(){
        var value = controller.getRatingValue();
        console.log(value);
        if(value){
            this.elem.find('input[type=radio][value=' + value + ']').attr('checked', true);
            console.log(1);
        } else {
            this.elem.find('input[type=radio]').attr('checked', false);
        }
    }
};

window.onload = function(){
    controller.init();
};
