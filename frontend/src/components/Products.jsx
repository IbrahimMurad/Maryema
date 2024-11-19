import React from "react";
import ProductCard from "./ProductCard";

export default function Products({ products }) {
  return (
    <div className="flex flex-row flex-wrap justify-center">
      {products.map((product) => (
        <ProductCard product={product} />
      ))}
    </div>
  );
}
