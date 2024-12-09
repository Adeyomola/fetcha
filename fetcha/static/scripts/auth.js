const password = document.getElementById("password");
const confirm_password = document.getElementById("confirm_password");

function validatePassword(e) {
  if (password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords do not match");
    confirm_password.reportValidity();
    e.preventDefault();
  } else {
    confirm_password.setCustomValidity("");
  }
}

function validatePasswordComponent() {
  const regex = /^[a-zA-Z0-9!@#\$%\^\&*\)\(+=._-]{6,}$/g;

  if (!password.value.match(regex)) {
    alert(
      "Use at least six characters, an uppercase letter, a number, and a special character"
    );
  }
}
password.onchange = validatePassword;
password.onkeyup = validatePasswordComponent;
confirm_password.onkeyup = validatePassword;

const email = document.getElementById("email");
const confirm_email = document.getElementById("confirm_email");

if (email && confirm_email) {
  function validateEmail(e) {
    if (email.value != confirm_email.value) {
      confirm_email.setCustomValidity("Emails do not match");
      confirm_email.reportValidity();
      e.preventDefault();
    } else {
      confirm_email.setCustomValidity("");
    }
  }
  email.onchange = validateEmail;
  confirm_email.onkeyup = validateEmail;
}
