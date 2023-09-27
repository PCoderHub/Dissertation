import { createSlice } from "@reduxjs/toolkit"

const initialState = {
    user: {},
}

const userSlicer = createSlice({
    name: 'user',
    initialState,
    reducers: {
        addUserInfo: (state, action) => {
            state.user = {...action.payload},
            console.log(state.user);
        },
    },
});

export const {addUserInfo} = userSlicer.actions;
export default userSlicer.reducer;