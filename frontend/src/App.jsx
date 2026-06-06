import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import VideoDetails from "./pages/VideoDetails";
import MeteorBackground from "./components/MeteorBackground";
import "./App.css";

function App() {
  return (
    <>
      <MeteorBackground />
      <Routes>
        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/video/:videoId"
          element={<VideoDetails />}
        />
      </Routes>
    </>
  );
}

export default App;
