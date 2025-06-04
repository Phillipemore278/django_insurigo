// Automatically apply spinner and disable effect to all links with [data-link-action]
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll("[data-link-action]");

  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const spinner = link.querySelector(".spinner");
      const linkText = link.querySelector(".link-text");
      const linkColor = link.getAttribute("data-disabled-color") || "#ccc";

      if (!spinner || !linkText) {
        console.warn("Spinner or text element not found inside link:", link);
        return;
      }

      // Hide the text, show the spinner
      linkText.style.display = "none";
      spinner.style.display = "inline-block";

      // Disable the link
      link.style.pointerEvents = "none";
      link.style.backgroundColor = linkColor;
      link.style.opacity = "0.6";

      setTimeout(() => {
        window.location.href = link.href;
      }, 100);
    });
  });
});
