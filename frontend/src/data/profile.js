export async function get() {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/profile/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });
    if (response.ok) {
      return { status: response.status, data: await response.json() };
    }
    return { status: response.status, error: await response.json() };
  } catch (error) {
    throw new Error(`An error occurred while fetching. ${error}`);
  }
}

export async function update(data) {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/profile/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      data: JSON.stringify(data),
    });
    if (response.ok) {
      return { status: response.status, data: await response.json() };
    }
    return { status: response.status, error: await response.json() };
  } catch (error) {
    throw new Error(`An error occurred while fetching. ${error}`);
  }
}
