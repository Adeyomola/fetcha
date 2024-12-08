const monthContainer = document.querySelector(".month");
const dateContainer = document.getElementById("dateContainer");
const timepopup = document.getElementById("timepopup");
const calendar = document.getElementById("calendar");

let date = new Date();
let month = date.getMonth();
let year = date.getFullYear();

function displayCalendar() {
  let dayOne = new Date(year, month, 1);
  let lastDay = new Date(year, month + 1, 0);

  monthContainer.innerText = date.toLocaleString("en-US", {
    month: "long",
    year: "numeric",
  });

  // ensures date starts on correct days
  for (i = 1; i < dayOne.getDay() + 7; i++) {
    let formattingDiv = document.createElement("div");
    formattingDiv.innerText = " ";
    dateContainer.appendChild(formattingDiv);
  }

  // inserts dates into calendar
  for (i = 1; i <= lastDay.getDate(); i++) {
    let dateDiv = document.createElement("div");
    dateDiv.className = "dates";
    dateDiv.innerText = i;
    dateContainer.appendChild(dateDiv);
  }
}

displayCalendar();

const previousMonth = document.querySelector(".fa-caret-left");
const nextMonth = document.querySelector(".fa-caret-right");

previousMonth.addEventListener("click", () => {
  month = month - 1;

  if (month < 0) {
    month = 11;
    year = year - 1;
    date.setFullYear(year);
  }

  monthContainer.innerText = " ";
  dateContainer.replaceChildren();

  date.setMonth(month);
  displayCalendar();
});

nextMonth.addEventListener("click", () => {
  month = month + 1;

  if (month > 11) {
    month = 0;
    year = year + 1;
    date.setFullYear(year);
  }
  monthContainer.innerText = " ";
  dateContainer.replaceChildren();

  date.setMonth(month);
  displayCalendar();
});

let chosen = document.getElementById("chosen");
chosen = chosen.getAttribute("content");

function choosingDates() {
  const dates = document.querySelectorAll(".dates");

  //
  dates.forEach((selectedDate) => {
    let availabledates = new Date(year, month, selectedDate.innerText);
    let weekday = availabledates.toLocaleString("en-US", {
      weekday: "long",
    });

    if (chosen.includes(weekday)) {
      selectedDate.addEventListener("click", () => {
        scheduleDate = new Date(year, month, selectedDate.innerText);
        timepopup.style.position = "absolute";
        timepopup.toggleAttribute("hidden");
      });
    } else {
      selectedDate.style.color = "grey";
    }
  });
}

choosingDates();
