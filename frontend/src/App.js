import React from "react";
import { jwtDecode } from 'jwt-decode';
import { Navigate } from 'react-router-dom';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import MainPage from "./pages/MainPage";
import ErrorPage from "./pages/ErrorPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import PatientHomePage from "./pages/PatientHomePage"; 
import HospitalHomePage from "./pages/HospitalHomePage"; 
import HospitalInvPage from "./pages/HospitalInvPage"; 
import WholesalerHomePage from "./pages/WholesalerHomePage"; 
import WholesalerInvPage from "./pages/WholesalerInvPage"; 
import ManufacturerHomePage from "./pages/ManufacturerHomePage"; 
import ManufacturerInvPage from "./pages/ManufacturerInvPage"; 
import ManufacturerItemPage from "./pages/ManufacturerItemPage"; 
//import Navbar from "./components/Navbar";

// const isAuthenticated = () => {
//   const token = localStorage.getItem('token');
//   if (!token) {
//     return false;
//   }
//   return true
// };

// const RequireAuth = ({ children }) => {
//   if (!isAuthenticated()) {
//     return <Navigate to="/error" replace />;
//   }
//   return children;
// };

const isAuthenticated = (expectedRole) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return false;
  }
  try {
    console.log("expect to be ",expectedRole," in this route.")
    const decoded = jwtDecode(token);
    console.log("token username decode as: ",decoded.username)
    console.log("token identity decode as: ",decoded.sub)
    const currentRole = decoded.sub;
    return currentRole === expectedRole;
  } catch (error) {
    console.error('Error decoding token:', error);
    return false;
  }
};

const RequireAuth = ({ children, role }) => {
  if (!isAuthenticated(role)) {
    return <Navigate to="/error" replace />;
  }
  return children;
};

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/error" element={<ErrorPage />} />
          <Route path="/" element={<MainPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/patient/homepage" element={<PatientHomePage />} />
          <Route path="/hospital/homepage" element={<RequireAuth role="hospital"><HospitalHomePage /></RequireAuth>} />
          <Route path="/hospital/inventory" element={<RequireAuth role="hospital"><HospitalInvPage /></RequireAuth>} />
          <Route path="/wholesaler/homepage" element={<RequireAuth role="wholesaler"><WholesalerHomePage /></RequireAuth>} />
          <Route path="/wholesaler/inventory" element={<RequireAuth role="wholesaler"><WholesalerInvPage /></RequireAuth>} />
          <Route path="/manufacturer/homepage" element={<RequireAuth role="manufacturer"><ManufacturerHomePage /></RequireAuth>} />
          <Route path="/manufacturer/inventory" element={<RequireAuth role="manufacturer"><ManufacturerInvPage /></RequireAuth>} />
          <Route path="/manufacturer/items" element={<RequireAuth role="manufacturer"><ManufacturerItemPage /></RequireAuth>} />
        </Routes>
      </Router>
  );
}

export default App;

