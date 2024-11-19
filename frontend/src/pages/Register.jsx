import React, { useState } from "react";
import { register } from "../data/auth";
import { useNavigate } from "react-router-dom";
import StyledInput from "../styledComponents/StyledInput";
import StyledLabel from "../styledComponents/StyledLabel";
import Auth, {
  ErrorMessages,
  AuthHeader,
  AuthFooter,
} from "../components/auth/Auth";
import SubmitButton from "../components/buttons/SubmitButton";
import ShowButton from "../components/buttons/ShowButton";

export default function Register() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState({});
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    const clearedData = {
      email: e.target.email.value,
      username: e.target.username.value,
      password: e.target.password.value,
    };
    if (e.target.confirmPassword.value !== clearedData.password) {
      setError({ ...error, confirmPassword: ["Passwords do not match"] });
      return;
    }
    try {
      const response = await register(clearedData);
      if (response.status === 201) {
        navigate("/login");
      } else {
        setError({ ...error, ...response.data });
      }
    } catch (error) {
      alert("An error occurred while fetching.");
      return;
    }
  }

  return (
    <Auth>
      {/* register header */}
      <AuthHeader>Create an account.</AuthHeader>

      {/* register form */}
      <form onSubmit={handleSubmit} className="my-4 w-full">
        {/* email input */}
        <StyledLabel htmlFor="email">Email</StyledLabel>
        <StyledInput type="email" id="email" name="email" />

        {/* email error message */}
        <div className="h-4">
          {error.email && <ErrorMessages messages={error.email} />}
        </div>

        {/* username input */}
        <StyledLabel htmlFor="username">Username</StyledLabel>
        <StyledInput type="text" id="username" name="username" />

        {/* username error message */}
        <div className="h-4">
          {error.username && <ErrorMessages messages={error.username} />}
        </div>

        {/* password input */}
        <div className="mt-4 relative">
          <StyledLabel htmlFor="password">Password</StyledLabel>
          <StyledInput
            type={showPassword ? "text" : "password"}
            id="password"
            name="password"
          />

          {/* show password icon */}
          <ShowButton show={showPassword} setShow={setShowPassword} />
        </div>

        {/* password error message */}
        <div className="h-4">
          {error.password && <ErrorMessages messages={error.password} />}
        </div>

        {/* confirm password input */}
        <div className="mt-4 relative">
          <StyledLabel htmlFor="confirm-password">Confirm password</StyledLabel>
          <StyledInput
            type={showConfirmPassword ? "text" : "password"}
            id="confirm-password"
            name="confirmPassword"
          />
          <ShowButton
            show={showConfirmPassword}
            setShow={setShowConfirmPassword}
          />
        </div>

        {/* confirm password error message */}
        <div className="h-4">
          {error.confirmPassword && (
            <ErrorMessages messages={error.confirmPassword} />
          )}
        </div>

        {/* submit button */}
        <div className="mt-4">
          <SubmitButton>Register</SubmitButton>
        </div>

        {/* form error messages */}
        <div className="h-4">
          {error.details && <ErrorMessages messages={error.details} />}
        </div>
      </form>

      {/* register footer */}
      <AuthFooter
        question="Already have an account ?"
        link="/login"
        linkText="Login"
      />
    </Auth>
  );
}
