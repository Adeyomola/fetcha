// Dropdown
const anchor = document.querySelectorAll(".anchor");
anchor.forEach((element) => {
  element.children[1].addEventListener("click", () => {
    if (element.children[4].getAttribute("hidden") == null) {
      element.children[1].classList.add("fa-caret-right");
      element.children[1].classList.remove("fa-caret-down");
      element.children[4].toggleAttribute("hidden");
    } else {
      element.children[1].classList.remove("fa-caret-right");
      element.children[1].classList.add("fa-caret-down");
      element.children[4].toggleAttribute("hidden");
    }
  });
});

// copy function
const copy_icon = document.querySelectorAll(".copy_icon");

copy_icon.forEach((icon) => {
  icon.addEventListener("mousedown" || "touchstart", () => {
    icon.style.scale = 1.05;
    navigator.clipboard.writeText(icon.previousElementSibling.href);
  });
  icon.addEventListener("mouseup" || "touchend", () => {
    icon.style.scale = 1;
  });
});
