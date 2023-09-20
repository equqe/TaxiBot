import 'antd/dist/antd.css';
import "leaflet/dist/leaflet.css";
import React from "react";
import ReactDOM from "react-dom/client";
import {Provider} from "react-redux";
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import "./static/css/banner.css";
import "./static/css/index.css";
import "./static/css/navbar.css";
import {store} from "./store/store";
import eruda from "eruda";


const root = ReactDOM.createRoot(document.getElementById("root"));

if (process.env.REACT_APP_DEBUG !== '0') {
    eruda.init()
}

root.render(
    <Provider store={store}>
        <ToastContainer limit={3}/>
        <App/>
    </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
