(function () {
  var KEY = "artvue-favourites";

  function read() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(raw) ? raw : [];
    } catch (e) {
      return [];
    }
  }

  function write(ids) {
    localStorage.setItem(KEY, JSON.stringify(ids));
  }

  function paint() {
    var ids = read();
    var count = document.getElementById("saved-count");
    if (count) count.textContent = String(ids.length);
    document.querySelectorAll("[data-fav]").forEach(function (btn) {
      var on = ids.indexOf(btn.getAttribute("data-fav")) !== -1;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      if (!btn.querySelector("svg")) btn.textContent = on ? "Saved on this device" : "Save this work";
    });
  }

  document.addEventListener("click", function (event) {
    var fav = event.target.closest("[data-fav]");
    if (!fav) return;
    event.preventDefault();
    var id = fav.getAttribute("data-fav");
    var ids = read();
    var i = ids.indexOf(id);
    if (i === -1) ids.push(id);
    else ids.splice(i, 1);
    write(ids);
    paint();
    document.dispatchEvent(new CustomEvent("artvue:fav"));
  });

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  var backdrop = document.querySelector(".backdrop");

  function closeNav() {
    if (!nav) return;
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    if (backdrop) backdrop.classList.remove("is-open");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("nav-open", open);
      if (backdrop) backdrop.classList.toggle("is-open", open);
      if (open) {
        var first = nav.querySelector("a");
        if (first) first.focus();
      }
    });
  }

  if (backdrop) {
    backdrop.addEventListener("click", function () {
      closeNav();
      var filters = document.getElementById("filters");
      if (filters) filters.classList.remove("is-open");
      document.body.classList.remove("drawer-open");
      var opener = document.querySelector(".filter-open");
      if (opener) opener.setAttribute("aria-expanded", "false");
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeNav();
      var filters = document.getElementById("filters");
      if (filters && filters.classList.contains("is-open")) {
        filters.classList.remove("is-open");
        document.body.classList.remove("drawer-open");
        var opener = document.querySelector(".filter-open");
        if (opener) {
          opener.setAttribute("aria-expanded", "false");
          opener.focus();
        }
      }
      var box = document.getElementById("lightbox");
      if (box && box.open) box.close();
    }
  });

  paint();
  window.ARTVUE_FAV = { read: read, paint: paint };
})();
