import React from "react";

export default function SubmitButton({ children }) {
  return (
    <button
      type="submit"
      className="w-full px-3 py-2 text-white bg-indigo-600 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      {children}
    </button>
  );
}
