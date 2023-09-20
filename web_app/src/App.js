import {useEffect} from "react";
import {toast} from "react-toastify";
import {useUserActions} from "./store/useActions";
import {coreGetUser} from "./api/core";
import {useUserSelector} from "./store/useSelectors";
import HapticFeedback from "./components/HapticFeedback";
import CreateOrder from "./components/CreateOrder";
import ActiveOrderMenu from "./components/ActiveOrderMenu";
import Loader from "./components/Loader";


const App = (props) => {

    const {
        token: userAuthToken,
        data: userData,
        loaded: userLoaded,
    } = useUserSelector()
    const {setUserData} = useUserActions()

    useEffect(() => {
        coreGetUser(userAuthToken).then(
            response => setUserData(response.data)
        ).catch(
            error => {
                console.error(error)
                toast.error("Пользователь не найден")
            }
        )
        window.Telegram.WebApp.expand();
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.enableClosingConfirmation()
        window.Telegram.WebApp.onEvent("viewportChanged", () => {
            if (!window.Telegram.WebApp.isExpanded) {
                window.Telegram.WebApp.expand();
            }
        });
    }, []);

    if (!userLoaded){
        return <Loader text={"Загрузка..."} />
    }

    return (
        <>
            <HapticFeedback/>
            { userData?.has_active_order ? <ActiveOrderMenu /> : <CreateOrder />}
        </>
    );
};

export default App;
