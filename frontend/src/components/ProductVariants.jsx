import React, { useRef, useEffect } from "react";
import { RadioGroup, Radio } from "@headlessui/react";
import { handleXScroll } from "../utils/handleXScroll";
import PropTypes from "prop-types";
import styled from "styled-components";

export default function ProductVariants({
  detailed,
  variants,
  selectedVariant,
  setSelectedVariant,
}) {
  const StyledRadioGroup = styled(RadioGroup)`
    display: flex;
    flex-direction: row;
    font-size: ${detailed ? "1.25rem" : "1rem"};
    flex-wrap: ${detailed ? "wrap" : "nowrap"};
    ${!detailed && "overflow-x: scroll;"}

    &::-webkit-scrollbar {
      height: 6px;
    }
    &::-webkit-scrollbar-track {
      border-radius: 100vh;
      background: #aeebff;
    }
    &::-webkit-scrollbar-thumb {
      background: #3ba0ff;
      border-radius: 100vh;
      border: none;
    }
    &::-webkit-scrollbar-thumb:hover {
      background: #311ffc;
    }
  `;

  const variantRef = useRef(null);
  useEffect(() => {
    const variantElement = variantRef.current;
    variantElement.addEventListener("wheel", handleXScroll, { passive: false });
    return () => {
      variantElement.removeEventListener("wheel", handleXScroll);
    };
  });

  return (
    <>
      <StyledRadioGroup
        value={selectedVariant}
        onChange={setSelectedVariant}
        ref={variantRef}
      >
        {variants && variants.length > 0 ? (
          variants.map((variant) => (
            <Radio
              key={variant.name}
              value={variant}
              className="group relative flex cursor-pointer rounded-lg bg-white/5 px-2 py-1 m-2 shadow-md transition focus:outline-none data-[focus]:outline-1 data-[focus]:outline-black data-[checked]:bg-white data-[checked]:text-gray-700 data-[checked]:font-bold data-[checked]:ring-2 data-[checked]:ring-blue-500 data-[checked]:ring-opacity-60 data-[checked]:ring-offset-2 hover:bg-gray-100"
            >
              {variant.name}
            </Radio>
          ))
        ) : (
          <li className="text-gray-500">No variants available</li>
        )}
      </StyledRadioGroup>
    </>
  );
}

ProductVariants.propTypes = {
  detailed: PropTypes.bool,
  variants: PropTypes.array,
  selectedVariant: PropTypes.object,
  setSelectedVariant: PropTypes.func,
};

ProductVariants.defaultProps = {
  detailed: false,
  variants: [],
  selectedVariant: {},
  setSelectedVariant: () => {},
};
