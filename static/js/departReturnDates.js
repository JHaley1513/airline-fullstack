var $today = new Date();
$lastReturnDate = "XX/XX/XX";

$(document).ready(function(){
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

for(let i=0; i<42; i++){
    $newDate = $('<div></div>');
    $($newDate).html(   );
    $newDate.click(function(){
        dateSelected( $($newDate).html() );
    });
    $('#calendar').append
}

function dateSelected($dayNum){
    
    month = 'none';
    year = 'none';
}



function showDepartCalendar(){

}

function showReturnCalendar(){

}
