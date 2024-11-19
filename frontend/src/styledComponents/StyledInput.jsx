import styled from "styled-components";

const StyledInput = styled.input`
  margin-top: 0.25rem;
  display: block;
  width: 100%;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  --tw-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --tw-shadow-colored: 0 1px 2px 0 var(--tw-shadow-color);
  box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),
    var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow);

  &:focus {
    outline: 2px solid transparent;
    outline-offset: 2px;
    border-color: #6366f1;
  }

  @media (min-width: 640px) {
    font-size: 0.875rem;
    line-height: 1.25rem;
  }
`;

export default StyledInput;
