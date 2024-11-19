import React from "react";
import loginImgLg from "../../images/login-image-lg.jpg";
import loginImgSm from "../../images/login-image-sm.png";
import { NavLink } from "react-router-dom";

// A wrapper component for login and register page
export default function Auth({ children }) {
  return (
    <main className="flex h-screen bg-slate-100 items-center">
      <div className="flex flex-1 min-h-fit justify-center lg:px-8">
        <div className="grid grid-cols-5 max-w-lg bg-white rounded-2xl shadow-lg mx-5 md:max-w-6xl">
          <div className="hidden md:block md:col-span-3">
            <img
              src={loginImgLg}
              alt="Muslim women wearing a hijab"
              className="rounded-l-2xl object-cover"
            />
          </div>
          <div className="col-span-full flex flex-col justify-between items-center min-w-full my-4 px-10 md:col-span-2 md:pt-5  md:px-12">
            <div className="relative w-[180px] h-[80px] md:hidden">
              <img
                src={loginImgSm}
                alt="Muslim women wearing a hijab"
                className="rounded-full h-[180px] w-[180px] shadow-lg absolute  -top-24"
              />
            </div>
            {children}
          </div>
        </div>
      </div>
    </main>
  );
}

export function ErrorMessages({ messages }) {
  return (
    <>
      {messages.map((message) => (
        <p className="text-red-600 text-sm mt-1 ml-2">{message}</p>
      ))}
    </>
  );
}

export function AuthHeader({ children }) {
  return <h2 className="text-xl font-semibold my-6 md:text-3xl">{children}</h2>;
}

export function AuthFooter({ question, link, linkText }) {
  return (
    <div className="mb-5 md:text-lg md:font-semibold">
      {question}
      <NavLink
        to={link}
        className="pl-2 text-indigo-600 hover:text-indigo-700 font-semibold md:font-bold bg-transparent border-none cursor-pointer hover:underline"
      >
        {linkText}
      </NavLink>
    </div>
  );
}
