import React, { useState } from "react";
import { FaChevronDown } from "react-icons/fa";
import styled from "styled-components";

const FilterContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 90%;
  justify-self: center;
  position: relative;
  background-color: #f3f4f6;
  border-radius: 0 0 0.5rem 0.5rem;

  @media (min-width: 768px) {
    min-width: 18rem;
    max-width: 20rem;
    position: sticky;
    left: 0;
    top: 4rem;
    height: 100%;
  }
`;

const FilterDropDown = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  background-color: #f3f4f6;
  min-height: fit-content;
  border: 2px solid #e5e7eb;
  border-radius: 0 0 0.5rem 0.5rem;
  padding: 0.5rem;
  z-index: 5;
  justify-content: space-between;
  box-shadow: 0 0 0.5rem 0.5rem #e5e7eb inset;

  span {
    font-weight: 700;
    margin-left: 0.5rem;
  }

  button {
    height: fit-content;
    width: fit-content;
    border: 2px solid #9ca3af;
    border-radius: 50%;
    padding: 0.25rem;
    cursor: pointer;
    background-color: transparent;
    margin-right: 0.25rem;

    @media (min-width: 768px) {
      display: none;
    }
  }
`;

const StyledFilterBody = styled.div`
  position: relative;
  width: 100%;
  overflow: hidden;
  height: ${(props) => (props.isDropedDown ? "28rem" : "0")};
  transition: height 0.7s ease-out;

  @media (min-width: 768px) {
    height: fit-content;
  }
`;

function ToggleButton({ isDropedDown, handleDropDown }) {
  return (
    <button
      onClick={handleDropDown}
      aria-expanded={isDropedDown}
      aria-controls="filter"
    >
      <FaChevronDown
        className={`h-5 w-5 transition-transform duration-700 ease-in-out ${
          isDropedDown && "rotate-180"
        }`}
      />
    </button>
  );
}

function DivisionFilter() {
  return (
    <>
      <label htmlFor="division" className="font-bold ml-2 col-span-2 w-fit">
        Division :
      </label>
      <div className="flex flex-col ml-4 col-start-2">
        <label className="mb-2">
          <input
            type="checkbox"
            name="division"
            value="electronics"
            className="m-2"
          />
          Clothes
        </label>
        <label className="mb-2">
          <input
            type="checkbox"
            name="division"
            value="jewelery"
            className="m-2"
          />
          Accessories
        </label>
      </div>
    </>
  );
}

function CategoryFilter() {
  return (
    <>
      <label htmlFor="category" className="font-bold  col-span-2 ml-2">
        Category
      </label>
      <select
        id="category"
        className="flex flex-col ml-4 max-w-[80%] p-2 rounded-md hover:ring-1 hover:ring-indigo-400 col-start-2"
      >
        <option value="All" key="All">
          All
        </option>
        <option value="Electronics" key="Electronics">
          Electronics
        </option>
        <option value="Jewelery" key="Jewelery">
          Jewelery
        </option>
        <option value="scart" key="scart">
          scart
        </option>
      </select>
    </>
  );
}

function PriceFilter() {
  return (
    <>
      <label className="font-bold ml-2 col-span-2 col-start-1">
        Price Range
      </label>
      <div className="col-start-2 grid grid-cols-[auto_1fr_2.5rem] gap-x-1 mt-2">
        <label htmlFor="price" className="col-span-3 font-bold">
          Min :
        </label>
        <input
          className="col-start-1 col-span-2"
          type="range"
          id="price"
          name="min-price"
          min={10}
          max={1000}
          step={5}
          defaultValue={10}
          onInput={(e) =>
            (e.target.nextElementSibling.textContent = e.target.value)
          }
        />
        <span className="relative">10</span>
      </div>
      <div className="col-start-2 grid grid-cols-[auto_1fr_2.5rem] gap-x-1 mt-2">
        <label htmlFor="price-from" className="col-span-3 font-bold">
          Max :
        </label>
        <input
          className="col-start-1 col-span-2"
          type="range"
          id="price-from"
          name="max-price"
          min={100}
          max={10000}
          step={20}
          defaultValue={100}
          onInput={(e) =>
            (e.target.nextElementSibling.textContent = e.target.value)
          }
        />
        <span>100</span>
      </div>
    </>
  );
}

export default function Filter() {
  const [isDropedDown, setIsDropDown] = useState(false);

  const handleDropDown = () => {
    setIsDropDown(!isDropedDown);
  };

  return (
    <FilterContainer>
      <FilterDropDown>
        <span>Filter</span>
        <ToggleButton
          isDropedDown={isDropedDown}
          handleDropDown={handleDropDown}
        />
      </FilterDropDown>
      <StyledFilterBody isDropedDown={isDropedDown} id="filter">
        <div className="grid grid-cols-[1rem_1fr] gap-y-2 items-start m-2">
          <DivisionFilter />
          <CategoryFilter />
          <PriceFilter />
        </div>
      </StyledFilterBody>
    </FilterContainer>
  );
}
