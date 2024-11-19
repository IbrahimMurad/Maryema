import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";

const MenuButton = styled.input`
  display: none;
`;

const MenuLabel = styled.label`
  cursor: pointer;
  border-radius: 8%;
  padding: 1rem;
  display: block;
  position: relative;
  user-select: none;
`;

const NavIcon = styled.span`
  display: block;
  width: 1.8rem;
  height: 0.18rem;
  position: relative;
  border-radius: 0.25rem;
  background-color: rgb(120, 120, 120);
  transition: background-color 0.2s ease-out;

  &::before,
  &::after {
    content: "";
    display: block;
    width: 100%;
    height: 100%;
    position: absolute;
    border-radius: 0.2rem;
    background-color: rgb(120, 120, 120);
    transition: all 0.2s ease-out;
  }

  &::before {
    top: 0.5rem;
  }

  &::after {
    top: -0.5rem;
  }

  ${MenuButton}:checked + ${MenuLabel} & {
    background-color: transparent;
  }

  ${MenuButton}:checked + ${MenuLabel} &::before {
    transform: rotate(-45deg);
    top: 0;
  }

  ${MenuButton}:checked + ${MenuLabel} &::after {
    transform: rotate(45deg);
    top: 0;
  }
`;

const StyledMenu = styled.nav`
  position: absolute;
  flex: 1 1 auto;
  min-width: fit-content;
  max-width: 50%;
  margin: 0 10px;
  height: 100svh;
  left: ${({ isVisible }) => (isVisible ? "-1rem" : "-16rem")};
  z-index: 10;
  background-color: #ddd;
  transition: left 0.5s ease-out;
  top: 3.3rem;
  z-index: 2;

  @media (min-width: 768px) {
    display: flex;
    position: relative;
    top: 0;
    left: 0;
    justify-content: center;
    background: none;
    height: 100%;
  }

  ul {
    display: flex;
    flex-direction: column;
    list-style: none;
    padding-right: 0.6rem;
    padding-left: 0.6rem;
    height: 100%;
    background-color: lightgray;
    @media (min-width: 768px) {
      flex-direction: row;
      margin: auto 0;
      justify-content: center;
      max-width: 80%;
      height: 100%;
      background-color: transparent;
    }
  }

  li {
    display: flex;
    padding: 1rem;
    width: 12rem;
    cursor: pointer;
    transition: background-color 0.3s ease-out;
    border-radius: 0.5rem;
    font-weight: 500;

    @media (min-width: 768px) {
      align-items: center;
      justify-content: center;
      border-radius: 0;
      padding: 0% 1rem;
    }

    &:hover {
      background-color: rgb(200, 200, 200);
      font-size: 1.1rem;
      font-weight: 600;
    }
  }

  li + li {
    border-left: none;
    border-top: 1px solid rgb(200, 200, 200);
    @media (min-width: 768px) {
      border-left: 1px solid rgb(200, 200, 200);
      border-radius: 0;
      border-top: none;
    }
  }
`;

export function MenuIcon({ isChecked, onToggle }) {
  return (
    <div className="block cursor-pointer md:hidden z-10">
      <MenuButton
        id="menu-btn"
        type="checkbox"
        checked={isChecked}
        onChange={onToggle}
      />
      <MenuLabel htmlFor="menu-btn">
        <span className="sr-only">Open menu</span>
        <NavIcon />
      </MenuLabel>
    </div>
  );
}

export function MenuDrower({ isVisible }) {
  return (
    <StyledMenu isVisible={isVisible}>
      <ul>
        <li>
          <Link to="/">All products</Link>
        </li>
        <li>New products</li>
        <li>Best sells</li>
        <li>On sale</li>
      </ul>
    </StyledMenu>
  );
}
