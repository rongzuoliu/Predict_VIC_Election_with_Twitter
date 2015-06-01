function getPartyTimeLine(party) {
    timeLines = electDataSumByTime["timeLines"];
    tl = [];

    total10 = 0;
    for (p in timeLines["2010"]) {
        total10 += timeLines["2010"][p]["total"];
    }
    total11 = 0;
    for (p in timeLines["2011"]) {
        total11 += timeLines["2011"][p]["total"];
    }
    total12 = 0;
    for (p in timeLines["2012"]) {
        total12 += timeLines["2012"][p]["total"];
    }
    total13 = 0;
    for (p in timeLines["2013"]) {
        total13 += timeLines["2013"][p]["total"];
    }
    total14 = 0;
    for (p in timeLines["2014"]) {
        total14 += timeLines["2014"][p]["total"];
    }
    
    // tl.push(timeLines["2010"][party]["pos"]/total10);
    // tl.push(timeLines["2011"][party]["pos"]/total11);
    // tl.push(timeLines["2012"][party]["pos"]/total12);
    // tl.push(timeLines["2013"][party]["pos"]/total13);   
    // tl.push(timeLines["2014"][party]["pos"]/total14); 

    // tl.push(timeLines["2010"][party]["neg"]/total10);
    // tl.push(timeLines["2011"][party]["neg"]/total11);
    // tl.push(timeLines["2012"][party]["neg"]/total12);
    // tl.push(timeLines["2013"][party]["neg"]/total13);   
    // tl.push(timeLines["2014"][party]["neg"]/total14); 

    tl.push(timeLines["2010"][party]["neg"]/timeLines["2010"][party]["total"]);
    tl.push(timeLines["2011"][party]["neg"]/timeLines["2011"][party]["total"]);
    tl.push(timeLines["2012"][party]["neg"]/timeLines["2012"][party]["total"]);
    tl.push(timeLines["2013"][party]["neg"]/timeLines["2013"][party]["total"]);   
    tl.push(timeLines["2014"][party]["neg"]/timeLines["2014"][party]["total"]); 
    console.log(tl);
    return tl;
}

function getLineChartData() {
    // throw('zoey');

    var dataLabor = getPartyTimeLine("Labor");
    var dataLiberal = getPartyTimeLine("Liberal");
    var dataGreens = getPartyTimeLine("Greens");
    var dataNationals = getPartyTimeLine("Nationals");

    var lineChartData = {
        labels: ["2011", "2012", "2013", "2014"],
        datasets: [
            {
                label: "Labor",
                fillColor: "rgba(209,25,209,0.2)", // rgba format of #D119D1
                strokeColor: "#D119D1",
                pointColor: "rgba(209,25,209,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(209,25,209,1)",
                data: dataLabor
            },
            {
                label: "Liberal/Nationals",
                fillColor: "rgba(25,117,209,0.2)",
                strokeColor: "#1975D1",
                pointColor: "rgba(25,117,209,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(25,117,209,1)",
                data: dataLiberal
            },
            {
                label: "Greens",
                fillColor: "rgba(46,184,46,0.2)",
                strokeColor: "#2EB82E",
                pointColor: "rgba(46,184,46,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(46,184,46,1)",
                data: dataGreens
            },
            {
                label: "Nationals",
                fillColor: "rgba(255,255,77,0.2)",
                strokeColor: "#FFFF4D",
                pointColor: "rgba(255,255,77,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(255,255,77,1)",
                data: dataNationals            },

        ]
    };
    return lineChartData;
}


function showTimeLine() {
	$('.resultsByTime').html('<canvas class="lineChart" id="timeLine" width="420" height="320"></canvas>');
    var lineChart = document.getElementById('timeLine').getContext('2d');
    window.lineChart = new Chart(lineChart).Line(getLineChartData());
    $('.resultsByTime').show();

}
