import * as React from "react";
import { Box, Stack, Typography, IconButton, Card, CardMedia, Tooltip } from "@mui/material";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

const parseFirst = (urls) => (urls ? urls.split(",")[0]?.trim() : null);

export default function SimilarStrip({ title = "Similar products", items = [], onSelect }) {
  const ref = React.useRef(null);

  const scroll = (dir) => {
    if (!ref.current) return;
    ref.current.scrollBy({ left: dir * 400, behavior: "smooth" });
  };

  if (!items.length) {
    return (
      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
        No similar products found.
      </Typography>
    );
  }

  return (
    <Box sx={{ position: "relative", mt: 3 }}>
      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 1 }}>
        <Typography variant="h6">{title}</Typography>
        <Stack direction="row" spacing={1}>
          <IconButton onClick={() => scroll(-1)}><ChevronLeftIcon /></IconButton>
          <IconButton onClick={() => scroll(1)}><ChevronRightIcon /></IconButton>
        </Stack>
      </Stack>
      <Box
        ref={ref}
        sx={{
          display: "flex",
          gap: 2,
          overflowX: "auto",
          scrollBehavior: "smooth",
          pb: 1,
        }}
      >
        {items.map((p) => (
          <Card
            key={p.PRODUCT_ID}
            onClick={() => onSelect?.(p)}
            sx={{ minWidth: 180, cursor: "pointer" }}
            variant="outlined"
          >
            <CardMedia
              component="img"
              image={parseFirst(p.IMAGE_URLS) || "https://via.placeholder.com/300x300?text=No+Image"}
              alt={p.TITLE || "Product"}
              sx={{ aspectRatio: "1 / 1", objectFit: "contain" }}
            />
            <Tooltip title={p.TITLE || ""}>
              <Typography variant="body2" noWrap sx={{ p: 1 }}>{p.TITLE}</Typography>
            </Tooltip>
          </Card>
        ))}
      </Box>
    </Box>
  );
}
