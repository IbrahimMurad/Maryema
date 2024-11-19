import styled from "styled-components";
import { FaSearch } from "react-icons/fa";
import PropTypes from "prop-types";

const SearchBox = styled.div`
  width: fit-content;
  height: fit-content;
  position: relative;
  align-self: center;
  background-color: white;
  border-radius: 999px;
  transition: top 0.3s ease;
  transition-delay: 0.5s;
  border: 2px solid lightgray;
`;

const InputSearch = styled.input`
  height: 45px;
  width: 50px;
  border-style: none;
  padding: 10px;
  outline: none;
  border-radius: 25px;
  transition: all 0.5s ease-in-out;
  background-color: white;
  padding-right: 40px;
  color: black;

  &::placeholder {
    color: gray;
    font-weight: 100;
  }

  &:focus {
    width: 280px;
    border-radius: 0px;
    background-color: transparent;
    transition: all 500ms cubic-bezier(0, 0.11, 0.35, 1.8);
  }
`;

const BtnSearch = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 45px;
  border-style: none;
  font-size: 20px;
  font-weight: bold;
  outline: none;
  cursor: pointer;
  border-radius: 50%;
  position: absolute;
  right: 0px;
  color: #ffffff;
  background-color: transparent;
  pointer-events: painted;

  &:focus ~ input {
    width: 280px;
    border-radius: 0px;
    background-color: transparent;
    transition: all 500ms cubic-bezier(0, 0.11, 0.35, 1.8);
  }
`;

export default function SearchBar() {
  return (
    <div className="p-2 self-center">
      <SearchBox>
        <BtnSearch>
          <FaSearch className="h-5 w-5 text-gray-400" />
        </BtnSearch>
        <InputSearch placeholder="Search..." />
      </SearchBox>
    </div>
  );
}

SearchBar.propTypes = {
  isOpen: PropTypes.bool,
};
