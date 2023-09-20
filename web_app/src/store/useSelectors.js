import {useSelector} from "react-redux";


export const useTaxiSelector = () => useSelector(state => state.taxi);

export const useUISelector = () => useSelector(state => state.ui);

export const useUserSelector = () => useSelector(state => state.user);

export const useActiveOrderSelector = () => useSelector(state => state.activeOrder);
