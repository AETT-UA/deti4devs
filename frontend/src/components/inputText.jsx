import React from "react";

export const InputText = ({ placeholder, className }) => {
  return (
    <input
      className={`p-3 bg-gray-primary ${className}`}
      type="text"
      placeholder={placeholder}
    />
  );
};
