import L from "leaflet";
import "leaflet-routing-machine";


export const routingCreateControl = (startLocation, endLocation) => L.Routing.control({
    waypoints: [
        L.latLng(startLocation.latitude, startLocation.longitude),
        L.latLng(endLocation.latitude, endLocation.longitude),
    ],
    language: "ru",
    draggableWaypoints: false,
    routeWhileDragging: false,
    fitSelectedRoutes: true,
    addWaypoints: false,
    show: false,
    lineOptions: {
        styles: [{color: "rgb(0, 136, 204)", opacity: 0.8, weight: 9}],
    },
    router: new L.Routing.OSRMv1({
        serviceUrl: "https://routing.taxiber.ru/route/v1",
        routingOptions: {
            alternatives: false,
            steps: false,
        },
        useHints: false,
    }),
    createMarker: function () {
        return null;
    },
})
