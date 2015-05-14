// JavaScript Document
var addNumber;
var addStreet;
var addBurb;
var mattersTitle = 'YES! Your vote matters!';
var mattersBlurb = '';
var oldAddress;
var newAddress;
var promiseArray = new Array();
var dropStr;
var swingParty;



$(document).ready(function() {
	$('.pez_topStat').hide();
	$('#pez_nats').hide();


	// Dropdown Menu:

	// for(i=0;i<electorateArray.length;i++){
	// 	$('#elect_dropdown').append('<option>'+electorateArray[i]+'</option>');
	// }
	//
	// $('#elect_dropdown').change(function () {
	//     dropStr = "";
	//     $( "#elect_dropdown option:selected" ).each(function(index, val) {
	//     	 dropStr += $( this ).text();
	//     });
	//     //console.log(dropStr);
	//     if(dropStr.indexOf("Select your electorate")<0){
	//     	$('.pez-deets-error').html('');
	//     	$('#pez_lowerOverlay').fadeIn(500);
	// 		$('#pez_topOverlay').fadeIn(500, function(){
	// 			pez_show_results(get_election_index(dropStr));
	// 		});
	//     }
	// });

	/*	Submit mobile form 
		Gather info from the 1 field, validates and submits
	// */
	// $('#pez_mobile_submit_btn').click(function(event) {
	// 	newAddress = $('#pez_mobile_address').find('input').val();
		
	// 	//Start form validation
	// 	var formValidated = true;
	// 	if(newAddress=='' || newAddress==' '){
	// 		formValidated = false;
	// 		$('#pez_mobile_address').css('background-color', '#FF556F');
	// 	}
	// 	//End form validation

	// 	if(formValidated){
	// 		$('.pez-deets-error').html('');
	// 		$('#pez_mobile_address').css('background-color', '#FFF');

	// 		//Only submit form if address is NEW
	// 		if(oldAddress != newAddress){
	// 			oldAddress = newAddress;
	// 			$('#pez_lowerOverlay').fadeIn(500);
	// 			$('#pez_topOverlay').fadeIn(500, function(){
	// 				codeAddress();
	// 			});
	// 			console.log('wot?');
	// 		}
	// 	}else{
	// 		$('.pez-deets-error').html('Please enter a valid address.');
	// 	}
	// });

});



function codeAddress() {
	//console.log(newAddress);
	var geocoder = new google.maps.Geocoder();
	geocoder.geocode( { 'address': newAddress}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			var marker = new google.maps.Marker({
				position: results[0].geometry.location,
				lat: results[0].geometry.location.k,
				lon: results[0].geometry.location.B,
				latlon: [results[0].geometry.location.k,results[0].geometry.location.B]
			});
			p = marker.latlon;
			//console.log('p: '+p);
			passCoordinates(p);		
		} else {
			$('.pez-preloader').fadeOut();
			$('.pez-deets-error').html('Could not find electorate');
		}
	});
}

//Start Marc magic//
function passCoordinates(j) {
	queue()
	.defer(d3.csv,"data/lowerHouseCandidates.csv")
	.await(ready);		
	function ready(error, i,l){	
		$.ajax({
			type: 'post',
			url: 'http://origin-interactives.stuff.co.nz/geo/test.php',
			data: {
				source1: j[0],
				source2: j[1],
			},
			success: function( data ) {
				info = data.split(',');
				//console.log(data);
				newStats = {}
				
				for(j in l){
					if(l[j].electorate == info[4]){
						newStats = l[j];
					}
				}
				format = d3.format(".3n");
				format = d3.format(".3n");
				var electorate = info[4];
				pez_show_results(get_election_index(electorate));
			}
		});
	}
}

function pez_show_results(thisElect){
	$('.pez_topStat').show();
	// $('.pez_overlayText').hide();

	var goodData = true;
	//swingNeeded":"8.69 - % To LP"
	var swingNeededVar = electionData.electorate[thisElect].swingNeeded;
	swingNeededVar = swingNeededVar.split(' - % To ');
	var pez_swingNeeded = swingNeededVar[0];
	var swingParty = swingNeededVar[1];
	var pez_Name = electionData.electorate[thisElect].name;
	var pez_Enroll= electionData.electorate[thisElect].enrolled;
	var pez_PcCounted= electionData.electorate[thisElect].countedPercent;
	var pez_Swing= electionData.electorate[thisElect].swing;
	var pez_candName = '';

	if(currentPartyArray[thisElect][2]!='null')  pez_candName = currentPartyArray[thisElect][2]+', '
	var pez_heldby = pez_candName+currentPartyArray[thisElect][1];
	

	
	//fill data//////////////////////////////

	//top data
	$("#pez_electName").html(pez_Name);
	$('#pez_heldby').html(pez_heldby);
	$("#pez_enrolled").html(pez_Enroll);
	$("#pez_counted").html(pez_PcCounted+ "%");



	//candidates data in the information of the bottom 
	var pezCandiList = electionData.electorate[thisElect].candidate;
	var pezCandiNum = electionData.electorate[thisElect].candidate.length;
	var pezOrderedArray = new Array();
	for(j in pezCandiList){
		pezOrderedArray.push([pezCandiList[j].candName,pezCandiList[j].candParty,pezCandiList[j].candCount, pezCandiList[j].candPercent]);
	}
	
	pezOrderedArray.sort((function(index){
		return function(a, b){
			return (b[index] === a[index] ? 0 : (b[index] < a[index] ? -1 : 1));
		};
	})(3)); // 2 is the index
	//console.log(pezOrderedArray);
	var rowCount = 1;
	$('.pez_candiTable').html('<div class="pez_row pez_topRow"><div class="pez_col pez_nameCol">Candidate</div><div class="pez_col">Party</div><div class="pez_col">Count</div><div class="pez_col">%</div></div>');
	for(j in pezOrderedArray){
		rowCount++;
		var className = '';
		if(!isEven(rowCount)) className = 'pez_greyRow';
		var rowString = '';
		rowString += '<div class="pez_row '+className+'">';
		rowString += '<div class="pez_col pez_nameCol">'+pezOrderedArray[j][0]+'</div>';
		rowString += '<div class="pez_col">'+pezOrderedArray[j][1]+'</div>';
		rowString += '<div class="pez_col">'+pezOrderedArray[j][2]+'</div>';
		var percentString = pezOrderedArray[j][3];
		if(percentString == 'NaN%'){
			percentString = '-';
			goodData = false;
		}
		rowString += '<div class="pez_col">'+percentString+'</div>';
		rowString += '</div>';
		$('.pez_candiTable').append(rowString);
	}
	
	$('#pez_smallSwing').html('Margin:');
	$("#pez_swing").html(electionData.electorate[thisElect].swing+"%");
	$('#pez_smallSwingNeeded').html('Swing<br>to<br>'+swingParty+':')
	$("#pez_swingNeeded").html(pez_swingNeeded+"%");

	$('#pez_marginCircle').css('background-color',get_party_col(currentPartyArray[thisElect][1]));
	$('#pez_swingCircle').css('background-color',get_party_col(swingParty));
	
	//decided
	var pez_callIt = electionData.electorate[thisElect].status;
	
	switch(pez_callIt){
		case "Labor retains": case "Labor gains": case "Labor gain": case "Labor retain":
			$("#pez_status").css('background-color','#B30104');
		break;
		case "Liberals retain": case "Liberals gain":
			$("#pez_status").css('background-color','#0252AD');
		break;
		case "Greens gain": case "Greens retain":  case "Greens retains":
			$("#pez_status").css('background-color','#1D8601');
		break;
		case "Nationals gain": case "Nationals retain":  case "Nationals retains":
			$("#pez_status").css('background-color','#eeba05');
		break;
		default:
			$("#pez_status").css('background-color','#999');
		break
	}
	$("#pez_dec").html(electionData.electorate[thisElect].status);
	

	if(goodData){
		var firstPartyCol = get_party_col(electionData.electorate[thisElect].twoCandPrefOne.tcpOneParty);
		var secondPartyCol = get_party_col(electionData.electorate[thisElect].twoCandPrefTwo.tcpTwoParty); 
		var chartData = [{
			value: parseInt(electionData.electorate[thisElect].twoCandPrefOne.tcpOneCount),
			color: firstPartyCol,
			highlight: "#f2f2f2",
			label: electionData.electorate[thisElect].twoCandPrefOne.tcpOneParty
		},
		{
			value: parseInt(electionData.electorate[thisElect].twoCandPrefTwo.tcpTwoCount),
			color: secondPartyCol,
			highlight: "#f2f2f2",
			label: electionData.electorate[thisElect].twoCandPrefTwo.tcpTwoParty
		}]






		
		// Main Pie chart:   

		//console.log(chartData);
		$('#pez_chart_legend').html("");

		// Just the text placeholders of two circles
		$('#pez_chart_legend').append("<li style='color:"+firstPartyCol+"'>"+electionData.electorate[thisElect].twoCandPrefOne.tcpOneName+" - "+electionData.electorate[thisElect].twoCandPrefOne.tcpOneParty+" "+electionData.electorate[thisElect].twoCandPrefOne.tcpOnePercent+"%"+"</li>");
		$('#pez_chart_legend').append("<li style='color:"+secondPartyCol+"'>"+electionData.electorate[thisElect].twoCandPrefTwo.tcpTwoName+" - "+electionData.electorate[thisElect].twoCandPrefTwo.tcpTwoParty+" "+electionData.electorate[thisElect].twoCandPrefTwo.tcpTwoPercent+"%"+"</li>");

		// Set the main pie chart to the html content
		$('.pez_chartBlock').html('<canvas id="pez_relChart" width="120" height="120"></canvas>');


		var ctx = document.getElementById('pez_relChart').getContext('2d');
		window.myPieChart = new Chart(ctx).Pie(chartData,{segmentShowStroke: true});





		   
		$('.pez_chartholder').show();
		// Two circles before the pie chart:
		$('.pez_circleholder').show();
	}

	else{
		$('.pez_chartholder').hide();
		// Two circles before the pie chart:
		$('.pez_circleholder').hide();
	}

	$('#pez_lowerOverlay').fadeOut(500);
	$('#pez_topOverlay').fadeOut(500);
	$('.pez-preloader').fadeOut(500);
}

function get_election_index(eName){
	return electorateArray.indexOf(eName);
}

function isEven(value) {
	if (value%2 == 0)
		return true;
	else
		return false;
}

function load_data_csv(){
	$.ajax({
		
		type: "GET",
		url: csvPath,
		dataType: "text",
		success: function(csv) {
			promiseArray = $.csv.toArrays(csv);
			$('.pez-detail-holder').fadeIn();
		}
	});
}

function get_party_col(name){
	var col = '#7B7E6B';
	switch(name){
		case 'GRN': case 'Greens':
		col = '#0ab751';
		break;
		case 'ALP': case 'Labor':
		col = '#d21034';
		break;
		case 'LP': case 'Liberal':
		col = '#006fba';
		break;
		case 'NP': case 'Nationals':
		col = '#eeba05';
		break;

	}
	return col;
}

function pass_elect(elect){
	$('.pez-deets-error').html('');

	// element: the information at the bottom
	$('#pez_lowerOverlay').fadeIn(500); 

	// element: the space holder of left before clicking on the map
	$('#pez_topOverlay').fadeIn(500, function(){ 
		pez_show_results(get_election_index(elect));
	});

	// $("#elect_dropdown").get(0).selectedIndex = 0;
}