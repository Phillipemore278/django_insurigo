document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".local-time").forEach((td) => {
    const utcString = td.getAttribute("data-utc");
    if (utcString) {
      const date = new Date(utcString);
      // Format the local date/time string as you prefer
      // Example: "Jun 2, 2025, 3:23 PM"
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      };
      td.textContent = date.toLocaleString(undefined, options);
    }
  });
});
