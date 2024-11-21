export async function login(data) {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
      credentials: "include",
      mode: "cors",
    });
    if (response.ok) {
      return { status: response.status, data: await response.json() };
    }
    return { status: response.status, error: await response.json() };
  } catch (error) {
    throw new Error("An error occurred while fetching.", error);
  }
}

export async function register(data) {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/auth/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
      credentials: "include",
    });
    return { status: response.status, data: await response.json() };
  } catch (error) {
    throw new Error("An error occurred while fetching.");
  }
}

export async function logout() {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/auth/logout/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });
    return { status: response.status, data: await response.json() };
  } catch (error) {
    throw new Error("An error occurred while fetching.");
  }
}
