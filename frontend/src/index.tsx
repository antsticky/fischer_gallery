import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./route.tsx";

const rootElement = document.getElementById("root");

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<AppRoutes />);
} else {
  console.error("Could not find root element to mount to!");
}
