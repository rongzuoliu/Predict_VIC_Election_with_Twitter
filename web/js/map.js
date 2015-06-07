var info = L.control();
var legend = L.control({position: 'bottomright'});

var ALP = 0;
var LP = 0;
var GRN = 0;
var NP = 0;
function showMap() {
    // Set up an original map
    L.mapbox.accessToken = 'pk.eyJ1Ijoicm9uZ3p1b2wiLCJhIjoiM09xSU1TZyJ9.yB_yO1xg4PzZ2h7LrY53Zw';
    // Replace 'examples.map-i87786ca' with your map id: rongzuol.f5f6a9f0
    var mapboxTiles = L.tileLayer('https://{s}.tiles.mapbox.com/v4/rongzuol.f5f6a9f0/{z}/{x}/{y}.png?access_token=' + L.mapbox.accessToken, {
        attribution: '<a href="http://www.mapbox.com/about/maps/" target="_blank">Terms &amp; Feedback</a>'
        }
    );
    map = L.map('map')
        .addLayer(mapboxTiles)
        .setView([-37.8455171,144.9609444], 7);
        addGeoToMap(map);
    
    info.addTo(map);
    legend.addTo(map);
    // console.log("ALP: " + ALP);
    // console.log("LP: " + LP);
    // console.log("GRN: " + GRN);
    // console.log("NP: " + NP);
}

function addGeoToMap(map) {
    geojson = L.geoJson(electInfo, {
        onEachFeature: onEachFeature,
        style: style
    }).addTo(map);
}

function style(feature) {
    return {
        fillColor: getColor(getElect(feature.properties.Name)),
        weight: 1,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.8
    };
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: selectedElectorate
    });
}

function highlightFeature(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 3,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.8,
    });
    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function selectedElectorate(e) {
    var layer = e.target;
    var i = layer.feature.properties.Name;
    passElect(layer.feature.properties.Name);
}

info.onAdd = function(map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function(props) {
    this._div.innerHTML = '' + (props ? '<b>' + props.Name + '</b>' : 'Click on an electorate');
};

function getColor(party) {
    var color = 'white';
    if (party == "Labor") {
      color = "#D119D1";
    } 
    else if (party == "Liberal") {
      color = "#1975D1";
    }
    else if (party == "Greens") {
      color = "#2EB82E";
    }
    else {
        color = '#FFFF4D';
    }
    return color
}

function getElect(name) {
    var party = '';
    for (var elect in electDataCounts.counts) {
        // console.log(i);
        if (elect == name) {
            // console.log(name);
            party = getParty(electDataCounts.counts[elect]);
        }
    }
    if (party == "Labor") {ALP+=1;}
    else if (party == "Liberal") {LP+=1;}
    else if (party == "Greens") {GRN+=1;}
    else if (party == "Nationals") {NP+=1;}
    return party;
}

function getParty(parties) {  
    var party = '';
    var electTotal = 0;
    var max = 0.0;
    for (var i in parties) {
        electTotal += parties[i].total;
    }
    for (var i in parties) {
        var partyName = i;
        var partyPosRate = parties[i].pos/electTotal;
        if (partyPosRate >= max) {
            max = partyPosRate;
            party = partyName;
        }
    }
    return party;
}

legend.onAdd = function (map) {
    var leg = L.DomUtil.create('div', 'info legend');
    leg.innerHTML += '<div class="myLegend"><i style="background:#D119D1"></i>Labor</div>';
    leg.innerHTML += '<div class="myLegend"><i style="background:#1975D1"></i>Liberal</div>';
    leg.innerHTML += '<div class="myLegend"><i style="background:#2EB82E"></i>Green</div>';
    leg.innerHTML += '<div class="myLegend"><i style="background:#FFFF4D"></i>Nationals</div>';
    return leg;
};



    








