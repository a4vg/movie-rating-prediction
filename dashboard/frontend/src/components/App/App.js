import React from "react";
import { Router } from "@reach/router";
import NavBar from "../NavBar/Navbar";
import Prediction from "../Prediction/Prediction";
import "./App.css";

const App = () => {
  //year,genre,director,budget,country,runtime,mc1,mc2
  return (
    <div className="App">
      <NavBar />
      <Router>
        <Prediction path="/" />
      </Router>
    </div>
  );
};

export default App;
