const btnYourClasses = document.querySelector(".your-classes-btn");
const yourClassesContent = document.querySelector(".your-classes-content");

const btnAddClasses = document.querySelector(".add-classes-btn");
const addClassesContent = document.querySelector(".add-classes-content");

btnYourClasses.addEventListener("click", function () {
  addClassesContent.classList.add("hidden");
  yourClassesContent.classList.remove("hidden");
});

btnAddClasses.addEventListener("click", function () {
  yourClassesContent.classList.add("hidden");
  addClassesContent.classList.remove("hidden");
});
