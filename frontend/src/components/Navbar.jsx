import { AppBar, Toolbar, Typography, Box } from "@mui/material";

export default function Navbar() {
  return (
    <AppBar position="sticky" elevation={0}>
      <Toolbar sx={{ maxWidth: 1320, mx: "auto", width: "100%" }}>
        <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: 0.4 }}>
          Dynamic Recommender
        </Typography>
        <Box sx={{ flex: 1 }} />
        <Typography variant="body2" sx={{ opacity: 0.8 }}>
          API: {import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000"}
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
