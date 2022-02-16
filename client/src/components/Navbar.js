import React from "react";
import Button from "@mui/material/Button";
import LoginButton from "./LoginButton";
import LogoutButton from "./LogoutButton";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import PhotoCamera from "@mui/icons-material/PhotoCamera";

const pages = ["Questions", "Quizzes", "Groups"];

const Navbar = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <PhotoCamera color="accent" />
          </IconButton>
          <Typography variant="h5" component="div">
            Quiz Master
          </Typography>
          <Box
            sx={{
              flexGrow: 1,
              display: { xs: "none", md: "flex" },
              marginLeft: 5,
            }}
          >
            {pages.map((page) => (
              <Button
                key={page}
                href={page.toLowerCase()}
                sx={{ my: 2, color: "white", display: "block" }}
              >
                {page}
              </Button>
            ))}
          </Box>
          <LoginButton />
          <LogoutButton />
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;
