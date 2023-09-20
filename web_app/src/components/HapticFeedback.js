import {useEffect} from "react";
import {useTaxiSelector, useUISelector} from "../store/useSelectors";
import {sendHapticFeedback} from "../services/telegram";


const HapticFeedback = () => {
    const {startAddress, endAddress, babyChair, paymentMethod, currentLocation, coupon} = useTaxiSelector();
    const {navbar1Opened, navbar2Opened, navbarPreferencesOpened} = useUISelector();


    useEffect(() => {
        sendHapticFeedback()
    }, [startAddress, endAddress, babyChair, paymentMethod, currentLocation, coupon, navbar1Opened, navbar2Opened, navbarPreferencesOpened])
}


export default HapticFeedback;