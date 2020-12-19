import React, { Suspense } from "react";
import ReactDOM from "react-dom";
import "./index.css";
import { Router } from "@reach/router";
import App from "./components/App/App";
import reportWebVitals from "./reportWebVitals";
import "materialize-css/dist/js/materialize";
import "materialize-css/dist/css/materialize.css";
import "material-design-icons/iconfont/material-icons.css";

ReactDOM.render(
  <React.StrictMode>
    <Suspense fallback={<div>Loeding...</div>}>
      <Router>
        <App default />
      </Router>
    </Suspense>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
