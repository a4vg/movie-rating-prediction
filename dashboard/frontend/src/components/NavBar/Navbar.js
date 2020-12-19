import React from "react";
import { Navbar, NavItem, Icon } from "react-materialize";
import { Link } from "@reach/router";
import "./navbar.css";

const NavBar = () => {
  return (
    <Navbar
      className="navbar z-depth-0"
      alignLinks="left"
      centerLogo
      id="mobile-nav"
      menuIcon={<Icon>menu</Icon>}
      options={{
        draggable: true,
        edge: "left",
        inDuration: 250,
        onCloseEnd: null,
        onCloseStart: null,
        onOpenEnd: null,
        onOpenStart: null,
        outDuration: 200,
        preventScrolling: true,
      }}
    >
      <Link to="/">
        <NavItem className="navitem">Prediction</NavItem>
      </Link>
    </Navbar>
  );
};

export default NavBar;
