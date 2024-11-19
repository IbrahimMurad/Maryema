import React from "react";
import { Link } from "react-router-dom";
import NavLinks from "./NavLinks";

export default function SideNav() {
  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <Link
        className="mb-2 flex h-20 items-end justify-start rounded-md bg-blue-600 p-4 md:h-40"
        to="/admin"
      >
        <div className="w-32 text-white md:w-40">
          <div className="font-lusitana flex flex-row items-center leading-none text-white">
            <p className="ml-8 text-[44px] md:ml-2">Maryema</p>
          </div>
        </div>
      </Link>
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
        <NavLinks />
        <div className="hidden h-auto w-full grow rounded-md bg-gray-50 md:block"></div>
      </div>
    </div>
  );
}
