import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import FormControl from "@mui/material/FormControl";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import InputLabel from "@mui/material/InputLabel";
import OutlinedInput from "@mui/material/OutlinedInput";
import TextField from "@mui/material/TextField";

import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

import { deleteProfile, changePassword } from "../data/profile";

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
    <form onSubmit={handleSubmit} className="w-full">
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
            <FormControl variant="outlined" fullWidth={true}>
              <InputLabel htmlFor="outlined-adornment-password" required>
                Old password
              </InputLabel>
              <OutlinedInput
                id="outlined-adornment-password"
                type={showOldPassword ? "text" : "password"}
                onChange={handleOldPasswordChange}
                fullWidth={true}
                required
                endAdornment={
                  <InputAdornment position="end">
                    <IconButton
                      aria-label={
                        showOldPassword
                          ? "hide the password"
                          : "display the password"
                      }
                      onClick={() => setShowOldPassword(!showOldPassword)}
                      edge="end"
                    >
                      {showOldPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                }
                label="Old password"
              />
            </FormControl>
          </div>
          <div className="sm:col-span-3 sm:col-start-1">
            <FormControl variant="outlined" fullWidth={true}>
              <InputLabel htmlFor="outlined-adornment-password" required>
                New password
              </InputLabel>
              <OutlinedInput
                id="outlined-adornment-password"
                type={showNewPassword ? "text" : "password"}
                onChange={handleNewPasswordChange}
                fullWidth={true}
                required
                endAdornment={
                  <InputAdornment position="end">
                    <IconButton
                      aria-label={
                        showNewPassword
                          ? "hide the password"
                          : "display the password"
                      }
                      onClick={() => setShowOldPassword(!newPassword)}
                      edge="end"
                    >
                      {showNewPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                }
                label="New password"
              />
            </FormControl>
          </div>

          <div className="sm:col-span-3 sm:col-start-1">
            <FormControl variant="outlined" fullWidth={true}>
              <InputLabel htmlFor="outlined-adornment-password" required>
                Confirm new password
              </InputLabel>
              <OutlinedInput
                id="outlined-adornment-password"
                type={showConfirmPassword ? "text" : "password"}
                onChange={handleConfirmPasswordChange}
                fullWidth={true}
                required
                endAdornment={
                  <InputAdornment position="end">
                    <IconButton
                      aria-label={
                        showConfirmPassword
                          ? "hide the password"
                          : "display the password"
                      }
                      onClick={() => setShowOldPassword(!showConfirmPassword)}
                      edge="end"
                    >
                      {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                }
                label="Confirm new password"
              />
            </FormControl>
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
    <form onSubmit={handelSubmit} className="px-4 mx-2">
      <legend className="text-xl font-bold text-gray-900 mb-4">
        Delete Account
      </legend>
      <TextField
        className="w-full sm:w-[80%] md:w-[70%] lg:w-[60%] xl:[50%]"
        type="password"
        label="Password"
        variant="outlined"
        required
        value={password}
        onChange={handleChange}
        error={deleteError}
        helperText={deleteError}
        onFocus={() => setDeleteError(null)}
      />
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
