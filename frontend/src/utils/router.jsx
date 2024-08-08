import { createBrowserRouter } from "react-router-dom";
import { Home } from "../pages/home";
import { Login } from "../pages/login";
import { Register } from "../pages/register";
import { Recovery } from "../pages/recovery";
import AuthOutlet from "@auth-kit/react-router/AuthOutlet";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AuthOutlet fallbackPath='/login' />,
    children: [
      {
        path: "/",
        element: <Home />,
      }
    ]
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
    path: "/recover",
    element: <Recovery />,
  },
]);
