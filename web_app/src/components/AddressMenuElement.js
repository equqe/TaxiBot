import {  useEffect, useState } from "react";
import { useSelector } from "react-redux";
import {useTaxiActions, useUIActions} from "../store/useActions";
import grayLocationIcon from "../assets/gray-location.svg";
import redLocationIcon from "../assets/red-location.svg";
import {useUISelector} from "../store/useSelectors";
import {nominatimSearch} from "../api/nominatim";
import {nominatimProcessResult} from "../services/nominatim";

const AddressMenuElement = (props) => {
  let placeholder = props.isStart ? "Откуда поедете?" : "Куда поедете?";
  const [value, setValue] = useState("");
  const { startAddress, endAddress, startAddressEntrance } = useSelector((state) => state.taxi);
  const { setStartAddressEntrance } = useTaxiActions();
  const { setPickLocationField, setNavbar1Opened, setNavbar2Opened } = useUIActions();
  const { pickLocationField } = useUISelector();



  if (pickLocationField) {
    if (pickLocationField === "start" && props.isStart) {
      placeholder = "Укажите точку на карте"
    } else if (pickLocationField === "end" && !props.isStart) {
      placeholder = "Укажите точку на карте"
    }
  }


  const useEffectArg = props.isStart ? startAddress : endAddress;

  useEffect(() => {
    props.isStart ? setValue(startAddress) : setValue(endAddress);
  }, [useEffectArg]);

  const setActiveField = () => {
    if (props.isStart) {
      props.setActiveField("start");
    } else {
      props.setActiveField("end");
    }
  };

  const onChange = (event) => {
    setValue(event.target.value);
    const newValue = event.target.value
    setActiveField();
    if (newValue === "") {
      props.setResults([]);
      return;
    }

    nominatimSearch(newValue).then((response) => {
          response.data.forEach(a => {
            nominatimProcessResult(a)
          })
          props.setResults(response.data)
        }
    );
  };

  return (
    <div className="menu__element" style={props.style}>
      <div className="menu__element-link">
        <div className="menu__element-content">
          <div className="menu__element-icon">{props.point}</div>

          {!props.isInput ? (
            <span className="menu__element-text"
                  style={{ width: "80%" }}
                  onClick={() => setNavbar2Opened(true)}>
              {props.text || <div style={{ opacity: 0.5 }}>{placeholder}</div>}
            </span>
          ) : (
            <>
              <input
                style={{ width: "80%" }}
                className="menu__element-text"
                value={value}
                placeholder={placeholder}
                onChange={(event) => onChange(event)}
              />

              <img className="pick-location-icon"
                   src={props.isStart ? redLocationIcon : grayLocationIcon}
                   alt="location-icon"
                   height={'24px'}
                   onClick={() => {
                     setNavbar2Opened(false);
                     setPickLocationField(props.isStart ? "start" : "end");
                   }}
              />
            </>
          )}

          {props.isEntranceRequired
            ? [
                <div className="vertical-line"></div>,
                <input
                  type="tel"
                  className="entrance-input"
                  maxLength={2}
                  placeholder="Подъезд"
                  value={startAddressEntrance}
                  onChange={(event) => setStartAddressEntrance(event.target.value)}
                  onFocus={() => setNavbar1Opened(true)}
                  onBlur={() => setNavbar1Opened(false)}
                />,
              ]
            : ""}
        </div>
      </div>
    </div>
  );
};

export default AddressMenuElement;
