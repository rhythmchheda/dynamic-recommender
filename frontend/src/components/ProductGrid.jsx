import * as React from "react";
import { Grid2 as Grid, Skeleton } from "@mui/material";
import ProductCard from "./ProductCard";

export default function ProductGrid({ items, loading, onSelect }) {
  if (loading) {
    return (
      <Grid container spacing={2}>
        {Array.from({ length: 12 }).map((_, i) => (
          <Grid key={i} size={{ xs: 12, sm: 6, md: 3 }}>
            <Skeleton variant="rounded" height={260} />
          </Grid>
        ))}
      </Grid>
    );
  }

  return (
    <Grid container spacing={2}>
      {items.map((p) => (
        <Grid key={p.PRODUCT_ID} size={{ xs: 12, sm: 6, md: 3 }}>
          <ProductCard product={p} onClick={onSelect} />
        </Grid>
      ))}
    </Grid>
  );
}
