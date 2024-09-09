import { createBrowserRouter } from "react-router-dom";
import { Home } from "../pages/home";
import { Login } from "../pages/login";
import { Register } from "../pages/register";
import { Desafios } from "../pages/desafios";
import AuthOutlet from "@auth-kit/react-router/AuthOutlet";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AuthOutlet fallbackPath="/login" />,
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
    path: "/desafios",
    element: <Desafios />,
  },
]);
