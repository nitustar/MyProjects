document.getElementById("registerForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const message = document.getElementById("message");
  message.innerText = "";

  const response = await fetch("/blog/api/register/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    })
  });

  const data = await response.json();

  if (response.ok) {
    message.style.color = "green";
    message.innerText = "Account created successfully. Redirecting to login...";
    setTimeout(() => {
      window.location.href = "/login/";
    }, 1500);
  } else {
    message.style.color = "red";
    message.innerText = Object.values(data).join(", ");
  }
});
