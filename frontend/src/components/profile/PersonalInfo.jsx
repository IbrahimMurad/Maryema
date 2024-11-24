import React, { useState, useRef } from "react";

import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";
import Snackbar from "@mui/material/Snackbar";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";

import SaveIcon from "@mui/icons-material/Save";

import { update } from "../../data/profile";
import areEqual from "../../utils/areEqual";
import toLabel from "../../utils/toLabel";
import FormInputField from "../common/FormInputField";

export default function PersonalInfoForm({ data }) {
  // The initialDataRef is used to store the initial data from the props.
  // This is used to compare the initial data with the updated data,
  // and to store it when the user cancels the changes.
  const initialDataRef = useRef({ ...data });

  // the data of the form
  const [personalInfo, setPersonalInfo] = useState({
    ...initialDataRef.current,
  });
  const [open, setOpen] = useState(false); // Snackbar visibility

  // Form errors (for each field)
  const [errors, setErrors] = useState({});

  // Notification message for the Snackbar (message error, details error, successful)
  const [notification, setNotification] = useState({
    status: null,
    message: null,
  });

  // Snackbar close event
  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpen(false);
  };

  // Handle form field changes
  function handleChange(event) {
    const { name, value } = event.target;
    setErrors((prev) => ({ ...prev, [name]: null }));
    setPersonalInfo((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (areEqual(initialDataRef.current, personalInfo)) {
      setNotification({ status: "error", message: "No changes detected." });
      setOpen(true);
      return;
    }
    try {
      const response = await update(personalInfo);
      if (response.status === 200) {
        setNotification({ status: "success", message: "Profile updated." });
        setOpen(true);
        initialDataRef.current = { ...response.data };
        setPersonalInfo((prev) => ({ ...prev, ...response.data }));
      } else {
        setErrors(response.error);
        if (response.error.details) {
          setOpen(true);
        }
      }
    } catch (error) {
      setNotification({ status: "error", message: error.message });
      setOpen(true);
    }
  }

  function handleCancel() {
    setPersonalInfo({ ...initialDataRef.current });
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="border-b border-gray-900/10 pb-8 px-4 mx-2">
        <legend className="text-xl font-bold text-gray-900">
          Personal Information
        </legend>
        <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          {Object.keys(personalInfo).map((key) => {
            if (key === "id") return null;
            return (
              <FormInputField
                key={key}
                name={key}
                value={personalInfo[key]}
                label={toLabel(key)}
                error={!!errors?.[key]}
                helperText={errors?.[key] || ""}
                onChange={handleChange}
              />
            );
          })}
        </div>
        <div className="mt-8 flex items-center justify-end gap-x-6">
          <Stack spacing={2} direction="row">
            <Button variant="outlined" onClick={handleCancel}>
              Cancel
            </Button>
            <Button
              variant="contained"
              type="submit"
              color="primary"
              startIcon={<SaveIcon />}
            >
              Save
            </Button>
          </Stack>
        </div>
      </div>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={open}
        autoHideDuration={3000}
        onClose={handleClose}
      >
        <Alert severity={notification.status}>{notification.message}</Alert>
      </Snackbar>
    </form>
  );
}
