
function passElect(electName){
	console.log(electName);
	// element: the information at the bottom
	$('#lowerOverlay').fadeIn(500); 
	// element: the space holder of left before clicking on the map
	$('#topOverlay').hide();
	// showPie(get_election_index(elect));
	showPie(electName); // For test: set up the name of an electorate
	
}

function showPie(electName){
	console.log("get in showPie");
	$("#electName").html(electName);
	$("#status").html('Predicted Results VS Actual Results');
	// Set the main pie chart to the html content
	$('.chartBlock').html('<canvas class="relChart" id="predictedPie" width="120" height="120"></canvas><canvas class="relChart" id="resultPie" width="120" height="120"></canvas>');
	var predictedPieData = getPredictedPieData(electName);
	var resultPieData = getResultPieData(electName);	
	var predictedPie = document.getElementById('predictedPie').getContext('2d');
	var resultPie = document.getElementById('resultPie').getContext('2d');
	window.resultPieChart = new Chart(resultPie).Pie(resultPieData);
	window.predictedPieChart = new Chart(predictedPie).Pie(predictedPieData);

	$('#dashboard').empty();
	$('.chartBlock').show();
	$(".chartBlock").unbind('click');
	$('.chartBlock').one("click", function(evt){
		// Clear container before adding new chart
		$('#dashboard').empty();
		$('.chartBlock').hide();
		var activePoints = predictedPieChart.getSegmentsAtEvent(evt);
		console.log("click on pie chart");
		var sentiData = getDashBoardData(electName);
		dashBoard('#dashboard',sentiData);
		$('#dashboard').show();
	});  	
}


function getPredictedPieData(electName) {
	var pieDataLabor = getPartyData(electName, 'Labor')['total']
	var pieDataLiberal = getPartyData(electName, 'Liberal')['total'];
	var pieDataGreens = getPartyData(electName, 'Greens')['total'];
	var pieDataNationals = getPartyData(electName, 'Nationals')['total'];
	if (!(pieDataLabor==0 && pieDataLiberal==0 && pieDataGreens==0 && pieDataNationals==0)) {
		var chartData = [{
			value: pieDataLabor,
			color: "#D119D1",
			highlight: "#E375E3", 
			label: "Labor"
		},{
			value: pieDataLiberal,
			color: "#1975D1",
			highlight: "#6685E0",
			label: "Liberal"
		},{
			value: pieDataGreens,
			color: "#2EB82E",
			highlight: "#5CD65C",
			label: "Greens"
		},{
			value: pieDataNationals,
			color: "#FFFF4D",
			highlight: "#FFFF99",
			label: "Nationals"
		}];
		return chartData;
	}
	else {
		var chartData = [{
			value: 1,
			color: '#DEDEDE',
			highlight: '#DEDEDE',
			label: "No Party Data"
		}];
		return chartData;
	}
}

function getResultPieData(electName) {
	var pieDataLabor = 0;
	var pieDataLiberal = 0;
	var pieDataGreens = 0;
	var pieDataNationals = 0;
	for (i in electResults) {
		if (electResults[i].name == electName) {
			parties = electResults[i].candidate;
			for (p in parties) {
				partyName = parties[p].candParty;
				console.log(partyName);
				if (partyName == "ALP") {
					pieDataLabor = parties[p].candCount;
					console.log(pieDataLabor);
				}
				else if (partyName == "LP"){
					pieDataLiberal = parties[p].candCount;
					console.log(pieDataLiberal);
				}
				else if (partyName == "GRN"){
					pieDataGreens = parties[p].candCount;
					console.log(pieDataGreens);
				}
				else if (partyName == "NP"){
					pieDataNationals = parties[p].candCount;
					console.log(pieDataNationals);
				}
			}
		}
	}

	if (!(pieDataLabor==0 && pieDataLiberal==0 && pieDataGreens==0 && pieDataNationals==0)) {
		var chartData = [{
			value: pieDataLabor/10,
			color: "#D119D1",
			highlight: "#E375E3", 
			label: "Labor"
		},{
			value: pieDataLiberal/10,
			color: "#1975D1",
			highlight: "#6685E0",
			label: "Liberal"
		},{
			value: pieDataGreens/10,
			color: "#2EB82E",
			highlight: "#5CD65C",
			label: "Greens"
		},{
			value: pieDataNationals/10,
			color: "#FFFF4D",
			highlight: "#FFFF99",
			label: "Nationals"
		}];
		return chartData;
		console.log(chartData);
	}
	else {
		var chartData = [{
			value: 1,
			color: '#DEDEDE',
			highlight: '#DEDEDE',
			label: "No Party Data"
		}];
		return chartData;
	}
}



function getPartyData(electName, partyName) {
	// console.log(electName);
	// console.log(partyName);
	var partyData = {};
	for (elect in electDataCounts.counts) {
		if (elect == electName) {
			parties = electDataCounts.counts[elect]
			for (party in parties) {
				if (party == partyName) {
					partyData["total"] = parties[party].total;
					partyData["pos"] = parties[party].pos;
					partyData["neu"] = parties[party].neu;
					partyData["neg"] = parties[party].neg;
				}
			}
		}
	}
	return partyData;
}


function getDashBoardData(electName) {
	var sentiData = [];
	var LaborData = getPartyData(electName, 'Labor');
	var LiberalData = getPartyData(electName, 'Liberal');
	var GreensData = getPartyData(electName, 'Greens');
	sentiData.push({"senti": 'Pos', 
					"parties": 
						{"Labor": LaborData['pos'], "Liberal": LiberalData['pos'], "Greens": GreensData['pos']}
				});
	sentiData.push({"senti": 'Neg', 
				"parties": 
					{"Labor": LaborData['neg'], "Liberal": LiberalData['neg'], "Greens": GreensData['neg']}
				});
	sentiData.push({"senti": 'Neu', 
			"parties": 
				{"Labor": LaborData['neu'], "Liberal": LiberalData['neu'], "Greens": GreensData['neu']}
				});
	console.log(sentiData);
	return sentiData
}




