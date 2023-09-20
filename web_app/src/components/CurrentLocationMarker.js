import { useEffect } from "react";
import { CircleMarker, Popup } from "react-leaflet";
import { useSelector } from "react-redux";



const CurrentLocationMarker = (props) => {
    const { currentLocation } = useSelector((state) => state.taxi);

    useEffect(()=>{
        
    }, [currentLocation])

    const element = currentLocation?<CircleMarker
        center={[currentLocation.latitude, currentLocation.longitude]}
        pathOptions={{ color: "rgb(0, 136, 204)" }}
        radius={5}
    >
        <Popup>Вы находитесь примерно тут</Popup>
    </CircleMarker>:null

    return element;
} 



export default CurrentLocationMarker;