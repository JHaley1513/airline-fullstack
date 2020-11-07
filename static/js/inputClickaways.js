$('body').click(function(event){
    var clickedElement = 'none';
    var triangle = 'none';
    var $target = $( event.target );
    // if($target.is('#dropdown-origin')){
    //     clickedElement = '#dropdown-origin';
    // }
    // else if($target.is('#dropdown-destination')){
    //     clickedElement = '#dropdown-destination';
    // }
    // else if($target.is('#calendar')){
    //     clickedElement = '#calendar';
    // }
    // else if($target.is('#dropdown-class-travelers')){
    //     clickedElement = '#dropdown-class-travelers';
    // }

    if($target.is('#calendar')){
        clickedElement = '#calendar';
        if($('#depart-or-return').hasClass('depart')){
            triangle = '#triangle-depart-date';
        }
        else if($('#depart-or-return').hasClass('return')){
            triangle = '#triangle-return-date';
        }
    }
    else if($target.is('#dropdown-class-travelers')){
        clickedElement = '#dropdown-class-travelers';
        triangle = '#triangle-class-travelers';
    }

    $('.dropdown').css({
        display: 'none'
    });
    $('.triangle-up').css({
        display: 'none'
    });
    if(clickedElement !== 'none'){
        $(clickedElement).css({
            display: 'block'
        });
        $(triangle).css({
            display: 'block'
        });
    }
});
