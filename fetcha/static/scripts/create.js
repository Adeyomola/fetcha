// copy function
function copy() {
  const custom_link = document.getElementById("custom_link");
  navigator.clipboard.writeText(custom_link.value);
}

// buttons on create page
const buttons = [
  "whatsapp",
  "instagram",
  "x",
  "pinterest",
  "snapchat",
  "facebook",
  "website",
  "linkedin",
];

const submit_button = document.getElementById("submit_button");

buttons.forEach((button_name) => {
  let button = document.getElementById(button_name);

  button.onclick = () => {
    const element = document.getElementById(`${button_name}_p`);
    element.toggleAttribute("hidden");

    const icon = document.getElementById(`${button_name}_i`);
    icon.toggleAttribute("hidden");
  };
});

// Inputs that alter preview
const identifier = document.getElementById("identifier");
const tagline = document.getElementById("tagline");
const background_color = document.getElementById("background-color");
const foreground_color = document.getElementById("foreground-color");

const preview = document.getElementById("preview");
const preview_foregound = document.getElementById("preview-foreground");
const preview_title = document.getElementById("preview-title");
const preview_tagline = document.getElementById("preview-tagline");

identifier.addEventListener("input", () => {
  preview_title.innerText =
    identifier.value.charAt(0).toUpperCase() + identifier.value.slice(1);
});

tagline.addEventListener("input", () => {
  preview_tagline.innerText = tagline.value;
});
background_color.addEventListener("input", () => {
  preview.style.backgroundColor = background_color.value;
});

foreground_color.addEventListener("input", () => {
  preview_foregound.style.backgroundColor = foreground_color.value;
});

// convert uploaded image to base64
const logo = document.getElementById("logo");
const main_picture = document.getElementById("main_picture");
const image_base64 = document.getElementById("image_base64");

logo.addEventListener("input", () => {
  const file = logo.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);

  reader.onloadend = () => {
    main_picture.setAttribute("src", reader.result);
    image_base64.value = reader.result;
  };
});

// Close Modal
const close_modal = document.getElementById("close_modal");
const copy_modal = document.getElementById("copy_modal");

if (close_modal) {
  close_modal.onclick = () => {
    copy_modal.style.display = "none";
  };
}

// dropdown
const dropdown = document.querySelector(".fa-caret-right");

dropdown.onclick = () => {
  if (preview.style.visibility == "visible") {
    preview.style.visibility = "hidden";
    dropdown.classList.remove("fa-caret-down");
    dropdown.classList.add("fa-caret-right");
  } else {
    preview.style.visibility = "visible";
    dropdown.classList.remove("fa-caret-right");
    dropdown.classList.add("fa-caret-down");
  }
};
