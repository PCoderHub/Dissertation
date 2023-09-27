import { configureStore, combineReducers } from "@reduxjs/toolkit";
import userReducer from "./redux/userSlicer";

const rootReducer = combineReducers({
    user: userReducer,
});

export default configureStore({
    reducer: rootReducer,
});