const availableDays = document.querySelectorAll(".availableDays");
let chosen = document.getElementById("chosen");
chosen = chosen.getAttribute("content");

availableDays.forEach((days) => {
  if (chosen.includes(days.value)) {
    days.setAttribute("checked", "");
  }
});
