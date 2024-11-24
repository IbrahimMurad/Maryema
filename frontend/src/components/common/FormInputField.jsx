import React from "react";
import PropTypes from "prop-types";
import TextField from "@mui/material/TextField";
import styled from "styled-components";

const StyledDiv = styled.div`
  @media (min-width: 640px) {
    grid-column: span 5 / span 5;
  }
  @media (min-width: 768px) {
    grid-column: span 4 / span 4;
  }
  @media (min-width: 1024px) {
    grid-column: span 3 / span 3;
  }
`;

export default function FormInputField({ name, value, label, ...props }) {
  return (
    <StyledDiv>
      <TextField
        label={label}
        variant="outlined"
        name={name}
        type={
          (name === "email" && "email") ||
          (name === "phone_number" && "tel") ||
          ([
            "password",
            "new_password",
            "old_password",
            "confirm_password",
          ].includes(name) &&
            "password") ||
          "text"
        }
        fullWidth={true}
        value={value}
        {...props}
      />
    </StyledDiv>
  );
}

FormInputField.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};
