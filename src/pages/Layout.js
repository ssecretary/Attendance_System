import React from "react";
import { Link, Outlet } from "react-router-dom";
const Layout = () => {
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/aboutus">About Us</Link>
          </li>
          <li>
            <Link to="/contact">Contact Us</Link>
          </li>
        </ul>
      </nav>
      <Outlet />
    </>
  );
};

export default Layout;
