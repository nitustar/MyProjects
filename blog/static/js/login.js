document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const errorBox = document.getElementById("error");

  errorBox.innerText = "";

  try {
    const response = await fetch("/api/token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Invalid credentials");
    }

    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);

    // decode JWT to get user_id
    const payload = JSON.parse(atob(data.access.split('.')[1]));
    localStorage.setItem("user_id", payload.user_id);


    window.location.href = "/blog";
  } catch (error) {
    errorBox.innerText = error.message;
  }
});
