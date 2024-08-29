import { createBrowserRouter } from "react-router-dom";
import { Home } from "../pages/home";
import { Login } from "../pages/login";
import { Register } from "../pages/register";
import AuthOutlet from "@auth-kit/react-router/AuthOutlet";
import { Desafios } from "../pages/desafios";
import Profile from "../pages/profile";

export const router = createBrowserRouter([
  {
    path: "/",
    //    element: <AuthOutlet fallbackPath="/login" />,
    children: [
      {
        path: "/",
        element: <Home />,
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
    path: "/profile",
    element: <Profile />,
  },
  {
    path: "/desafios",
    element: <Desafios />,
  },
]);
