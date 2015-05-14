$(document).ready(function() {

});


function pez_show_results(electName){

	console.log("get in pez_show_results");

	$("#pez_electName").html(electName);
	$("#pez_status").html(electName);

	// Set the main pie chart to the html content
	$('.pez_chartBlock').html('<canvas id="pez_relChart" width="120" height="120"></canvas>');

	var pieDataLabor = getPartyData(electName, 'Labor')['total']
	var pieDataLiberal = getPartyData(electName, 'Liberal')['total'];
	var pieDataGreens = getPartyData(electName, 'Greens')['total'];

	if (!(pieDataLabor==0 && pieDataLiberal==0 && pieDataGreens==0)) {
		var chartData = [
		{
			value: pieDataLabor,
			color: "#D119D1",
			highlight: "#E375E3", 
			label: "Labor"
		},
		{
			value: pieDataLiberal,
			color: "#1975D1",
			highlight: "#6685E0",
			label: "Liberal"
		},
		{
			value: pieDataGreens,
			color: "#2EB82E",
			highlight: "#5CD65C",
			label: "Greens"
		}
		// todo: add National Party
		]
	}
	else {
		var chartData = [
		{
			value: 1,
			color: '#DEDEDE',
			highlight: '#DEDEDE',
			label: "No Party Data"
		}]
	}
	
	var ctx = document.getElementById('pez_relChart').getContext('2d');
	// window.myPieChart = new Chart(ctx).Pie(chartData,{segmentShowStroke: true});
	window.myPieChart = new Chart(ctx).Pie(chartData);
	$('#dashboard').empty();
	$('.pez_chartholder').show();
	$(".pez_chartholder").unbind('click');
	$('.pez_chartholder').one("click", function(evt){
		// Clear container before adding new chart
		$('#dashboard').empty();
		$('.pez_chartholder').hide();

		var activePoints = myPieChart.getSegmentsAtEvent(evt);
		console.log("zoey");
		var sentiData = getDashBoardData(electName);
		dashBoard('#dashboard',sentiData);
		$('#dashboard').show();
	});  
	
}


function getPartyData(electName, partyName) {
	// console.log(electName);
	// console.log(partyName);

	var partyData = {};
	for (i in electData.counts) {
		elect = electData.counts[i].electorate;
		if (elect.name == electName) {
			for (party in elect.parties) {
				if (party == partyName) {
					partyData["total"] = elect.parties[party].total;
					partyData["pos"] = elect.parties[party].pos;
					partyData["neu"] = elect.parties[party].neu;
					partyData["neg"] = elect.parties[party].neg;
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
	console.log(GreensData);

	// var posTotal = {};
	// posTotal['Labor'] = LaborData['pos'];
	// posTotal['Liberal'] = LiberalData['pos'];
	// posTotal['Greens'] = GreensData['pos'];
	// var parties = {};
	// parties['parties'] = $.extend(true, {}, posTotal);

	// sentiData.push({"senti": 'Pos', 
	// 				"parties": $.extend(true, {}, parties)});

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




function pass_elect(electName){
	console.log(electName);

	$('.pez-deets-error').html('');

	// element: the information at the bottom
	$('#pez_lowerOverlay').fadeIn(500); 

	// element: the space holder of left before clicking on the map
	$('#pez_topOverlay').hide();

	// pez_show_results(get_election_index(elect));
	pez_show_results(electName); // For test: set up the name of an electorate
	
	// $("#elect_dropdown").get(0).selectedIndex = 0;
}
