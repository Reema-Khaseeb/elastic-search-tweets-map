// create a Leaflet map and add it to the page
// setView([latitude, longitude], ZoomLevel);
var map = L.map('map').setView([51.505, -0.09], 13);
var popup = L.popup();

// set latitude and longitude on click at ny point at the map
function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}


// attribution <Object type>
const attributionVar = {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
};

const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

// baseLayer
const tiles = L.tileLayer(tileUrl, attributionVar);
tiles.addTo(map);

map.on('click', onMapClick);



const form = document.getElementById('form');
let submitButton = $("#submitButton")[0]
// add an event listener for the submit event
submitButton.addEventListener('click', (event) => {
  // Send a request to the FastAPI server
  sendRequest();
});


async function sendRequest(){
    // Get the query parameters from the form inputs
    const inputText = $('#text_form')[0].value;
    const startDate = $('#start-date')[0].value;
    const endDate = $('#end-date')[0].value;
    const coor1 = $('#coor1')[0].value;
    const coor2 = $('#coor2')[0].value;
    const coor3 = $('#coor3')[0].value;
    const coor4 = $('#coor4')[0].value;

    // send a GET request to the /get_form_input endpoint using the fetch function
    await fetch('/get_form_input?'
    + '&text_form=' +inputText
    + '&start_date=' +startDate
    + '&end_date=' +endDate
    + '&coor1=' +coor1
    + '&coor2=' +coor2
    + '&coor3=' +coor3
    + '&coor4=' +coor4
    ).then(async(response)=>{
    // Parse the JSON response
    res = await response.json()
    listCoordinates = res.score_source

    // Utilize response data to create the heatmap using Leaflet
    var heat = L.heatLayer(listCoordinates, {
        // Set the visual properties of the heatmap
        minOpacity: 0.5,
        maxZoom: 18,
        radius: 25,
        blur: 15
        // Add the heatmap to the Leaflet map
    }).addTo(map);    
    })
}
