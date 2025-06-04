// Automatically handle all forms with [data-form-action] attribute
document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form[data-form-action]");

  forms.forEach((form) => {
    const button = form.querySelector("button[type='submit']");
    if (!button) {
      console.warn("No submit button found inside form:", form);
      return;
    }

    const spinner = button.querySelector(".spinner");
    const buttonText = button.querySelector(".button-text");
    const disabledColor = button.getAttribute("data-disabled-color") || "#ccc";

    if (!spinner || !buttonText) {
      console.warn(
        "Spinner or button-text element not found inside button:",
        button
      );
      return;
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();

      // Hide button text, show spinner
      buttonText.style.display = "none";
      spinner.style.display = "inline-block";

      // Disable the button and change color
      button.disabled = true;
      button.style.backgroundColor = disabledColor;
      button.style.cursor = "not-allowed";

      // Actually submit the form after a tiny delay so UI updates
      setTimeout(() => {
        form.submit();
      }, 100);
    });
  });
});

// How to use the new script:
// Just include your globalscript.js in your base template (typically at the end of <body> or inside {% block scripts %})

// Mark your forms with data-form-action attribute and structure your button like we discussed

// The script will automatically find all such forms and bind the submit handlers

// below uses id
// function handleFormSubmission(
//   formId,
//   buttonId,
//   spinnerId,
//   buttonTextId,
//   buttonColor = "#ccc"
// ) {
//   const form = document.getElementById(formId);
//   const button = document.getElementById(buttonId);
//   const spinner = document.getElementById(spinnerId);
//   const buttonText = document.getElementById(buttonTextId);

//   if (!form || !button || !spinner || !buttonText) {
//     console.error(
//       "One or more elements (form, button, spinner, buttonText) not found."
//     );
//     return;
//   }

//   form.addEventListener("submit", function (e) {
//     e.preventDefault();

//     buttonText.style.display = "none";
//     spinner.style.display = "inline-block";
//     button.disabled = true;
//     button.style.backgroundColor = buttonColor;

//     setTimeout(() => {
//       form.submit();
//     }, 100);
//   });
// }
