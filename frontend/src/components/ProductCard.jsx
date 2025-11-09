import React from "react";
import { useNavigate } from "react-router-dom";

export default function ProductCard({ product }) {
  const navigate = useNavigate();

  if (!product || !product.IMAGE_URLS) return null;
  const image = product.IMAGE_URLS.split(",")[0];

  return (
    <div
      style={{
        backgroundColor: "#12273d",
        borderRadius: "15px",
        overflow: "hidden",
        boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
        transition: "transform 0.2s",
        cursor: "pointer",
      }}
      onClick={() => navigate(`/product/${product.PRODUCT_ID}`)}
      onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.03)")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1.0)")}
    >
      <img
        src={image}
        alt={product.TITLE}
        style={{
          width: "100%",
          height: "230px",
          objectFit: "cover",
          backgroundColor: "#0b1622",
        }}
        onError={(e) => (e.target.style.display = "none")}
      />
      <div style={{ padding: "15px" }}>
        <h3
          style={{
            fontSize: "0.95rem",
            fontWeight: "600",
            color: "#e2e8f0",
            marginBottom: "8px",
            height: "2.4em",
            overflow: "hidden",
          }}
        >
          {product.TITLE || "Untitled"}
        </h3>
        <p style={{ fontSize: "0.85rem", color: "#94a3b8", marginBottom: "6px" }}>
          {product.BRAND || "Unknown Brand"}
        </p>
        <p
          style={{
            fontWeight: "600",
            color: "#38bdf8",
            marginBottom: "4px",
          }}
        >
          ${product.PRICE}
        </p>
        <p style={{ fontSize: "0.85rem", color: "#facc15" }}>⭐ {product.RATING}/5</p>
      </div>
    </div>
  );
}
