import React from "react";
import Filter from "../components/Filter";
import styled from "styled-components";
import SearchBar from "../components/SearchBar";
import Products from "../components/Products";
import { products } from "../data/products";
import Pagination from "@mui/material/Pagination";

const StyledMain = styled.main`
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  @media (min-width: 768px) {
    display: grid;
    grid-template-columns: 18rem 1fr;
    gap: 1rem;
    align-items: flex-start;
  }
`;

export default function Home() {
  return (
    <StyledMain>
      <Filter />
      <div className="flex flex-col w-full p-4">
        <SearchBar />
        <section className="flex flex-col justify-between align-middle items-center gap-4 p-4 w-full">
          <Products products={products} />
          <Pagination
            count={1}
            color="primary"
            size="large"
            shape="circle"
            className="mt-4"
          />
        </section>
      </div>
    </StyledMain>
  );
}
