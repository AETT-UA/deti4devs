import React from "react";
import Navbar from "./Navbar";
export default function BaseLayout({ children }) {
  return (
    <>
      <Navbar />
      {children}
    </>
  );
}
