import {bindActionCreators} from "@reduxjs/toolkit";
import {useDispatch} from "react-redux";
import taxiSlice from "./slices/taxi";
import UISlice from "./slices/ui";
import userSlice from "./slices/user";
import activeOrderSlice from "./slices/activeOrder";


export const useTaxiActions = () => {
    const dispatch = useDispatch();
    return bindActionCreators(taxiSlice.actions, dispatch);
};

export const useUIActions = () => {
    const dispatch = useDispatch();
    return bindActionCreators(UISlice.actions, dispatch);
};

export const useUserActions = () => {
    const dispatch = useDispatch();
    return bindActionCreators(userSlice.actions, dispatch);
};

export const useActiveOrderActions = () => {
    const dispatch = useDispatch();
    return bindActionCreators(activeOrderSlice.actions, dispatch);
}
