import {useEffect, useMemo, useState} from "react";
import {CircleMarker, MapContainer, TileLayer} from "react-leaflet";
import {toast} from "react-toastify";
import {LocationPicker} from "./LocationPicker";
import {DEFAULT_CENTER_POSITION} from "../const";
import {useTaxiActions, useUIActions} from "../store/useActions";
import {store} from "../store/store";
import {coreGetPrice} from "../api/core";
import {useTaxiSelector, useUISelector} from "../store/useSelectors";
import {routingCreateControl} from "../services/routing";
import Tutorial from "./Tutorial";
import BaseNavbar from "./BaseNavbar";
import {nominatimReverse} from "../api/nominatim";
import {nominatimProcessResult} from "../services/nominatim";


const App = (props) => {
    const [map, setMap] = useState();
    const [zoom, setZoom] = useState(13);
    const [routing, setRouting] = useState();
    const data = useTaxiSelector();
    const {
        startAddress,
        startLocation,
        endLocation,
        endAddress,
        babyChair,
        coupon,
    } = useTaxiSelector();

    const {centerPosition} = useUISelector();
    const {setCurrentLocation, setStartLocation, setStartAddress, setCoupon} = useTaxiActions();
    const {setNavbar2Opened} = useUIActions();

    useEffect(() => {

    });

    const flyTo = (coords, zoom = 17) => {
        map.flyTo([coords.latitude, coords.longitude], zoom, {
            duration: 0.5,
        });
    };

    const drawRoute = () => {
        if (!startLocation || !endLocation || !map) return;
        if (routing) routing.spliceWaypoints(0, 2);
        var newRouting = routingCreateControl(startLocation, endLocation).addTo(map);
        setRouting(newRouting);
        setNavbar2Opened(false);
    };

    const sendData = () => {
        const state = store.getState();
        const _data = state.taxi;
        const body = JSON.stringify({
            start_location: _data.startLocation,
            end_location: _data.endLocation,
            baby_chair: _data.babyChair,
            payment_method: _data.paymentMethod,
            comment: _data.comment,
            coupon: _data.coupon,
            entrance: _data.startAddressEntrance,
        });
        window.Telegram.WebApp.sendData(body);
    };

    const tryToGetPrice = () => {
        if (!startLocation || !endLocation || !map) return;
        const mainButton = window.Telegram.WebApp.MainButton;
        mainButton.setText("Расчёт...");
        window.Telegram.WebApp.MainButton.show();
        window.Telegram.WebApp.MainButton.showProgress();

        coreGetPrice(startLocation, endLocation, babyChair, coupon)
            .then((response) => {

                if (coupon && response.data.cost === response.data.raw_cost) {
                    toast.info("Скидка не может быть использована, так как стоимость поездки равна минимальной стоимости");
                    setCoupon(null);
                }

                window.Telegram.WebApp.MainButton.setText(
                    `Заказать — ${response.data.cost}р.`
                );
                mainButton.hideProgress();
                window.Telegram.WebApp.onEvent("mainButtonClicked", sendData);
            })
            .catch((error) => {
                mainButton.hide();
                if (error.response.data) {
                    const errorData = error.response.data;
                    if (errorData.detail === "city_not_registered") {
                        toast.error("Город не обслуживается");
                        return;
                    }
                }
                toast.error("Произошла ошибка");
            });
    };

    useEffect(() => {
        tryToGetPrice();
    }, [startLocation, endLocation, babyChair, coupon]);

    useEffect(() => {
        if (!endLocation) return;
        flyTo(endLocation);
        drawRoute();
    }, [endLocation]);

    useEffect(() => {
        if (!startLocation) return;
        flyTo(startLocation);
        drawRoute();
    }, [startLocation]);

    useEffect(() => {
        if (centerPosition === DEFAULT_CENTER_POSITION) return;
        flyTo({latitude: centerPosition[0], longitude: centerPosition[1]}, 13)

    }, [centerPosition]);

    const displayMap = useMemo(() => (
        <MapContainer
            center={startLocation ? startLocation : centerPosition}
            zoom={zoom}
            style={{width: "100vw", height: "70vh"}}
            ref={setMap}
        >
            <LocationPicker/>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {startLocation ? (
                <CircleMarker
                    center={[startLocation.latitude, startLocation.longitude]}
                    pathOptions={{color: "red"}}
                    radius={5}
                />
            ) : null}
            {endLocation ? (
                <CircleMarker
                    center={[endLocation.latitude, endLocation.longitude]}
                    pathOptions={{color: "grey"}}
                    radius={5}
                />
            ) : null}
        </MapContainer>
    ));

    const getCurrentPosition = () => {
        if (navigator.geolocation) {
            function geo_success(position) {
                flyTo(position.coords);
                setCurrentLocation({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                });
                try {
                    setStartLocation({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                    })

                    nominatimReverse(position.coords.latitude, position.coords.longitude)
                        .then((response) => {

                            if (!response.data) return;
                            const result = nominatimProcessResult(response.data)
                            setStartAddress(result.set_name)
                        }).catch(error => {
                        toast.error("Не удалось определить адрес");
                        console.error(error);
                    });
                } catch {
                    toast.error("Не удалось определить адрес");
                }
            }

            function geo_error(error) {
                geolocFail();
            }

            navigator.geolocation.getCurrentPosition(geo_success, geo_error, {});
        } else {
            geolocFail();
        }

        function geolocFail() {
            toast.error("Не удалось определить местоположение");
        }
    };


    return (
        <div>
            <Tutorial/>
            {displayMap}
            <BaseNavbar getCurrentPosition={getCurrentPosition}/>
        </div>
    );
};

export default App;
