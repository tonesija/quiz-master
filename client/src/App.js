import Profile from "./components/Profile";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <Navbar />

      <Routes>
        <Route element={<Profile />} path="/"></Route>
        <Route element={<p>TODO tmp</p>} path="/questions"></Route>
      </Routes>
    </Router>
  );
}

export default App;
