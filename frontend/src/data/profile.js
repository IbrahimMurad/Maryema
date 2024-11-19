export async function get() {
  try {
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken"));
    const headers = {
      "Content-Type": "application/json",
    };
    if (csrfToken) {
      headers["X-CSRFToken"] = csrfToken.split("=")[1];
    }
    const response = await fetch("http://127.0.0.1:8000/api/profile", {
      method: "GET",
      headers: headers,
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
