import React from "react";
import {
  createBrowserRouter,
  RouterProvider,
  useParams,
} from "react-router-dom";
import "./App.css";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import ProductDetails from "./pages/ProductDetails";
import MainLayout from "./components/MainLayout";
import Profile from "./pages/Profile";
import AdminLayout from "./components/admin/AdminLayout";

function ProductDetailsWrapper() {
  const { slug } = useParams();
  return <ProductDetails slug={slug} />;
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "products/:slug",
        element: <ProductDetailsWrapper />,
      },
      {
        path: "profile",
        element: <Profile />,
      },
    ],
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/register",
    element: <Register />,
  },
  {
    path: "/admin",
    element: <AdminLayout />,
    children: [
      {
        path: "",
        element: <div>Admin Dashboard</div>,
      },
      {
        path: "products",
        element: <div>Admin Products</div>,
      },
      {
        path: "orders",
        element: <div>Admin Orders</div>,
      },
      {
        path: "customers",
        element: <div>Admin Customers</div>,
      },
      {
        path: "settings",
        element: <div>Admin Settings</div>,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
