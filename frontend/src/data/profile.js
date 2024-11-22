import refresh_token from "../utils/refreshToken";

const url = "http://127.0.0.1:8000/api/profile/";
const headers = {
  "Content-Type": "application/json",
};

const request = (method, data) => {
  return fetch(url, {
    method: method,
    headers: headers,
    credentials: "include",
    body: data ? JSON.stringify(data) : undefined,
  });
};

export async function get() {
  try {
    let response = await request("GET");
    if (response.ok) {
      return { status: response.status, data: await response.json() };
    } else if (response.status === 401) {
      const refresh_response = await refresh_token();
      if (refresh_response.ok) {
        response = await request("GET");
        return { status: response.status, data: await response.json() };
      }
    }
    return { status: response.status, error: await response.json() };
  } catch (error) {
    throw new Error(`An error occurred while fetching. ${error}`);
  }
}

export async function update(updatedData) {
  try {
    let response = await request("PUT", updatedData);
    if (response.ok) {
      return { status: response.status, data: await response.json() };
    } else if (response.status === 401) {
      const refresh_response = await refresh_token();
      if (refresh_response.ok) {
        response = await request("PUT", updatedData);
        return { status: response.status, data: await response.json() };
      }
    }
    return { status: response.status, error: await response.json() };
  } catch (error) {
    throw new Error(`An error occurred while fetching. ${error}`);
  }
}

export async function deleteProfile(password) {
  try {
    let response = await request("DELETE", password);
    if (response.ok) {
      return { status: response.status, data: await response.json() };
    } else if (response.status === 401) {
      const refresh_response = await refresh_token();
      if (refresh_response.ok) {
        response = await request("DELETE", password);
        return { status: response.status, data: await response.json() };
      }
    }
    return { status: response.status, error: await response.json() };
  } catch (error) {
    throw new Error(`An error occurred while fetching. ${error}`);
  }
}

export async function changePassword({ oldPassword, newPassword }) {
  try {
    const data = { old_password: oldPassword, new_password: newPassword };
    let response = await fetch(
      "http://127.0.0.1:8000/api/profile/change-password/",
      {
        method: "PUT",
        headers: headers,
        credentials: "include",
        body: JSON.stringify(data),
      }
    );
    if (response.ok) {
      return { status: response.status, data: await response.json() };
    } else if (response.status === 401) {
      const refresh_response = await refresh_token();
      if (refresh_response.ok) {
        response = await request("PATCH", data);
        return { status: response.status, data: await response.json() };
      }
    }
    return { status: response.status, error: await response.json() };
  } catch (error) {
    throw new Error(`An error occurred while fetching. ${error}`);
  }
}
