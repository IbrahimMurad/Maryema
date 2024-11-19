import React, { useState, useEffect } from "react";
import {
  PersonalInfoForm,
  ChangePasswordForm,
  DeleteAccount,
} from "../components/ProfileForms";
import { get } from "../data/profile";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const response = await get();
      if (response.status === 200) {
        setProfile(response.data);
      } else {
        setError(response.error);
      }
    }

    try {
      fetchData();
    } catch (error) {
      setError(error.message);
    }
  }, []);

  return (
    <div className="space-y-12 mx-auto my-4 p-6 w-full lg:w-[50%] md:w-[70%] sm:w-[80%]">
      {error && <div className="text-red-500">{String(error.details)}</div>}
      <div className="border-b border-gray-900/10 pb-4">
        <h2 className="text-4xl font-bold text-gray-900">Profile</h2>
      </div>
      <PersonalInfoForm data={profile} />
      <ChangePasswordForm />
      <DeleteAccount />
    </div>
  );
}
