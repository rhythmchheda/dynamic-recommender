import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

export default function ProductDetails() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [similar, setSimilar] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/products`)
      .then((res) => res.json())
      .then((data) => {
        const item = data.find((p) => p.PRODUCT_ID === id);
        setProduct(item);

        // ✅ Create random similar products that aren’t the same
        const others = data.filter((p) => p.PRODUCT_ID !== id && p.IMAGE_URLS);
        const randomThree = others.sort(() => 0.5 - Math.random()).slice(0, 3);
        setSimilar(randomThree);
      });
  }, [id]);

  if (!product)
    return (
      <div
        style={{
          color: "white",
          textAlign: "center",
          marginTop: "100px",
        }}
      >
        Loading...
      </div>
    );

  const img = product.IMAGE_URLS?.split(",")[0];

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
      <div style={{ maxWidth: "1000px", margin: "0 auto" }}>
        <Link
          to="/"
          style={{
            color: "#38bdf8",
            textDecoration: "none",
            marginBottom: "20px",
            display: "inline-block",
          }}
        >
          ← Back to Dashboard
        </Link>

        <div
          style={{
            display: "flex",
            gap: "40px",
            alignItems: "center",
            backgroundColor: "#12273d",
            borderRadius: "20px",
            padding: "30px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.2)",
          }}
        >
          <img
            src={img}
            alt={product.TITLE}
            style={{
              width: "350px",
              height: "350px",
              objectFit: "cover",
              borderRadius: "10px",
            }}
          />
          <div>
            <h1 style={{ fontSize: "1.5rem", marginBottom: "10px" }}>
              {product.TITLE}
            </h1>
            <p style={{ color: "#94a3b8", marginBottom: "10px" }}>
              {product.BRAND}
            </p>
            <p style={{ color: "#38bdf8", fontWeight: "600", marginBottom: "10px" }}>
              ${product.PRICE}
            </p>
            <p style={{ color: "#facc15" }}>⭐ {product.RATING}/5</p>
          </div>
        </div>

        <h2 style={{ marginTop: "50px", marginBottom: "20px" }}>Similar Products</h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
            gap: "30px",
          }}
        >
          {similar.map((p, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: "#12273d",
                borderRadius: "15px",
                overflow: "hidden",
                boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
              }}
            >
              <img
                src={p.IMAGE_URLS?.split(",")[0]}
                alt={p.TITLE}
                style={{
                  width: "100%",
                  height: "230px",
                  objectFit: "cover",
                  backgroundColor: "#0b1622",
                }}
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
                <p style={{ fontSize: "0.85rem", color: "#94a3b8" }}>
                  {p.BRAND || "Unknown Brand"}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
