// Dark Amazon-inspired theme
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#FF9900" },        // Amazon amber
    secondary: { main: "#232F3E" },      // Amazon navy
    background: {
      default: "#0B1320",                // page
      paper: "#1B2433",                  // cards
    },
    text: {
      primary: "#E6EAF2",
      secondary: "#B7C0CE",
    },
  },
  shape: { borderRadius: 14 },
  typography: {
    fontFamily: '"Inter", system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"',
    h4: { fontWeight: 800, letterSpacing: 0.2 },
    h6: { fontWeight: 700 },
    button: { textTransform: "none", fontWeight: 700 },
  },
  components: {
    MuiCard: { styleOverrides: { root: { border: "1px solid rgba(255,255,255,0.06)" } } },
    MuiAppBar: { styleOverrides: { root: { background: "#232F3E" } } },
  },
});

export default theme;
