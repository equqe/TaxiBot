import {createSlice} from "@reduxjs/toolkit";


const userSlice = createSlice({
    name: "user",
    initialState: {
        data: {
            coupons: [],
            has_active_order: null,
        },
        token: new URLSearchParams(window.location.search).get("telegram_auth_token"),
        loaded: false
    },
    reducers: {
        setUserData: (state, action) => {
            state.data = action.payload;
            state.loaded = true;
        },
    },
});


export default userSlice;
