import React, { useState, useEffect } from "react";
import { ChangePasswordForm, DeleteAccount } from "../components/ProfileForms";
import PersonalInfoForm from "../components/profile/PersonalInfo";
import { get } from "../data/profile";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);

  // Fetch the profile data when the component mounts
  // for the first time and store it in profile state
  useEffect(() => {
    async function fetchData() {
      const response = await get();
      if (response.status === 200) {
        setProfile({
          first_name: response.data.first_name || "",
          last_name: response.data.last_name || "",
          username: response.data.username || "",
          email: response.data.email || "",
          phone_number: response.data.phone_number || "",
        });
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
      {profile ? (
        <>
          <PersonalInfoForm data={profile} />
          <ChangePasswordForm />
          <DeleteAccount />
        </>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
}
