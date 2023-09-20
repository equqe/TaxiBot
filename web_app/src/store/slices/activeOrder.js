import {createSlice} from "@reduxjs/toolkit";


const activeOrderSlice = createSlice({
    name: "activeOrder",
    initialState: {
        activeOrderData: null
    },
    reducers: {
        setActiveOrderData: (state, action) => {
            state.activeOrderData = action.payload;
        },
    },
});

export default activeOrderSlice;


const activeOrderData = {
    "start_location": {
        "latitude": 59.929651463441324,
        "longitude": 30.316944122314457
    },
    "end_location": {
        "latitude": 59.93396845073152,
        "longitude": 30.32087087631226
    },
    "driver": {
        "first_name": "Сергей 👾 «ChatUpper»",
        "last_name": "",
        "driver": {
            "photo_url": "https://taxiber.ru/media/driver_avatars/9.jpg",
            "car": {
                "brand": "БЭ ЭМ ВЭ",
                "color": "Красивый",
                "number": "А222КК"
            }
        },
        "location": {
            "latitude": 59.938483,
            "longitude": 30.312072
        }
    },
    "cost": "50.00",
    "address": 305,
    "status": 102
}