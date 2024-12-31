import React, { useContext } from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import Basic from "./routes/basic";
import Login from "./routes/login";


function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Basic />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}

export default AppRoutes;
