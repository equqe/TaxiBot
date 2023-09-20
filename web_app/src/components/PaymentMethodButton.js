import React from 'react'
import cashIcon from '../assets/wwallet.png'
import debitIcon from '../assets/online-money.png'
import CustomButton from './CustomButton'
import { useTaxiActions } from "../store/useActions";
import { useSelector } from 'react-redux';
import {sendHapticFeedback} from "../services/telegram";

const PaymentMethodButton = () => {
  
  const { paymentMethod } = useSelector((state) => state.taxi);

  const { setPaymentMethod } = useTaxiActions();

  const toggle = () => {
    if (paymentMethod === 'cash')
    {
      setPaymentMethod('card');
    }
    else
    {
      setPaymentMethod('cash');
    }

  }

    return (
      // state == true - наличные
      // state == false - перевод на карту
      // ####Piece of bad code####
      // В перспективе рассматривается переход на TypeScript,
      // где эта же логика будет по-человечески переписана на enum'ы. 
      paymentMethod === 'cash' ? 
      <CustomButton 
      width='50vw'
      height='3.5em' 
      text="Наличные"
      icon={cashIcon}
      backgroundColor='black' 
      onClick={toggle} />
      :
      <CustomButton width='50vw' height='3.5em' text="Перевод" icon={debitIcon} backgroundColor='black' onClick={toggle} />

  )
} 

export default PaymentMethodButton