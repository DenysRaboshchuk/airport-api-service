import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Flights from "./pages/Flights";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Orders from "./pages/Orders.tsx";


const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "flights",
        element: <Flights />,
      },
      {
        path: "login",
        element: <Login />,
      },
      {
        path: "register",
        element: <Register />,
      },
      {
        path: "orders",
        element: <Orders />,
      },
    ]
  }
])

function App() {
  return <RouterProvider router={router} />
}

export default App