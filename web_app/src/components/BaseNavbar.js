import {useTaxiActions, useUIActions} from "../store/useActions";
import {useSelector} from "react-redux";
import {useUserSelector} from "../store/useSelectors";
import {Fragment, useEffect} from "react";
import AddressMenu from "./AddressMenu";
import OrderDetailsMenu from "./OrderDetailsMenu";
import {Divider, Input, Select, Switch} from "antd";
import {Option} from "antd/es/mentions";
import CustomButton from "./CustomButton";
import Navbar from "./Navbar";


const BaseNavbar = (props) => {
    const {setNavbar1Opened, setNavbar2Opened, setNavbarPreferencesOpened} = useUIActions();
    const {navbar1Opened, navbar2Opened, navbarPreferencesOpened} = useSelector((state) => state.ui);
    const {setBabyChair, setComment, setCoupon} = useTaxiActions();
    const {babyChair, coupon} = useSelector((state) => state.taxi);
    const user = useUserSelector();

    const {TextArea} = Input;

    useEffect(() => {
    }, coupon);

    const coupons = user.data.coupons;

    return (<Fragment>


        <Navbar
            maxHeight={"70%"}
            minHeight={"35%"}
            opened={navbar1Opened}
            setOpened={setNavbar1Opened}
            getCurrentPosition={props.getCurrentPosition}
            detectLocationButton={true}
        >
            <AddressMenu isEntranceRequired={true}/>

            <OrderDetailsMenu onClick={() => setNavbarPreferencesOpened(true)}/>
        </Navbar>

        <Navbar
            minHeight={"0%"}
            maxHeight={"90%"}
            zIndex={1003}
            opened={navbar2Opened}
            setOpened={setNavbar2Opened}
            isInput={true}
        >
            <div className="banner-card">
                <AddressMenu isInput={true}/>
            </div>
        </Navbar>

        <Navbar
            minHeight={"0%"}
            maxHeight={"70%"}
            zIndex={1003}
            opened={navbarPreferencesOpened}
            setOpened={setNavbarPreferencesOpened}
            isInput={true}
        >

            <Divider orientation="left">Другие опции</Divider>
            <div className="preferences-menu-element">
                Детское кресло
                <Switch
                    onChange={() => {
                        setBabyChair(!babyChair);
                    }}
                />
            </div>

            {coupons.length > 0 ?
                <Select placeholder={"Купон на скидку"}
                        style={{width: "100%"}}
                        value={coupon}
                        onChange={(value) => {
                            setCoupon(value)
                        }}>
                    {coupon ?
                        <Option>Отменить</Option>
                        : null}
                    {coupons
                        .filter(coupon => coupon.type === "discount")
                        .map(coupon => (<Option key={coupon.id} value={coupon.id}>{coupon.name}</Option>))}

                </Select>
                : null
            }

            <Divider orientation="left">Комментарий к заказу</Divider>
            <TextArea
                showCount
                maxLength={1000}
                style={{height: 110}}
                autoSize={{minRows: 5, maxRows: 5}}
                onChange={(event) => setComment(event.target.value)}
            />

            <div className="confirm-btn-wrapper">
                <CustomButton
                    width="90vw"
                    height="4em"
                    text="Готово"
                    backgroundColor="black"
                    style={{marginRight: 10}}
                    onClick={() => setNavbarPreferencesOpened(false)}
                />
            </div>
        </Navbar>
    </Fragment>);
};

export default BaseNavbar;
