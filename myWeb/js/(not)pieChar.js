$(document).ready(function() {

});


function pez_show_results(electName){

	console.log("get in pez_show_results");


	// Set the main pie chart to the html content
	$('.pez_chartBlock').html('<canvas id="pez_relChart" width="120" height="120"></canvas>');

	var chartDataLabor = getPartyTotal(electName, 'Labor');
	var chartDataLiberal = getPartyTotal(electName, 'Liberal');
	var chartDataGreens = getPartyTotal(electName, 'Greens');

	if (!(chartDataLabor==0 && chartDataLiberal==0 && chartDataGreens==0)) {
		var chartData = [
	    {
	        value: chartDataLabor,
	        color: "#FF3300",
	        highlight: "#FF704D", 
	        label: "Labor"
	    },
	    {
	        value: chartDataLiberal,
	        color: "#0033CC",
	        highlight: "#6685E0",
	        label: "Liberal"
	    },
	    {
	        value: chartDataGreens,
	        color: "#29A329",
	        highlight: "#87CB87",
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
	$('.pez_chartholder').show();
	
}


function getPartyTotal(electName, partyName) {
	// console.log(electName);
	// console.log(partyName);
	var partyTotal = 0;
	for (i in electData.counts) {
		elect = electData.counts[i].electorate;
		if (elect.name == electName) {
			for (party in elect.parties) {
				if (party == partyName) {
					partyTotal = elect.parties[party].total;
				}
			}
		}
	}
	return partyTotal;
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
