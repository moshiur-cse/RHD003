function mapInit() {

    var blankUrl = "../images/blank.png",
        osmUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        googleUrlHy = "http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}",
        googleUrlSa = "http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        googleUrlSt = "http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        googleUrlTr = "http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        myCustomrUrl = "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibW9zaGl1cmNzZSIsImEiOiJjazExcGZ4bjAwaXltM2NyaDdhajlyd2FkIn0.c_SEmtkCpdNmBpogXYkUng",
        mapbUrl = "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYWxoYWRpLWNzZSIsImEiOiJjamx1azJ5emcwamlkM3ZxeHB0ajB0d3I1In0.k_DovXLLPpp7fQ_i685ocA",
        esriUrl = "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        mapAttrib = "Map data © <a href='https://www.cegisbd.com/' target='_blank'>CEGIS</a>";

    var openstreet = L.tileLayer(osmUrl, { id: 'MapID', minZoom: 0, maxZoom: 25, attribution: mapAttrib }),
        googleHy = L.tileLayer(googleUrlHy, { id: 'MapID', minZoom: 0, maxZoom: 25, subdomains: ["mt0", "mt1", "mt2", "mt3"], attribution: mapAttrib }),
        googleSa = L.tileLayer(googleUrlSa, { id: 'MapID', minZoom: 0, maxZoom: 25, subdomains: ["mt0", "mt1", "mt2", "mt3"], attribution: mapAttrib }),
        googleSt = L.tileLayer(googleUrlSt, { id: 'MapID', minZoom: 0, maxZoom: 25, subdomains: ["mt0", "mt1", "mt2", "mt3"], attribution: mapAttrib }),
        googleTr = L.tileLayer(googleUrlTr, { id: 'MapID', minZoom: 0, maxZoom: 25, subdomains: ["mt0", "mt1", "mt2", "mt3"], attribution: mapAttrib }),
        myCustomr = L.tileLayer(myCustomrUrl, { id: 'moshiurcse.ckxd3f9kf08k528mp8e8ius4i-0vqks', minZoom: 0, maxZoom: 25, subdomains: ["mt0", "mt1", "mt2", "mt3"], attribution: mapAttrib }),
        //mapboxLi = L.tileLayer(myCustomrUrl, { id: 'MapID', minZoom: 0, maxZoom: 25, id: "mapbox.light", attribution: mapAttrib }),
        //mapboxSt = L.tileLayer(myCustomrUrl, { id: 'MapID', minZoom: 0, maxZoom: 25, id: "mapbox.streets", attribution: mapAttrib }),
        esri = L.tileLayer(esriUrl, { id: 'MapID', minZoom: 0, maxZoom: 25, attribution: mapAttrib }),

        blank = L.tileLayer(blankUrl, { id: 'MapID', minZoom: 0, maxZoom: 25, attribution: mapAttrib });


    mymap = new L.Map("basic-map",
        {
            center: new L.LatLng(23.737777, 90.537777),
            fullscreenControl: true,
            zoomControl: false,
            maxZoom: 15,
            minZoom: 2,
            zoom: 6.0,
            layers: [openstreet],

        });


    mymap.setView([23.837777, 90.347777], 7.0);

    var baseMaps = {
        "Open Street": openstreet,
        "Google Hybrid": googleHy,
        "Google Satellite": googleSa,
        "Google Streets": googleSt,
        "Google Terrain": googleTr,
        "My Customr": myCustomr,
        //"Mapbox Light": mapboxLi,
        //"Mapbox Streets": mapboxSt,
        "ESRI": esri,
        "None": blank
    };

    //mymap.createPane("admin-layer").style.zIndex = 405;
    //mymap.createPane("label-layer").style.zIndex = 601;


    L.tileLayer("", { attribution: mapAttrib }).addTo(mymap);
    L.control.scale().addTo(mymap);
    //L.control.zoom().addTo(mymap);

    L.control.zoom({
        position: 'bottomleft'
    }).addTo(mymap);


    var drawnItems = L.featureGroup().addTo(mymap);

    mymap.addControl(new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            poly: {
                allowIntersection: false
            }
        },
        draw: {
            polygon: {
                allowIntersection: false,
                showArea: true
            }
        }
    }));

    mymap.on(L.Draw.Event.CREATED, function(event) {
        var layer = event.layer;

        drawnItems.addLayer(layer);
    });




    //mymap.on("mousemove",
    //    function (evt) {
    //        $("#map_cord_info").html(evt.latlng.lat.toFixed(8) + ", " + evt.latlng.lng.toFixed(8));
    //    });


    $("#map_center").on("click",
        function(e) {
            mymap.setView([23.737777, 90.537777], 7.0);
        });

    bgLayers = L.control.layers(baseMaps, { 'drawlayer': drawnItems }, { collapsed: false });
    bgLayers.addTo(mymap);

    mymap.on('zoomend', function(evt) {
        hideOverlappingTooltips();
    });

    var bgLayersContent = $(bgLayers.getContainer());
    //bgLayersContent.find("a.leaflet-control-layers-toggle").remove();
    bgLayersContent.find("form.leaflet-control-layers-list").css("display", "block");
    //$("#map_bg_layers").append(bgLayersContent);


}

function overlap(rect1, rect2) {
    return (!(rect1.right < rect2.left ||
        rect1.left > rect2.right ||
        rect1.bottom < rect2.top ||
        rect1.top > rect2.bottom));
}

function hideOverlappingTooltips() {
    var rects = [];
    var tooltips = document.getElementsByClassName('mapLabel');
    for (var i = 0; i < tooltips.length; i++) {
        tooltips[i].style.visibility = '';
        rects[i] = tooltips[i].getBoundingClientRect();
    }
    for (var i = 0; i < tooltips.length; i++) {
        if (tooltips[i].style.visibility != 'hidden') {
            for (var j = i + 1; j < tooltips.length; j++) {
                if (overlap(rects[i], rects[j])) tooltips[j].style.visibility = 'hidden';
            }
        }
    }
}

function map_reset() {
    location.reload(true);
}

function afterRender(result) {
    return result;
}

function afterExport(result) {
    return result;
}

function downloadMap(caption) {
    jQuery("#busy-indicator").fadeIn(150);

    var downloadOptions = {
        container: mymap._container,
        caption: {
            text: caption,
            font: '30px Arial',
            fillStyle: 'black',
            position: [100, 200]
        },
        exclude: ['.leaflet-control-zoom', '.leaflet-control-attribution'],
        include: ['.map_btns_content'],
        format: 'image/png',
        fileName: 'Map.png',
        afterRender: afterRender,
        afterExport: afterExport
    };
    var promise = mymap.downloadExport(downloadOptions);
    var data = promise.then(function(result) {
        return result;
    });
    jQuery("#busy-indicator").fadeOut(150);

}
