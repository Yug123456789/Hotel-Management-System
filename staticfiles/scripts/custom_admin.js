document.addEventListener("DOMContentLoaded", function () {
  const actionSelect = document.querySelector('select[name="action"]');
  if (actionSelect && actionSelect.options.length > 1) {
    actionSelect.selectedIndex = 1; // Select the first actual action (skip the "---------" one)
  }
});
