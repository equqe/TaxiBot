import axios from "axios";
import { NOMINATIM_URL } from "../const";


const NominatimClient = axios.create({
    baseURL: NOMINATIM_URL,
})

export const nominatimSearch = query => {
    return NominatimClient.get(
        `/search?q=${query}&addressdetails=1`,
    )
}

export const nominatimReverse = (latitude, longitude) => {
    return NominatimClient.get(
        `/reverse?lat=${latitude}&lon=${longitude}&addressdetails=1&format=json`
    )
}