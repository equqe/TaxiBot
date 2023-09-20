import React from "react";
import PaymentMethodButton from "./PaymentMethodButton";
import OrderPreferencesButton from "./OrderPreferencesButton";
import { useUIActions } from "../store/useActions";

const OrderDetailsMenu = () => {
  const { setNavbarPreferencesOpened } = useUIActions();

  return (
    <div className="order-details-wrapper">
      <PaymentMethodButton />
      <OrderPreferencesButton
        onClick={() => setNavbarPreferencesOpened(true)}
        margin={'0 0 0 1em'}
      />
    </div>
  );
};

export default OrderDetailsMenu;
