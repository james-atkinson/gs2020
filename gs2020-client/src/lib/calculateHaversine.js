export default (lat1, lon1, lat2, lon2) => {
  Number.prototype.toRad = function() {
    return this * Math.PI / 180;
  }
 
  const R = 6371; // km 
  const x1 = lat2-lat1;
  const dLat = x1.toRad();  
  const x2 = lon2-lon1;
  const dLon = x2.toRad();  
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) + 
                 Math.cos(lat1.toRad()) * Math.cos(lat2.toRad()) * 
                 Math.sin(dLon/2) * Math.sin(dLon/2);  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  const d = R * c; 
 
  return (d * 1000) * 3.2808;
};