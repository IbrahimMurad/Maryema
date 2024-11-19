import React, { useState } from "react";

export function PersonalInfoForm({ data }) {
  return (
    <form className="space-y-12 w-full pt-8">
      <div className="border-b border-gray-900/10 pb-8 px-4 mx-2">
        <legend className="text-xl font-bold text-gray-900 pt-4">
          Personal Information
        </legend>
        <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div className="sm:col-span-3">
            <label
              htmlFor="username"
              className="block text-sm/6 font-medium text-gray-900"
            >
              username
            </label>
            <div className="mt-2">
              <input
                id="username"
                name="username"
                type="text"
                value={data?.username}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
          </div>
          <div className="sm:col-span-3 sm:col-start-1">
            <label
              htmlFor="first-name"
              className="block text-sm/6 font-medium text-gray-900"
            >
              First name
            </label>
            <div className="mt-2">
              <input
                id="first-name"
                name="first-name"
                type="text"
                value={data?.first_name}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
          </div>

          <div className="sm:col-span-3">
            <label
              htmlFor="last-name"
              className="block text-sm/6 font-medium text-gray-900"
            >
              Last name
            </label>
            <div className="mt-2">
              <input
                id="last-name"
                name="last-name"
                type="text"
                value={data?.last_name}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
          </div>

          <div className="sm:col-span-4">
            <label
              htmlFor="email"
              className="block text-sm/6 font-medium text-gray-900"
            >
              Email
            </label>
            <div className="mt-2">
              <input
                id="email"
                name="email"
                type="email"
                value={data?.email}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
          </div>
          <div className="sm:col-span-4">
            <label
              htmlFor="phone-number"
              className="block text-sm/6 font-medium text-gray-900"
            >
              Phone number
            </label>
            <div className="mt-2">
              <input
                id="phone-number"
                name="phone-number"
                type="tel"
                value={data?.phone_number}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
          </div>
        </div>
        <div className="mt-8 flex items-center justify-end gap-x-6">
          <button
            type="button"
            className="rounded-md bg-gray-100 px-3 py-2 text-sm font-semibold text-black shadow-sm hover:bg-gray-500 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Save
          </button>
        </div>
      </div>
    </form>
  );
}

export function ChangePasswordForm() {
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  return (
    <form className="space-y-12 w-full pt-8">
      <div className="border-b border-gray-900/10 pb-8 px-4 mx-2">
        <legend className="text-xl font-bold text-gray-900">
          Change password
        </legend>
        <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div className="sm:col-span-3 sm:col-start-1">
            <label
              htmlFor="old-password"
              className="block text-sm/6 font-medium text-gray-900"
            >
              Old password
            </label>
            <div className="relative mt-2">
              <input
                id="old-password"
                name="old-password"
                type={showOldPassword ? "text" : "password"}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
              <button
                type="button"
                onClick={() => setShowOldPassword(!showOldPassword)}
                className="absolute top-1/4 right-0 pr-3 flex items-center text-sm leading-5"
              >
                {showOldPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>
          <div className="sm:col-span-3 sm:col-start-1">
            <label
              htmlFor="new-password"
              className="block text-sm/6 font-medium text-gray-900"
            >
              New password
            </label>
            <div className="relative mt-2">
              <input
                id="new-password"
                name="new-password"
                type={showNewPassword ? "text" : "password"}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
              <button
                type="button"
                onClick={() => setShowNewPassword(!showNewPassword)}
                className="absolute top-1/4 right-0 pr-3 flex items-center text-sm leading-5"
              >
                {showNewPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          <div className="sm:col-span-3 sm:col-start-1">
            <label
              htmlFor="confirm-password"
              className="block text-sm/6 font-medium text-gray-900"
            >
              Confirm new password
            </label>
            <div className="relative mt-2">
              <input
                id="confirm-password"
                name="confirm-password"
                type={showConfirmPassword ? "text" : "password"}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute top-1/4 right-0 pr-3 flex items-center text-sm leading-5"
              >
                {showConfirmPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>
        </div>
        <div className="mt-8 flex items-center justify-end gap-x-6">
          <button
            type="button"
            className="rounded-md bg-gray-100 px-3 py-2 text-sm font-semibold text-black shadow-sm hover:bg-gray-500 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Save
          </button>
        </div>
      </div>
    </form>
  );
}

export function DeleteAccount() {
  return (
    <div className="py-8 px-4 mx-2">
      <legend className="text-xl font-bold text-gray-900">
        Delete Account
      </legend>
      <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
        <div className="sm:col-span-3">
          <label
            htmlFor="password"
            className="block text-sm/6 font-medium text-gray-900"
          >
            Password
          </label>
          <div className="mt-2">
            <input
              id="password"
              name="password"
              type="password"
              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
            />
          </div>
        </div>
      </div>
      <div className="mt-8 flex items-center justify-end gap-x-6">
        <button
          type="button"
          className="rounded-md bg-gray-100 px-3 py-2 text-sm font-semibold text-black shadow-sm hover:bg-gray-500 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600"
        >
          Delete Account
        </button>
      </div>
    </div>
  );
}
