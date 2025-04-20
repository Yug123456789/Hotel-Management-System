// This script automatically highlights the navigation link for the current page

document.addEventListener("DOMContentLoaded", function () {
  var currentPage = window.location.pathname; ///Get the current page's URL path (example: "/hotel/bookings/")

  // Get all navigation links
  var navLinks = document.querySelectorAll("nav ul li a");

  // Check each link one by one
  navLinks.forEach(function (link) {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active"); // Add the blue underline
    } else if (
      link.getAttribute("href") !== "#" &&
      currentPage.includes(link.getAttribute("href"))
    ) {
      link.classList.add("active");

      var parentDropdown = link.closest(".dropdown");
      if (parentDropdown) {
        var dropdownToggle = parentDropdown.querySelector("a");
        if (dropdownToggle) {
          dropdownToggle.classList.add("active"); //// Add blue underline to dropdown title
        }
      }
    }
  });
});
