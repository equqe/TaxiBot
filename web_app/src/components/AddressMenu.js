import { Fragment, useEffect, useState, useRef } from "react";
import { useSelector } from "react-redux";
import { toast } from "react-toastify";
import { useTaxiActions } from "../store/useActions";
import AddressMenuElement from "./AddressMenuElement";
import {useUISelector} from "../store/useSelectors";

const RedPoint = <div></div>;
const GreyPoint = <div className="grey-color"></div>;
const Slicer = (
  <div className="menu__slicer-wrap">
    <div className="menu__slicer"></div>
  </div>
);

const AddressMenu = (props) => {
  const [results, setResults] = useState([]);
  const [activeField, setActiveField] = useState("start");
  const { setStartAddress, setStartLocation, setEndAddress, setEndLocation } =
    useTaxiActions();


  const { startAddress, endAddress } = useSelector((state) => state.taxi);


  const onClickResult = (result) => {
    if (activeField === "start") {
      setStartAddress(result.set_name);
      setStartLocation({
        latitude: parseFloat(result.lat),
        longitude: parseFloat(result.lon),
      });
    } else {
      setEndAddress(result.set_name);
      setEndLocation({
        latitude: parseFloat(result.lat),
        longitude: parseFloat(result.lon),
      });
    }
  };

  return (
    <>
      <AddressMenuElement
        point={RedPoint}
        text={startAddress || ""}
        isInput={props.isInput}
        isStart={true}
        setResults={setResults}
        setActiveField={setActiveField}
        isEntranceRequired={props.isEntranceRequired}
      />

      {Slicer}

      <AddressMenuElement
        point={GreyPoint}
        text={endAddress || ""}
        style={{ paddingBottom: "12px" }}
        isInput={props.isInput}
        setResults={setResults}
        setActiveField={setActiveField}
      />
      <div
        style={{
          maxHeight: "70%",
          overflowY: "scroll",
          position: "fixed",
          width: "90%",
        }}
      >
        {results.map((result, idx) => {
          return (
            <Fragment key={idx}>
              <div
                className="address-result"
                style={{ padding: "5px 10px" }}
                onClick={() => onClickResult(result)}
              >
                {result.display_name}
              </div>
              {Slicer}
            </Fragment>
          );
        })}
      </div>
    </>
  );
};

export default AddressMenu;
