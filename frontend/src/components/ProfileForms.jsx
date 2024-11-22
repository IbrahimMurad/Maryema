import React, { useState } from "react";
import { update, deleteProfile, changePassword } from "../data/profile";
import areEqual from "../utils/areEqual";
import { useNavigate } from "react-router-dom";

export function PersonalInfoForm({ data }) {
  const initialData = {
    username: data.username || "",
    first_name: data.first_name || "",
    last_name: data.last_name || "",
    email: data.email || "",
    phone_number: data.phone_number || "",
  };
  const [personalInfo, setPersonalInfo] = useState(initialData);
  const [errors, setErrors] = useState({});

  function handleChange(event) {
    const { name, value } = event.target;
    console.log(name, value);
    setPersonalInfo((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (areEqual(initialData, personalInfo)) {
      setErrors({ message: "No changes detected." });
      return;
    }
    try {
      const response = await update(personalInfo);
      if (response.status === 200) {
        setPersonalInfo((prev) => ({ ...prev, ...response.data }));
      } else {
        setErrors(response.error);
      }
    } catch (error) {
      setErrors({ message: error.message });
    }
  }

  function handleCancel() {
    setPersonalInfo(initialData);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-12 w-full pt-8">
      <div className="border-b border-gray-900/10 pb-8 px-4 mx-2">
        <legend className="text-xl font-bold text-gray-900 pt-4">
          Personal Information
        </legend>
        {errors?.message && (
          <div className="py-2 text-center rounded-md mt-8 border border-red-400 text-red-500 font-semibold text-sm bg-red-100 opacity-90">
            {errors.message}
          </div>
        )}
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
                value={personalInfo.username}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
            {errors?.username && (
              <ul className="h-4 text-red-500 text-sm ml-4">
                {errors.username.map((error) => (
                  <li key={error}>{error}</li>
                ))}
              </ul>
            )}
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
                name="first_name"
                type="text"
                value={personalInfo.first_name}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
            {errors?.first_name && (
              <ul className="h-4 text-red-500 text-sm ml-4">
                {errors.first_name.map((error) => (
                  <li key={error}>{error}</li>
                ))}
              </ul>
            )}
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
                name="last_name"
                type="text"
                value={personalInfo.last_name}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
            {errors?.last_name && (
              <ul className="h-4 text-red-500 text-sm ml-4">
                {errors.last_name.map((error) => (
                  <li key={error}>{error}</li>
                ))}
              </ul>
            )}
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
                value={personalInfo.email}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
            {errors?.email && (
              <ul className="h-4 text-red-500 text-sm ml-4">
                {errors.email.map((error) => (
                  <li key={error}>{error}</li>
                ))}
              </ul>
            )}
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
                name="phone_number"
                type="tel"
                value={personalInfo.phone_number}
                onChange={handleChange}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
              />
            </div>
            {errors?.phone_number && (
              <ul className="h-4 text-red-500 text-sm ml-4">
                {errors.phone_number.map((error) => (
                  <li key={error}>{error}</li>
                ))}
              </ul>
            )}
          </div>
        </div>
        <div className="mt-8 flex items-center justify-end gap-x-6">
          <button
            type="button"
            className="rounded-md bg-gray-100 px-3 py-2 text-sm font-semibold text-black shadow-sm hover:bg-gray-500 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
            onClick={handleCancel}
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
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [changePassowrdError, setChangePasswordError] = useState(null);

  function handleOldPasswordChange(event) {
    const { value } = event.target;
    setOldPassword(value);
  }

  function handleNewPasswordChange(event) {
    const { value } = event.target;
    setNewPassword(value);
  }

  function handleConfirmPasswordChange(event) {
    const { value } = event.target;
    setConfirmPassword(value);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (newPassword !== confirmPassword) {
      setChangePasswordError("Passwords do not match.");
      return;
    }
    try {
      const response = await changePassword({ oldPassword, newPassword });
      if (response.status === 200) {
        alert("Password changed successfully.");
      } else {
        setChangePasswordError(response.error.details);
      }
    } catch (error) {
      setChangePasswordError(error.message);
    }
  }

  function handleCancel() {
    setOldPassword("");
    setNewPassword("");
    setConfirmPassword("");
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-12 w-full pt-8">
      {changePassowrdError && (
        <div className="py-2 text-center rounded-md mt-8 border border-red-400 text-red-500 font-semibold text-sm bg-red-100 opacity-90">
          {changePassowrdError}
        </div>
      )}
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
                value={oldPassword}
                onChange={handleOldPasswordChange}
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
                value={newPassword}
                onChange={handleNewPasswordChange}
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
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
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
            onClick={handleCancel}
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
  const [password, setPassword] = useState("");
  const [deleteError, setDeleteError] = useState(null);
  const navigate = useNavigate();

  function handleChange(event) {
    const { value } = event.target;
    setPassword(value);
  }

  async function handelSubmit(event) {
    event.preventDefault();
    try {
      const response = await deleteProfile({ password });
      if (response.status === 200) {
        alert("Account deleted successfully.");
        navigate("/login");
      } else {
        setDeleteError(response.error.details);
      }
    } catch (error) {
      setDeleteError(error.message);
    }
  }

  return (
    <form onSubmit={handelSubmit} className="py-8 px-4 mx-2">
      {deleteError && (
        <div className="py-2 text-center rounded-md mt-8 border border-red-400 text-red-500 font-semibold text-sm bg-red-100 opacity-90">
          {deleteError}
        </div>
      )}
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
              value={password}
              onChange={handleChange}
              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
            />
          </div>
        </div>
      </div>
      <div className="mt-8 flex items-center justify-end gap-x-6">
        <button
          type="button"
          onClick={() => setPassword("")}
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
    </form>
  );
}
