var airports = [];
var cities = [];
var states = [];
var countries = [];
//each airport was retrieved from the database via Flask and had its fields stored in hidden divs with the airport class
$('.airport').each(function(){
    let $newAirport = {};
    //$(x).eq(0) returns the jquery item at index 0. $(x)[0] would return it as an html element instead
    $newAirport['name'] = $(this).children('.airport-name').eq(0).html();
    $newAirport['city'] = $(this).children('.airport-city').eq(0).html();
    $newAirport['state'] = $(this).children('.airport-state').eq(0).html();
    $newAirport['country'] = $(this).children('.airport-country').eq(0).html();
    $newAirport['code'] = $(this).children('.airport-code').eq(0).html();
    airports.push($newAirport);

    if( ( $.inArray($newAirport['city'], cities) ) > -1){ //if city not already added to cities array
        cities.push($newAirport['city']);
    }
    if( ( $.inArray($newAirport['state'], states) ) > -1){
        cities.push($newAirport['state']);
    }
    if( ( $.inArray($newAirport['country'], countries) ) > -1){
        cities.push($newAirport['country']);
    }
});

$('#trip-origin-search').on('keyup paste', function(){
    $('#trip-origin-search').removeClass('autofilled has-us-state');
    var userInput = $(this).val(); //returns a String
    if(userInput.length === 0){
        hideSimilarAirports('origin');
    }
    else{
        var similarAirports = findAirports(userInput); //returns array of airport objects
        if(similarAirports.length > 0){
            displaySimilarAirports(similarAirports, 'origin');
        }
        else{
            hideSimilarAirports('origin');
        }
    }
});

$('#trip-destination-search').on('keyup paste', function(){
    $('#trip-destination-search').removeClass('autofilled has-us-state');
    var userInput = $(this).val(); //returns a String
    if(userInput.length === 0){ //no input
        hideSimilarAirports('destination');
    }
    else{
        if(equalsIgnoreCaseWithAccents(userInput, 'everywhere')){
            hideSimilarAirports('destination');
            destinationEverywhere(true);
        }
        else{
            var similarAirports = findAirports(userInput); //returns array of airport objects
            if(similarAirports.length > 0){
                displaySimilarAirports(similarAirports, 'destination');
                $('#dropdown-destination').append('<hr>');
                destinationEverywhere(false);
            }
            else{ //nothing matches the user's input
                hideSimilarAirports('destination');
                destinationEverywhere(true);
            }
        }
    }
});

function findAirports(query){
    let matches = [];
    matches = searchAirportBy('city', query, matches, 10 - matches.length);
    if(matches.length < 10 && query.length <= 3){
        matches = matches.concat(searchAirportBy('code', query, matches, 10)); //matches is array of airport objects
    }
    if(matches.length < 10){
        matches = matches.concat(searchAirportBy('name', query, matches, 10 - matches.length));
    }
    if(matches.length < 10){
        matches = matches.concat(searchAirportBy('country', query, matches, 10 - matches.length));
    }
    if(matches.length < 10){
        matches = matches.concat(searchAirportBy('state', query, matches, 10 - matches.length));
    }
    return matches;
}

function searchAirportBy(field, query, alreadyFound, howMany){
    var similar = [];
    var x;
    console.log(howMany);
    if(field==='code' || field==='name' || field==='city' || field==='country' || field==='state'){
        $.each( airports, function(idx, obj){
            if( equalsIgnoreCaseWithAccents( query, obj[field].substring(0, query.length) ) && !alreadyFound.includes(obj)){
                // console.log(obj[field].substring(0, query.length));
                // console.log(obj);
                similar.push(obj);
            }
            if(similar.length === howMany){
                return false; //this breaks the $.each loop
            }
        });
    }
    console.log(similar);
    return similar;
}

//hideSimilarAirports() hides the dropdown list of similar airports
function hideSimilarAirports(originOrDestination){
    if(originOrDestination === 'origin'){
        $('#dropdown-origin').empty();
        $('#dropdown-origin').css({
            display: "none"
        });
        $('#triangle-origin').css({
            display: "none"
        });
    }
    else if(originOrDestination === 'destination'){
        $('#dropdown-destination').empty();
        $('#dropdown-destination').css({
            display: "none"
        });
        $('#triangle-destination').css({
            display: "none"
        });
    }
    else if(originOrDestination === 'both'){
          $('#dropdown-origin').empty();
          $('#dropdown-origin').css({
              display: "none"
          });
          $('#triangle-origin').css({
              display: "none"
          });
          $('#dropdown-destination').empty();
          $('#dropdown-destination').css({
              display: "none"
          });
          $('#triangle-destination').css({
              display: "none"
          });
    }
}

function hasName(airport){
    return (airport['name'] != '' && airport['name'].toLowerCase() !== 'null' && airport['name'].toLowerCase() !== 'none')
}

function hasUSState(airport){
    return (airport['country'] === 'United States') && (airport['state'] != '' && airport['state'].toLowerCase() !== 'null' && airport['state'].toLowerCase() !== 'none');
}

function displaySimilarAirports(theseAirports, originOrDestination){
    var $newDiv0, $newDiv1, $newDiv2, $nameAndCode;
    var i = 0;
    if(originOrDestination === 'origin'){
        $('#dropdown-origin').empty(); //removes all child nodes
        $.each(theseAirports, function(idx, obj){
            if(i < 10){
                $newDiv0 = document.createElement("div");
                $($newDiv0).addClass("locations-origin");
                $($newDiv0).attr("id", "origin" + idx);
                if(idx === 0){
                    $($newDiv0).css({
                        borderTopLeftRadius: "2px",
                        borderTopRightRadius: "2px"
                    });
                }

                $newDiv1 = document.createElement("div");
                $($newDiv1).addClass("locations-main-info");
                $nameAndCode = obj['city'] + ', ';
                if(hasUSState(obj)){
                    $nameAndCode += obj['state'];
                }
                else{
                    $nameAndCode += obj['country'];
                }
                $nameAndCode += ' (' + obj['code'] + ')';
                $($newDiv1).html($nameAndCode);

                $newDiv2 = document.createElement("div");
                $($newDiv2).addClass("locations-name");
                if(hasName(obj)){
                    $($newDiv2).html(obj['name']);
                }
                else{
                    $($newDiv2).html(obj['city']);
                }

                $($newDiv0).append($newDiv1);
                $($newDiv0).append($newDiv2);

                $($newDiv0).click(function(){ //fills in this airport and hides the dropdown menu.
                    //$newDiv0 has one child with class '.locations-namecode' which contains the text we want to put into the input box
                    $('#trip-origin-search').val( $(this).children('.locations-main-info')[0].innerHTML );
                    $('#trip-origin-search').addClass('autofilled');
                    if(hasUSState(obj)){
                        $('#trip-origin-search').addClass('has-us-state');
                    }
                    hideSimilarAirports('origin');
                });

                if(idx !== 0){
                    $('#dropdown-origin').append('<hr>');
                }
                $('#dropdown-origin').append($newDiv0);

                ++i;
            }
        });
        $('#dropdown-origin').children().last().css({
            borderBottomLeftRadius: "2px",
            borderBottomRightRadius: "2px"
        });
        $('#dropdown-origin').css({
            display: "block"
        });
        $('#triangle-origin').css({
            display: "block"
        });
    }
    else if(originOrDestination === 'destination'){
        $('#dropdown-destination').empty(); //removes all child nodes
        $.each(theseAirports, function(idx, obj){
            if(i < 10){
                $newDiv0 = document.createElement("div");
                $($newDiv0).addClass("locations-destination");
                $($newDiv0).attr("id", "destination" + idx);
                if(idx === 0){
                    $($newDiv0).css({
                        borderTopLeftRadius: "2px",
                        borderTopRightRadius: "2px"
                    });
                }

                $newDiv1 = document.createElement("div");
                $($newDiv1).addClass("locations-main-info");
                $nameAndCode = obj['city'] + ', ';
                if(hasUSState(obj)){
                    $nameAndCode += obj['state'];
                }
                else{
                    $nameAndCode += obj['country'];
                }
                $nameAndCode += ' (' + obj['code'] + ')';
                $($newDiv1).html($nameAndCode);

                $newDiv2 = document.createElement("div");
                $($newDiv2).addClass("locations-name");
                if(hasName(obj)){
                    $($newDiv2).html(obj['name']);
                }
                else{
                    $($newDiv2).html(obj['city']);
                }

                $($newDiv0).append($newDiv1);
                $($newDiv0).append($newDiv2);

                $($newDiv0).click(function(){ //fills in this airport and hides the dropdown menu.
                    //$newDiv0 has one child with class '.locations-namecode' which contains the text we want to put into the input box
                    $('#trip-destination-search').val( $(this).children('.locations-main-info')[0].innerHTML );
                    $('#trip-destination-search').addClass('autofilled');
                    if(hasUSState(obj)){
                        $('#trip-destination-search').addClass('has-us-state');
                    }
                    $('#trip-destination-search')
                    hideSimilarAirports('destination');
                });

                if(idx !== 0){
                    $('#dropdown-destination').append('<hr>');
                }
                $('#dropdown-destination').append($newDiv0);

                ++i;
            }
        });

        $('#dropdown-destination').css({
            display: "block"
        });
        $('#triangle-destination').css({
            display: "block"
        });
    }
}

function destinationEverywhere(byItself){
    var $newDiv0 = document.createElement("div");
    $($newDiv0).addClass("locations-destination");
    $($newDiv0).attr("id", "everywhere");
    if(byItself){
        $($newDiv0).css({
            borderTopLeftRadius: "2px",
            borderTopRightRadius: "2px"
        });
    }
    $($newDiv0).css({
        borderBottomLeftRadius: "2px",
        borderBottomRightRadius: "2px"
    });

    $newDiv1 = document.createElement("div");
    $($newDiv1).addClass("locations-main-info");
    $($newDiv1).html("Can't decide where?");

    $newDiv2 = document.createElement("div");
    $($newDiv2).addClass("locations-name");
    $($newDiv2).html("Click here to search Everywhere ");

    $($newDiv0).append($newDiv1);
    $($newDiv0).append($newDiv2);

    $($newDiv0).click(function(){ //fills in this airport and hides the dropdown menu.
        //$newDiv0 has one child with class '.locations-namecode' which contains the text we want to put into the input box
        $('#trip-destination-search').val( 'Everywhere' );
        $('#trip-destination-search').addClass('autofilled');
        hideSimilarAirports('destination');
    });
    $('#dropdown-destination').append($newDiv0);
    $('#dropdown-destination').css({
        display: "block"
    });
    $('#triangle-destination').css({
        display: "block"
    });
}

function equalsIgnoreCaseWithAccents(a, b){
    // a.localeCompare(b, undefined, { sensitivity: 'accent' }) === 0, means a and b are the same ignoring case but differentiating on letters with accents (i.e. á).
    return (a.localeCompare(b, undefined, { sensitivity: 'accent' }) === 0);
}
