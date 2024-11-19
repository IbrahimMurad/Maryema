import React, { useEffect, useState } from "react";
import ProductVariants from "./ProductVariants";
import { Link } from "react-router-dom";
import AddShoppingCartOutlinedIcon from "@mui/icons-material/AddShoppingCartOutlined";
import ListItemIcon from "@mui/material/ListItemIcon";

export default function ProductCard({ product }) {
  const [selectedColor, setSelectedColor] = useState(product.colors[0]);
  const [selectedSize, setSelectedSize] = useState(product.colors[0].sizes[0]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    setSelectedSize(selectedColor.sizes[0]);
  }, [selectedColor]);

  return (
    <div className="flex flex-col bg-slate-50 h-fit w-80 rounded-lg shadow-lg hover:ring-indigo-400 hover:ring-1 m-2 p-2 overflow-visible">
      <div className="relative bg-white rounded-md">
        <img
          src={product.imgUrl || "placeholder.jpg"}
          alt={product.title || "No title"}
          className="h-48 w-full object-scale-down transition duration-300 cursor-pointer"
          onClick={() => setIsModalOpen(true)}
        />
      </div>
      {isModalOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          onClick={() => setIsModalOpen(false)}
        >
          <img
            src={product.imgUrl || "placeholder.jpg"}
            alt={product.title || "No title"}
            className="max-h-full max-w-full object-cover"
          />
        </div>
      )}

      <Link to={`/products/${product.title}`}>
        <h1 className="text-lg text-indigo-600 font-extrabold border-t-2 border-gray-200 m-4 py-2 text-center cursor-pointer">
          {product.title || "No title"}
        </h1>
      </Link>

      <div className="m-2 font-bold">Colors : </div>
      <ProductVariants
        type="color"
        variants={product.colors}
        selectedVariant={selectedColor}
        setSelectedVariant={setSelectedColor}
      />
      <div className="m-2 font-bold">Sizes : </div>
      <ProductVariants
        type="size"
        variants={selectedColor.sizes}
        selectedVariant={selectedSize}
        setSelectedVariant={setSelectedSize}
      />
      <div className="m-2 py-2 flex flex-row justify-between items-center w-full">
        <span className="font-bold">Price:</span>
        <span className="m-2 text-lg font-bold">
          {selectedSize.price || "N/A"} $
        </span>
      </div>
      <div className="border-gray-300 border-t-2 py-4 flex justify-center bg-gray-50">
        <button className="bg-blue-500 text-white flex flex-row items-center font-semibold py-2 px-6 rounded-lg shadow-lg hover:bg-blue-600 transition duration-300 transform hover:scale-105">
          <ListItemIcon>
            <AddShoppingCartOutlinedIcon style={{ color: "white" }} />
          </ListItemIcon>
          Add to cart
        </button>
      </div>
    </div>
  );
}
