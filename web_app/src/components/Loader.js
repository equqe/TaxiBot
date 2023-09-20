import React from 'react';
import taxiLogo from "../assets/taxi-logo.svg";

const Loader = ({text, ...props}) => {
    return (
        <>
            <div style={{
                margin: "15vh auto",
                textAlign: "center"
            }}>
                <img src={taxiLogo} alt="logo" height={'140vh'}
                     style={{
                         margin: "0 25vw",
                         marginBottom: "30vh",
                     }}/>
                <h1 className={"center-text"}>{text}</h1>
            </div>
        </>
    );
};

export default Loader;