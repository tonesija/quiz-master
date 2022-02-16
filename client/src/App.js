import Profile from "./components/Profile";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import { ThemeProvider, createTheme } from "@mui/material/styles";

// App theme
const theme = createTheme({
  palette: {
    primary: {
      main: "#27187E",
    },
    secondary: {
      main: "#AEB8FE",
    },
    accent: {
      main: "#FF8600",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Navbar />
        <Routes>
          <Route element={<Profile />} path="/"></Route>
          <Route element={<p>TODO tmp</p>} path="/questions"></Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
