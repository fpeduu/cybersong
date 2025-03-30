import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SongList from "./pages/SongList";
import Navbar from "./components/Navbar";
import Video from "./pages/Video";

function AppRoutes() {
  const showNavbar = location.pathname !== "/";
  return (
    <Router>
      {showNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/song-list" element={<SongList />} />
        <Route path="/video-result" element={<Video />} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
