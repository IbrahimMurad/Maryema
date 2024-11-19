import React from "react";
import Header from "./Header";
import { Outlet } from "react-router-dom";

export default function MainLayout() {
  console.log("MainLayout rendered");

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <Outlet />
      <footer className="border-t-2 border-t-slate-600 h-10"></footer>
    </div>
  );
}
