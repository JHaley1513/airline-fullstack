$defaultBorder = "1px solid gray";
$locationsWidth = 400;

var $today = new Date();
$lastReturnDate = "XX/XX/XX";

$(document).ready(function(){
    for(let i=0; i<50; i++){
        addLines();
    }

    updateContainer();
    $(window).resize(updateContainer)

    $('input[type=radio][name=trip-type]').change(function(){
        if(this.value === "oneway"){
            $('#return button').html("(One way)");
            $('#return, #return button').css({
                color: "gray"
            });
        }
        else if(this.value === "roundtrip"){
            $('#return button').html($lastReturnDate);
            $('#return, #return button').css({
                color: "black"
            });
        }
    });

    var $twoWksFromNow = todayPlusDays(14);
    var $threeWksFromNow = todayPlusDays(21);

    $('#depart button').html($twoWksFromNow);
    $('#return button').html($threeWksFromNow);
    $lastReturnDate = $threeWksFromNow;
});

function todayPlusDays($numDays){
    $newDate = new Date();
    $newDate.setDate($today.getDate()+$numDays);

    return ('0' + ($newDate.getMonth()+1)).slice(-2) + "/" + ('0' + $newDate.getDate()).slice(-2) + "/" + $newDate.getFullYear().toString().substr(2,2);
}

function addLines(){
    $('body').append('<div>...</div>');
}

function updateContainer(){
    var $windowWidth = $(window).width();
    updateMargins($windowWidth);
    updateBackgroundImage($windowWidth);
    updateInputs($windowWidth);
    if($windowWidth > 1128){
        $pageMargin = (($windowWidth - 1128)/2) + "px";
        $('#body-container').css({
            marginLeft: $pageMargin,
            marginRight: $pageMargin
        });
    }
    else{
        $('#body-container').css({
            marginLeft: 0,
            marginRight: 0
        });
        if($windowWidth > 788){ //same as above but without margin

        }
        else if($windowWidth > 730){ //two lines now instead of one

        }
        else if($windowWidth > 500){ //same as above but without background image and big text

        }
        else{ //four lines
            $('.flight-search').css({
                // height:
            });
        }
    }
}

function updateMargins($windowWidth){
    if($windowWidth > 1128){
        $newMargin = (($windowWidth - 1128)/2) + "px";
        $('#body-container').css({
            marginLeft: $newMargin,
            marginRight: $newMargin
        });
    }
    else{
        $('#body-container').css({
            marginLeft: 0,
            marginRight: 0
        });
    }
}

function updateBackgroundImage($windowWidth){
    if($windowWidth > 730){
        //show
    }
    else{
        //hide
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
