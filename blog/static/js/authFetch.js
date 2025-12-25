async function refreshAccessToken() {
  const refresh = localStorage.getItem("refresh_token");

  if (!refresh) {
    logoutUser();
    return null;
  }

  const response = await fetch("/api/token/refresh/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ refresh })
  });

  if (!response.ok) {
    logoutUser();
    return null;
  }

  const data = await response.json();
  localStorage.setItem("access_token", data.access);
  return data.access;
}

function logoutUser() {
  localStorage.clear();
  window.location.href = "/login/";
}

/**
 * Use this for ALL protected API calls
 */
async function authFetch(url, options = {}) {
  let accessToken = localStorage.getItem("access_token");

  const response = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      "Authorization": `Bearer ${accessToken}`,
      "Content-Type": "application/json"
    }
  });

  // If token expired
  if (response.status === 401) {
    const newAccessToken = await refreshAccessToken();
    if (!newAccessToken) return;

    // retry original request
    return fetch(url, {
      ...options,
      headers: {
        ...(options.headers || {}),
        "Authorization": `Bearer ${newAccessToken}`,
        "Content-Type": "application/json"
      }
    });
  }

  return response;
}
