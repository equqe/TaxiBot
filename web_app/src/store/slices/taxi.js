import {createSlice} from "@reduxjs/toolkit";

const taxiSlice = createSlice({
    name: "taxi",
    initialState: {
        startAddress: null,
        startLocation: null,

        endAddress: null,
        endLocation: null,
        currentLocation: null,

        startAddressEntrance: null,
        paymentMethod: "cash",
        babyChair: false,
        comment: null,
        coupon: null,
    },
    reducers: {
        setStartAddress: (state, action) => {
            state.startAddress = action.payload;
        },
        setStartLocation: (state, action) => {
            state.startLocation = action.payload;
        },
        setEndAddress: (state, action) => {
            state.endAddress = action.payload;
        },
        setEndLocation: (state, action) => {
            state.endLocation = action.payload;
        },
        setBabyChair: (state, action) => {
            state.babyChair = action.payload;
        },
        setCurrentLocation: (state, action) => {
            state.currentLocation = action.payload;
        },
        setPaymentMethod: (state, action) => {
            state.paymentMethod = action.payload
        },
        setStartAddressEntrance: (state, action) => {
            state.startAddressEntrance = action.payload
        },
        setComment: (state, action) => {
            state.comment = action.payload
        },
        setCoupon: (state, action) => {
            state.coupon = action.payload
        }
    },
});


export default taxiSlice;