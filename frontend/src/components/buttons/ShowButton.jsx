import React from "react";

export default function ShowButton({ show, setShow }) {
  return (
    <button
      type="button"
      onClick={() => setShow(!show)}
      className="absolute top-1/2 right-0 pr-3 flex items-center text-sm leading-5"
    >
      {show ? "🙈" : "👁️"}
    </button>
  );
}
