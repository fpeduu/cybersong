import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SongList from "./pages/SongList";
import Navbar from "./components/Navbar";

function AppRoutes() {
  const showNavbar = location.pathname !== "/";
  return (
    <Router>
      {showNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/song-list" element={<SongList />} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
