
const msk = { lat: 55.75583, lng: 37.61778 }
const spb = { lat: 59.95, lng: 30.31667 }
const ekb = { lat: 56.83333, lng: 60.58333 }
city_in_url = window.location.href.slice(0, -1).split('/').pop()

if(city_in_url=='msk'){
  city = msk
  heatMapData = mskdata
  radius = 50
  zoom = 13
}else if(city_in_url == 'spb'){
  city = spb
  heatMapData = spbdata
  radius = 150
  zoom = 13
}else if(city_in_url == 'ekb'){
  city = ekb
  heatMapData = ekbdata
  radius = 250
  zoom = 13
}


async function initMap() {
    

      var heatMapList = []
      for(let el of heatMapData){
          if(el){
            heatMapList.push({location: new google.maps.LatLng(el.lat, el.lng,), weight: el.weight})
          }
  }
      
      var sntpt = new google.maps.LatLng(city.lat, city.lng);
      
      map = new google.maps.Map(document.getElementById('map'), {
        center: sntpt,
        zoom: zoom,
        mapTypeId: 'satellite',
        zoomControl: false,
        scaleControl: false,
        scrollwheel: false,
      });
      
      var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatMapList,
        radius: radius,
      });
      heatmap.setMap(map);
    }
