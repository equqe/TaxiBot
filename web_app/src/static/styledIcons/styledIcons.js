import L from "leaflet";
import driverLocationIconSource from '../../assets/driver-location-icon.svg';

export const iconDown = (<svg className="" width="30" height="9" fill="none" transform="">
    <path
        d="M2 2l12.282 4.724a2 2 0 001.436 0L28 2"
        stroke="#ECEEF2"
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
    ></path>
</svg>);

export const iconUp = (<svg
    className=""
    width="30"
    height="9"
    fill="none"
    style={{transform: "rotate(180deg)"}}
>
    <path
        d="M2 2l12.282 4.724a2 2 0 001.436 0L28 2"
        stroke="#ECEEF2"
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
    ></path>
</svg>);

export const driverLocationIcon = new L.Icon({
    iconUrl: driverLocationIconSource,
    iconSize: [58, 51],
    iconAnchor: [25,50],
})
