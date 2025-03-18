const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const emailfeedBackArea = document.querySelector(".emailinvalid_feedback");
const usernameSuccesOuptup = document.querySelector(".usernameSuccessOuptup");
const emailSuccessOuptup = document.querySelector(".emailSuccessOuptup");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

usernameField.addEventListener("keyup", (e) => {
  const userNameValue = e.target.value;
  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display = "none";
  usernameSuccesOuptup.style.display = "none";
  usernameSuccesOuptup.textContent = `Checking: "${userNameValue}"`;
  if (userNameValue.length > 3) {
    fetch("/authentication/validate_username", {
      body: JSON.stringify({ username: userNameValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        usernameSuccesOuptup.style.display = "block";

        if (data.username_error) {
          submitBtn.disabled = true;
          usernameField.classList.add("is-invalid");
          usernameSuccesOuptup.style.display = "none";
          feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
          feedBackArea.style.display = "block";
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

emailField.addEventListener("keyup", (e) => {
  const EmailValue = e.target.value;
  emailfeedBackArea.style.display = "none";
  emailField.classList.remove("is-invalid");
  emailSuccessOuptup.style.display = "none";
  emailSuccessOuptup.textContent = `Checking: ${EmailValue}`;
  if (EmailValue.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: EmailValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        emailSuccessOuptup.style.display = "block";
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          submitBtn.disabled = true;
          emailSuccessOuptup.style.display = "none";
          emailfeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
          emailfeedBackArea.style.display = "block";
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === "SHOW") {
    showPasswordToggle.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    showPasswordToggle.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

{
}
