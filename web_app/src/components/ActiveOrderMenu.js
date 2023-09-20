import {useEffect, useMemo, useState} from "react";
import Navbar from "./Navbar";
import {useActiveOrderSelector, useUISelector, useUserSelector} from "../store/useSelectors";
import {CircleMarker, MapContainer, Marker, TileLayer} from "react-leaflet";
import {useActiveOrderActions, useUIActions} from "../store/useActions";
import {coreGetUserActiveOrder} from "../api/core";
import {toast} from "react-toastify";
import {driverLocationIcon} from "../static/styledIcons/styledIcons";
import {routingCreateControl} from "../services/routing";
import {useMap} from 'react-leaflet/hooks';
import Loader from "./Loader";

const statusMap = {
    101: "Ожидается принятие заказа одним из водителей",
    102: "Водитель уже в пути",
    103: "Водитель ожидает вас",
    104: "Поездка началась, приятного пути!",
}


const ActiveOrderRouting = (props) => {
    const map = useMap();
    const [routing, setRouting] = useState();
    const {activeOrderData} = useActiveOrderSelector();


    useEffect(() => {
        drawRoute();
    }, [activeOrderData])


    const drawRoute = () => {
        if (!map || !activeOrderData) return;

        const start = activeOrderData.driver.location;
        let end = null;
        let newRouting = null;

        switch (activeOrderData.status) {
            case 102:
                end = activeOrderData.start_location
                break
            case 104:
                end = activeOrderData.end_location
                break
        }
        if (end) {
            if (routing) routing.spliceWaypoints(0, 2);
            newRouting = routingCreateControl(start, end).addTo(map);
        }

        setRouting(newRouting);

    };

    return null;

}


const ActiveOrderMenu = (props) => {

    const [map, setMap] = useState();
    const [zoom, setZoom] = useState(13);
    const [routing, setRouting] = useState();
    const {activeOrderData} = useActiveOrderSelector();
    const {setActiveOrderData} = useActiveOrderActions();
    const {centerPosition, activeOrderNavbarOpened} = useUISelector();
    const {setActiveOrderNavbarOpened} = useUIActions();
    const {token: userAuthToken} = useUserSelector();

    const driverInfo = activeOrderData?.driver?.driver;
    const driverLocation = activeOrderData?.driver ? [activeOrderData.driver.location.latitude, activeOrderData.driver.location.longitude] : null;


    const updateActiveOrderData = () => {
        coreGetUserActiveOrder(userAuthToken)
            .then(response => setActiveOrderData(response.data))
            .catch((error) => {
                toast.error("Не удалось получить данные об активном заказе");
                console.error(error);
            });
    }

    useEffect(() => {
        updateActiveOrderData()
        const updateOrderDataInterval = setInterval(updateActiveOrderData, 5000)
        return () => {
            clearInterval(updateOrderDataInterval)
        }
    }, [])


    const flyTo = (coords, zoom = 17) => {
        map.flyTo([coords.latitude, coords.longitude], zoom, {
            duration: 0.5,
        });
    };


    const displayMap = useMemo(() => (
        <MapContainer
            center={driverLocation || centerPosition}
            zoom={zoom}
            style={{width: "100vw", height: "65vh"}}
            ref={setMap}
        >
            <ActiveOrderRouting/>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {driverLocation ?
                <Marker position={driverLocation} icon={driverLocationIcon}/>
                : null}
            {
                (activeOrderData?.status === 102 || activeOrderData?.status === 103)?
                    <CircleMarker
                        center={[activeOrderData?.start_location.latitude, activeOrderData?.start_location.longitude]}
                        pathOptions={{color: "red"}}
                        radius={5}
                    />
                    :null
            }
            {
                (activeOrderData?.status === 104)?
                    <CircleMarker
                        center={[activeOrderData?.end_location.latitude, activeOrderData?.end_location.longitude]}
                        pathOptions={{color: "grey"}}
                        radius={5}
                    />
                    :null
            }
        </MapContainer>
    ));

    if(activeOrderData?.status === 101){
        return <Loader text={"Поиск водителей..."}/>
    }

    return activeOrderData?.driver ? (
        <>
            {displayMap}

            <Navbar
                isInput={true}
                minHeight={"40%"}
                maxHeight={"70%"}
                zIndex={1003}
                opened={activeOrderNavbarOpened}
                setOpened={setActiveOrderNavbarOpened}
            >
                {<div className="active-order-menu__container">

                    <div className="active-order-menu__heading">
                        Вас повезёт
                    </div>

                    <div className="active-order-menu__flex-container">

                        <img src={driverInfo.photo_url} alt="driver's photo"
                             className="active-order-menu__driver-photo"/>

                        <div className="active-order-menu__driver-info">

                            <div className="active-order-menu__driver-name">
                                {activeOrderData.driver.first_name}
                            </div>

                            <div className="active-order-menu__car-info">
                                <b>{driverInfo.car.color}</b>
                                {` ${driverInfo.car.brand}`}
                            </div>

                        </div>
                    </div>

                    <div className="active-order-menu__number-plate">
                        {driverInfo.car.number}
                    </div>

                    <div className="active-order-menu__order-status">
                        {statusMap[activeOrderData.status]}
                    </div>

                </div>}
            </Navbar>
        </>
    ) : null
}

export default ActiveOrderMenu;