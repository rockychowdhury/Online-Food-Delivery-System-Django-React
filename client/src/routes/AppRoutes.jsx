import { Routes, Route } from "react-router-dom";
import HomePage from "../pages/HomePage";
import PrivateRoute from "./privateRoute";
import PublicRoute from "./PublicRoute";

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<PublicRoute />}>
        <Route path="/" element={<HomePage />} />
      </Route>

      {/* Private Routes */}
      {/* <Route element={<PrivateRoute />}>
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/orders" element={<OrderPage />} />
      </Route> */}
    </Routes>
  );
}
