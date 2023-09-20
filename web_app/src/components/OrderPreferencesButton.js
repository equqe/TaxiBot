import React from "react";
import CustomButton from "./CustomButton";
import prefIcon from "../assets/preferences.png";

const OrderPreferencesButton = (props) => {
  return (
    <CustomButton
      {...props}
      width="50vw"
      height="3.5em"
      text="Пожелания"
      icon={prefIcon}
      backgroundColor="black"
    />
  );
};

export default OrderPreferencesButton;
