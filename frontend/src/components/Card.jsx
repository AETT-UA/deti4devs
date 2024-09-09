import React from "react";

export const Card = ({ title, description, company, className }) => {
  return (
    <>
      <div className={`w-full grid grid-cols-1  ${className}`}>
        <div className="text-sm text-white w-full text-left">{company}</div>
        <div className="text-2xl text-white text-left my-1">{title}</div>
        <div className="text-xs text-white text-left ">{description}</div>
      </div>
    </>
  );
};
