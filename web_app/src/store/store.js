import { combineReducers, configureStore } from "@reduxjs/toolkit";
import taxiSlice from "./slices/taxi";
import UISlice from "./slices/ui";
import userSlice from "./slices/user";
import activeOrderSlice from "./slices/activeOrder";


const rootReducer = combineReducers({
  taxi: taxiSlice.reducer,
  ui: UISlice.reducer,
  user: userSlice.reducer,
  activeOrder: activeOrderSlice.reducer,
});

export const store = configureStore({
  reducer: rootReducer,
});


