$defaultBorder = "1px solid gray";
$locationsWidth = 400;

$(document).ready(function(){
    for(let i=0; i<50; i++){
        addLines();
    }

    updateContainer();
    $(window).resize(updateContainer)
});

function addLines(){
    $('.page-content').append('<div>...</div>');
}

function updateContainer(){
    var $windowWidth = $(window).width();
    updateMargins($windowWidth);
    updateBackgroundImage($windowWidth);
    updateInputs($windowWidth);
    updateTriangles();
    if($windowWidth > 1128){
        $pageMargin = (($windowWidth - 1128)/2) + "px";
        setMargins($pageMargin);
    }
    else{
        setMargins(0);
        if($windowWidth > 788){ //same as above but without margin

        }
        else if($windowWidth > 730){ //two lines now instead of one

        }
        else if($windowWidth > 500){ //same as above but without background image and big text

        }
        else{ //four lines
            $('#flight-search').css({
                // height:
            });
        }
    }
}

function updateMargins($windowWidth){
    if($windowWidth > 1128){
        $newMargin = (($windowWidth - 1128)/2) + "px";
        setMargins($newMargin);
    }
    else{
        setMargins(0);
    }
}

function setMargins($margin){
    $('#header-flexwrapper').css({
        paddingLeft: $margin,
        paddingRight: $margin
    });
    $('#flight-search').css({
        marginLeft: $margin,
        marginRight: $margin
    });
}

function updateBackgroundImage($windowWidth){
    if($windowWidth > 730){
        //show
        $('.page-content').removeClass('page-hide-bg');
    }
    else{
        //hide
        $('.page-content').addClass('page-hide-bg');
    }
}

function updateInputs($windowWidth){
    if(475 > $windowWidth && $windowWidth > 458){
        $('#locations').css({
            width: $locationsWidth + 10 + "px"
        });
    }
    else{
        $('#locations').css({
            width: $locationsWidth + "px"
        });
    }

    if($windowWidth > 865){ //all inputs connected on one line.
        //make combined corners lighter
        $('#location-from input, #location-to input, #depart button, #return button').css({
            borderRight: "none"
        });
        //rounded corners
        $('#location-from input').css({ //round left corners
            borderRadius: "3px 0 0 3px" //top l, top r, bot r, bot l
        });
        $('#travelers button').css({ //round right corners
            borderRadius: "0 3px 3px 0"
        });
        $('#location-to input, #depart button, #return button').css({
            borderRadius: "0"
        });

        //spacing between depart/return/travelers
        $('#location-from, #depart, #return').css({
            marginRight: "0"
        });
        $('#location-to, #travelers').css({
            marginLeft: "0"
        });
    }
    else if($windowWidth > 475){ //two lines
        $('#location-from input, #location-to input, #depart button, #return button').css({
            borderRight: $defaultBorder
        });

        $('#location-from input, #location-to input, #depart button, #return button, #travelers button').css({
            borderRadius: "3px"
        });

        $('#location-from, #depart, #return').css({
            marginRight: "5px"
        });
        $('#location-to, #travelers').css({
            marginLeft: "5px"
        });
    }
    else{ //four lines
        $('#location-from input, #location-to input, #depart button, #return button').css({
            borderRight: $defaultBorder
        });

        $('#location-from input, #location-to input, #depart button, #return button, #travelers button').css({
            borderRadius: "3px"
        });

        $('#depart').css({
            marginRight: "10px"
        });
        $('#location-from, #return').css({
            marginRight: "0"
        });
        $('#location-to, #travelers').css({
            marginLeft: "0"
        });
    }
}

function updateTriangles(){
    var triangleSize = 12;
    $('#triangle-origin').css({
        marginLeft: (halfOfDivWidth('#location-from') - triangleSize).toFixed(2) + "px" //x.toFixed(y) converts x to string with y decimal places
    });
    $('#triangle-destination').css({
        marginLeft: (halfOfDivWidth('#location-to') - triangleSize).toFixed(2) + "px"
    });
    $('#triangle-depart-date').css({
        marginLeft: (halfOfDivWidth('#depart-datepicker-button') - triangleSize).toFixed(2) + "px"
    });
    $('#triangle-return-date').css({
        marginLeft: (halfOfDivWidth('#return-datepicker-button') - triangleSize).toFixed(2) + "px"
    });
    $('#triangle-class-travelers').css({
        marginLeft: (halfOfDivWidth('#class-travelers-trigger') - triangleSize).toFixed(2) + "px"
    });
}

function halfOfDivWidth(divId){
    return parseFloat( $(divId).css('width').substring( 0, $(divId).css('width').length-2 ) ) / 2;
}
