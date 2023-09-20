import ReactJoyride from "react-joyride";
import {useUISelector} from "../store/useSelectors";


const STEPS = [{
    target: '.location-button--wrapper',
    content: 'Определить ваше местоположение? Нажмите',
    disableBeacon: true,
    placement: 'top-start',
    isFixed: true,
}];


const Tutorial = () => {
    const {tutorialRun} = useUISelector()


    return <ReactJoyride
        steps={STEPS}
        run={tutorialRun}
        spotlightClicks={true}
        styles={{
            options: {
                backgroundColor: '#fff',
                primaryColor: '#000',
                textColor: '#000',
                zIndex: 1005,
            }
        }}
        locale={{
            back: 'Назад',
            close: 'Закрыть',
            last: 'Последний',
            next: 'Далее',
            open: 'Открыть диалоговое окно',
            skip: 'Пропустить',
        }}
    />
}


export default Tutorial;