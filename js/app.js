$( document ).ready(function() {
    showResults();
    showTimeLine();
    showMap();
});


function showResults() {
    var rowCount = 1;
    // Add the first row of results_sum
    $('.resultsSum').html('<div class="row topRow">'
                            +'<div class="col">Party</div>'
                            +'<div class="col">Pos Count</div>'
                            +'<div class="col">Pos %</div>'
                            +'<div class="col">Neu Count</div>'
                            +'<div class="col">Neu %</div>'
                            +'<div class="col">Neg Count</div>'
                            +'<div class="col">Neg %</div>'
                            +'<div class="col">Total</div>'
                        +'</div>');
    for (p in totalDataRates['parties']) {
        partyName = p
        dataSum = totalDataRates['parties'][p];
        var rowString = '';
        rowString += '<div class="row '+partyName+'">' 
        rowString += '<div class="col">'+partyName+'</div>';
        rowString += '<div class="col">'+dataSum.total_pos+'</div>';
        rowString += '<div class="col">'+(dataSum.pos_rate*100).toFixed(2)+'%</div>';
        rowString += '<div class="col">'+dataSum.total_neu+'</div>';
        rowString += '<div class="col">'+(dataSum.neu_rate*100).toFixed(2)+'%</div>';
        rowString += '<div class="col">'+dataSum.total_neg+'</div>';
        rowString += '<div class="col">'+(dataSum.neg_rate*100).toFixed(2)+'%</div>';
        rowString += '<div class="col">'+dataSum.total+'</div>';
        rowString += '</div>';
        $('.resultsSum').append(rowString);
    }
    $('#resultSum').append(rowString);
    $('#resultsSum').show();
}





    








