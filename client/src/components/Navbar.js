import React from "react";
import { Link } from "react-router-dom";
import LoginButton from "./LoginButton";
import LogoutButton from "./LogoutButton";

const Navbar = () => {
  return (
    <nav className="bg-blue-200">
      <ul className="flex">
        <li className="mx-6">
          <h1>Quiz Muster</h1>
        </li>
        <li className="mr-6">
          <Link to="/">
            <p className="font-bold underline">Home</p>
          </Link>
        </li>
        <li className="mr-6">
          <Link to="/questions">
            <p className="font-bold underline">Questions</p>
          </Link>
        </li>
        <li className="mr-6 ml-auto">
          <LoginButton />
        </li>
        <li className="mr-6">
          <LogoutButton />
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
