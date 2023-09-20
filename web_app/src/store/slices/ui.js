import {createSlice} from "@reduxjs/toolkit";
import {DEFAULT_CENTER_POSITION} from "../../const";


const UISlice = createSlice({
    name: "ui",
    initialState: {
        navbar1Opened: false,
        navbar2Opened: false,
        navbarPreferencesOpened: false,
        activeOrderNavbarOpened: false,
        pickLocationField: null,
        centerPosition: DEFAULT_CENTER_POSITION,
        tutorialRun: true,
    },
    reducers: {
        setNavbar1Opened: (state, action) => {
            state.navbar1Opened = action.payload;
        },
        setNavbar2Opened: (state, action) => {
            state.navbar2Opened = action.payload;
        },
        setNavbarPreferencesOpened: (state, action) => {
            state.navbarPreferencesOpened = action.payload;
        },
        setPickLocationField: (state, action) => {
            state.pickLocationField = action.payload;
        },
        setActiveOrderNavbarOpened: (state, action) => {
            state.activeOrderNavbarOpened = action.payload;
        },
        setCenterPosition: (state, action) => {
            state.centerPosition = action.payload
        },
        setTutorialRun: (state, action) => {
            state.tutorialRun = action.payload
        },
    },
});

export default UISlice;
