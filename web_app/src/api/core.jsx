import axios from "axios";
import {API_URL} from "../const";

const CoreClient = axios.create({
    baseURL: API_URL,
    headers: {"Content-Type": "application/json"}
})

export const coreGetPrice = (startLocation, endLocation, babyChair, coupon) => {
    return CoreClient.post(
        'orders/getPrice/',
        {
            start_location: startLocation,
            end_location: endLocation,
            baby_chair: babyChair,
            coupon_id: coupon,
        }
    );
}

export const coreGetUser = token => {
    return CoreClient.get(
        `users/GetUserApiByTelegramTokenAuth/${token}/`
    )
}


export const coreGetUserActiveOrder = token => {
    return CoreClient.get(
        `orders/getActiveByTelegramAuthToken/${token}/`
    )
}
