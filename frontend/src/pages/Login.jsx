import React, { useState } from "react";
import Auth, { AuthHeader, AuthFooter } from "../components/auth/Auth";
import StyledInput from "../styledComponents/StyledInput";
import StyledLabel from "../styledComponents/StyledLabel";
import SubmitButton from "../components/buttons/SubmitButton";
import ShowButton from "../components/buttons/ShowButton";
import { login } from "../data/auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState({});
  const navigate = useNavigate();

  async function handleLogin(e) {
    e.preventDefault();
    const data = {
      email: e.target.email.value,
      password: e.target.password.value,
    };
    try {
      const response = await login(data);
      if (response.status === 200) {
        alert("Login successful");
        navigate("/profile");
      } else {
        alert("Login failed");
        setError(response.error);
      }
    } catch (error) {
      alert("An error occurred while fetching.");
    }
  }

  return (
    <Auth>
      {/* login header */}
      <AuthHeader>Login to your account.</AuthHeader>

      {/* login error message */}
      {error.details && (
        <div className="h-4 flex justify-center items-center p-6 bg-red-50 border border-red-600 rounded-md w-full my-6">
          <p className="text-red-600 text-sm font-semibold m-4">
            {error.details}
          </p>
        </div>
      )}
      {/* login form */}
      <form onSubmit={handleLogin} className="mb-4 w-full">
        {/* email input */}
        <StyledLabel htmlFor="email">Email</StyledLabel>
        <StyledInput
          type="email"
          id="email"
          name="email"
          autoComplete="email"
        />

        {/* password input */}
        <div className="mt-4 relative">
          <StyledLabel htmlFor="password">Password</StyledLabel>
          <StyledInput
            type={showPassword ? "text" : "password"}
            id="password"
            name="password"
            autoComplete="current-password"
          />

          {/* show password icon */}
          <ShowButton show={showPassword} setShow={setShowPassword} />
        </div>

        {/* submit button */}
        <div className="mt-4">
          <SubmitButton>Login</SubmitButton>
        </div>
      </form>

      {/* login footer */}
      <AuthFooter
        question="Do not have an account ?"
        link="/register"
        linkText="register"
      />
    </Auth>
  );
}
