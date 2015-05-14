var info = L.control();


$( document ).ready(function() {
    $('#dashboard').hide();
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
});




// get the max total field 
function getParty(parties) {  
    var mParty = '';
    var max = 0.0;

    // console.log(parties);

    for (var i in parties) {
        var partyName = i;
        var partyTotal = parties[i].total;
        // console.log(partyTotal);
        if (partyTotal >= max) {
            max = partyTotal;
            mParty = partyName;
        }
    }
    return mParty;
}



function getElect(name) {
    var party = '';
    // console.log(name);
    for (var i in electData.counts) {
        // console.log(i);
        line = electData.counts[i];
        if (line.electorate.name == name) {
            // console.log(name);
            party = getParty(line.electorate.parties);
        }
    }
    // console.log(party);
    return party;
}



function getColor(party) {
    var color = 'yellow';

    if (party == "Labor") {
      color = "#D119D1";
    } 
    else if (party == "Liberal") {
      color = "#1975D1";
    }
    else if (party == "Greens") {
      color = "#2EB82E";
    }

    return color
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
    console.log(layer.feature.properties.Name);
    console.log(layer.feature.properties.newMargins);
    // map.fitBounds(e.target.getBounds());
    pass_elect(layer.feature.properties.Name);
}


function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: selectedElectorate
    });
}


function addGeoToMap(map) {
    geojson = L.geoJson(electInfo, {
        onEachFeature: onEachFeature,
        style: style
    }).addTo(map);
}


info.onAdd = function(map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function(props) {
    this._div.innerHTML = '' + (props ? '<b>' + props.Name + '</b>' : 'Click on an electorate');
};



var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var leg = L.DomUtil.create('div', 'info legend');
    leg.innerHTML += '<div class="myLegend"><i style="background:#D119D1"></i>Labor</div>';
    leg.innerHTML += '<div class="myLegend"><i style="background:#1975D1"></i>Liberal</div>';
    leg.innerHTML += '<div class="myLegend"><i style="background:#2EB82E"></i>Green</div>';

    return leg;
};



    








