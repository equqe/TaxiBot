import {Input} from "antd";
import {useEffect} from "react";
import locationArrow from "../assets/location-marker.svg"
import {iconDown, iconUp} from "../static/styledIcons/styledIcons";
import {useUIActions} from "../store/useActions";

const {TextArea} = Input;

const Navbar = ({children, opened, setOpened, ...props}) => {
    const { setTutorialRun } = useUIActions();

    useEffect(() => {
    });

    const open = () => {
        setOpened(true);
    };

    const close = () => {
        setOpened(false);
    };

    const change = () => {
        if (opened) {
            close();
        } else {
            open();
        }
    };

    const style = {
        height: opened ? props.maxHeight : props.minHeight,
    };
    if (props.zIndex) {
        style.zIndex = props.zIndex;
    }

    return (<div
        className="banner"
        style={style}
        id={props.isInput ? "input-banner" : ""}
    >
        {props.isInput ? null : (<div
            className="location-button--wrapper"
            onClick={() => {
                setTutorialRun(false);
                props.getCurrentPosition();
            }}
        >
            <img src={locationArrow} alt="location-arrow" className="location-button--icon"/>

        </div>)}
        <div className="banner__top">
        <span className="banner__top-wrap" onClick={() => change()}>
          {opened ? iconDown : iconUp}
        </span>
        </div>
        <div className="banner__content">
            <div className="banner__content-menu">{children}</div>
        </div>
    </div>);
};

export default Navbar;
