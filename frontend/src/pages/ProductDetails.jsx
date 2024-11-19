import React, { useState, useEffect } from "react";
import ProductVariants from "../components/ProductVariants";
import { products } from "../data/products";
import styled from "styled-components";
import AddShoppingCartOutlinedIcon from "@mui/icons-material/AddShoppingCartOutlined";
import ListItemIcon from "@mui/material/ListItemIcon";

const StyledMain = styled.main`
  display: flex;
  justify-content: center;
  align-self: center;
  margin-top: 2rem;
  @media (min-width: 768px) {
    margin-top: 2rem;
    width: 50%;
  }
`;

const StyledProductDetails = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  justify-items: start;
  width: 20rem;
  @media (min-width: 768px) {
    display: grid;
    width: 100%;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: repeat(10, 1fr);
    gap: 1rem;
    align-items: center;
  }
`;

const StyledHeader = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
  font-weight: 700;
  @media (min-width: 768px) {
    grid-column-start: 1;
    grid-row-start: 1;
  }
`;

export default function ProductDetails({ slug }) {
  const product = products.find((product) => product.title === slug);
  const [selectedColor, setSelectedColor] = useState(product.colors[0]);
  const [selectedSize, setSelectedSize] = useState(product.colors[0].sizes[0]);

  useEffect(() => {
    setSelectedSize(selectedColor.sizes[0]);
  }, [selectedColor]);

  return (
    <StyledMain>
      <StyledProductDetails>
        <StyledHeader className="mb-4">
          <h1>{product.title}</h1>
        </StyledHeader>
        <div className="sm:col-start-2 sm:row-start-1 sm:row-span-8 justify-self-center place-self-start">
          <img src={product.imgUrl} alt={product.title} />
        </div>
        <div className="sm:col-start-1 sm:row-start-2">
          <div className="text-2xl font-bold mb-1">Colors : </div>
          <ProductVariants
            detailed={true}
            variants={product.colors}
            selectedVariant={selectedColor}
            setSelectedVariant={setSelectedColor}
          />
        </div>
        <div className="justify-self-start">
          <div className="text-2xl font-bold mb-1">Sizes : </div>
          <ProductVariants
            detailed={true}
            variants={selectedColor.sizes}
            selectedVariant={selectedSize}
            setSelectedVariant={setSelectedSize}
          />
        </div>
        <div className="flex flex-row justify-between items-center w-full text-2xl font-bold">
          <span>Price:</span>
          <span>{selectedSize.price || "N/A"} $</span>
        </div>
        <div className="border-gray-300 w-full pb-4 flex justify-center">
          <button className="bg-blue-500 text-white flex flex-row items-center font-semibold py-2 px-6 rounded-lg shadow-lg hover:bg-blue-600 transition duration-300 transform hover:scale-105">
            <ListItemIcon>
              <AddShoppingCartOutlinedIcon style={{ color: "white" }} />
            </ListItemIcon>
            Add to cart
          </button>
        </div>
      </StyledProductDetails>
    </StyledMain>
  );
}
