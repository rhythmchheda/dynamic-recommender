import React, { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000/products";

export default function Dashboard() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        // ✅ Step 1: Filter out products with no valid images
        const filtered = data.filter((p) => {
          if (!p.IMAGE_URLS) return false;
          const img = p.IMAGE_URLS.split(",")[0]?.trim();
          if (!img) return false;
          const invalid = ["placeholder", "loading", "default", "noimage"];
          return !invalid.some((word) => img.toLowerCase().includes(word));
        });

        // ✅ Step 2: Deduplicate by PRODUCT_ID and TITLE
        const seen = new Set();
        const unique = filtered.filter((p) => {
          const key = `${p.PRODUCT_ID}_${p.TITLE}`;
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        });

        // ✅ Step 3: Add random prices and ratings
        const withExtras = unique.map((p) => ({
          ...p,
          PRICE: p.PRICE || (Math.random() * 450 + 50).toFixed(2),
          RATING: p.RATING || (Math.random() * 2 + 3).toFixed(1),
        }));

        setProducts(withExtras);
      })
      .catch((err) => console.error("Error loading products:", err));
  }, []);

  return (
    <div
      style={{
        backgroundColor: "#0b1622",
        color: "white",
        minHeight: "100vh",
        padding: "40px 0",
        fontFamily: "Inter, sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center", fontSize: "1.8rem", marginBottom: 30 }}>
        Dynamic Recommender Dashboard
      </h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
          gap: "30px",
          justifyContent: "center",
          alignItems: "stretch",
          maxWidth: "1100px",
          margin: "0 auto",
        }}
      >
        {products.map((p) => {
          const image = p.IMAGE_URLS?.split(",")[0]?.trim();
          return (
            <div
              key={p.PRODUCT_ID}
              style={{
                backgroundColor: "#12273d",
                borderRadius: "15px",
                overflow: "hidden",
                boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
                transition: "transform 0.2s",
                cursor: "pointer",
              }}
              onClick={() => window.open(`/product/${p.PRODUCT_ID}`, "_blank")}
              onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.03)")}
              onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1.0)")}
            >
              <img
                src={image}
                alt={p.TITLE}
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
                  {p.TITLE || "Untitled"}
                </h3>
                <p
                  style={{
                    fontSize: "0.85rem",
                    color: "#94a3b8",
                    marginBottom: "6px",
                  }}
                >
                  {p.BRAND || "Unknown Brand"}
                </p>
                <p
                  style={{
                    fontWeight: "600",
                    color: "#38bdf8",
                    marginBottom: "4px",
                  }}
                >
                  ${p.PRICE}
                </p>
                <p style={{ fontSize: "0.85rem", color: "#facc15" }}>
                  ⭐ {p.RATING}/5
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {products.length === 0 && (
        <p
          style={{
            textAlign: "center",
            marginTop: "80px",
            color: "#94a3b8",
            fontSize: "1rem",
          }}
        >
          No products available at the moment.
        </p>
      )}
    </div>
  );
}
