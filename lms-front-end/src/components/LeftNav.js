import React, { useState } from "react";
import './LeftNav.css';
import { LeftNavItems } from "./LeftNavItems";
import { LeftNavUser } from './LeftNavUser';
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { addUserInfo } from "../redux/userSlicer";

const LeftNav = () => {

    const navigate = useNavigate();
    const userData = useSelector(
        (state) => state.user.user
    );
    const dispatch = useDispatch();

    return <div className="leftnav">
        <ul className="leftnavlist">
        {userData.role == 'admin' ? LeftNavItems.map((item, key) => {
            return (
                <li key={key} className="itemrow" id={window.location.pathname == item.link ? "active" : ""} onClick={() => {
                    if (item.title == 'Logout') {
                        navigate(item.link);
                        dispatch(addUserInfo({}));
                    } else {
                        navigate(item.link);
                    }
                }}>
                    <div id="icon">{item.icon}</div>{" "}
                    <div id="title">{item.title}</div>{" "}
                </li>
            )
        }) : LeftNavUser.map((item, key) => {
            return (
                <li key={key} className="itemrow" id={window.location.pathname == item.link ? "active" : ""} onClick={() => {
                    if (item.title == 'Logout') {
                        navigate(item.link);
                        dispatch(addUserInfo({}));
                    } else {
                        navigate(item.link);
                    }
                }}>
                    <div id="icon">{item.icon}</div>{" "}
                    <div id="title">{item.title}</div>{" "}
                </li>
            );
        })}
        </ul>
    </div>
}

export default LeftNav;