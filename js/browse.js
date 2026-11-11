(function () {
  var form = document.getElementById("filters");
  var grid = document.getElementById("works");
  if (!form || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".card"));
  var countEl = document.getElementById("result-count");
  var empty = document.getElementById("empty");
  var opener = document.querySelector(".filter-open");
  var backdrop = document.querySelector(".backdrop");

  function selected(name) {
    return Array.prototype.map.call(
      form.querySelectorAll('input[name="' + name + '"]:checked'),
      function (el) { return el.value; }
    );
  }

  function priceOk(price, bucket) {
    if (!bucket) return true;
    if (bucket === "under-500") return price < 500;
    if (bucket === "500-1500") return price >= 500 && price <= 1500;
    if (bucket === "1500-4000") return price > 1500 && price <= 4000;
    if (bucket === "over-4000") return price > 4000;
    return true;
  }

  function stateFromForm() {
    var sort = document.getElementById("sort");
    var q = document.getElementById("q");
    var price = form.querySelector('input[name="price"]:checked');
    return {
      category: selected("category"),
      style: selected("style"),
      medium: selected("medium"),
      size: selected("size"),
      orientation: selected("orientation"),
      price: price ? price.value : "",
      sort: sort ? sort.value : "featured",
      q: q ? q.value.trim() : "",
      saved: new URLSearchParams(location.search).get("saved") === "1"
    };
  }

  function writeUrl(state) {
    var params = new URLSearchParams();
    function put(key, list) {
      if (list && list.length) params.set(key, list.join(","));
    }
    put("category", state.category);
    put("style", state.style);
    put("medium", state.medium);
    put("size", state.size);
    put("orientation", state.orientation);
    if (state.price) params.set("price", state.price);
    if (state.sort && state.sort !== "featured") params.set("sort", state.sort);
    if (state.q) params.set("q", state.q);
    if (state.saved) params.set("saved", "1");
    var next = params.toString();
    history.replaceState(null, "", next ? "?" + next : location.pathname);
  }

  function readUrl() {
    var params = new URLSearchParams(location.search);
    function mark(name) {
      var raw = params.get(name);
      var values = raw ? raw.split(",") : [];
      form.querySelectorAll('input[name="' + name + '"]').forEach(function (el) {
        el.checked = values.indexOf(el.value) !== -1;
      });
    }
    ["category", "style", "medium", "size", "orientation"].forEach(mark);
    var price = params.get("price") || "";
    form.querySelectorAll('input[name="price"]').forEach(function (el) {
      el.checked = el.value === price;
    });
    var sort = document.getElementById("sort");
    if (sort) sort.value = params.get("sort") || "featured";
    var q = document.getElementById("q");
    if (q) q.value = params.get("q") || "";
  }

  function match(card, state) {
    function has(list, value) {
      return !list.length || list.indexOf(value) !== -1;
    }
    if (!has(state.category, card.dataset.category)) return false;
    if (!has(state.style, card.dataset.style)) return false;
    if (!has(state.medium, card.dataset.medium)) return false;
    if (!has(state.size, card.dataset.size)) return false;
    if (!has(state.orientation, card.dataset.orientation)) return false;
    if (!priceOk(Number(card.dataset.price), state.price)) return false;
    if (state.q) {
      var hay = (card.dataset.title + " " + card.dataset.artistName).toLowerCase();
      if (hay.indexOf(state.q.toLowerCase()) === -1) return false;
    }
    if (state.saved) {
      var ids = window.ARTVUE_FAV ? window.ARTVUE_FAV.read() : [];
      if (ids.indexOf(card.dataset.id) === -1) return false;
    }
    return true;
  }

  function sortCards(mode) {
    var list = cards.slice();
    list.sort(function (a, b) {
      if (mode === "price-asc") return Number(a.dataset.price) - Number(b.dataset.price);
      if (mode === "price-desc") return Number(b.dataset.price) - Number(a.dataset.price);
      if (mode === "newest") return Number(b.dataset.year) - Number(a.dataset.year) || Number(a.dataset.order) - Number(b.dataset.order);
      return Number(a.dataset.order) - Number(b.dataset.order);
    });
    list.forEach(function (card) { grid.appendChild(card); });
  }

  function apply(push) {
    var state = stateFromForm();
    var n = 0;
    cards.forEach(function (card) {
      var show = match(card, state);
      card.hidden = !show;
      if (show) n += 1;
    });
    sortCards(state.sort);
    if (countEl) countEl.textContent = n + (n === 1 ? " work" : " works");
    if (empty) empty.hidden = n !== 0;
    if (opener) {
      var active = state.category.length + state.style.length + state.medium.length + state.size.length + state.orientation.length + (state.price ? 1 : 0);
      opener.textContent = active ? "Filters (" + active + ")" : "Filters";
    }
    var showBtn = document.getElementById("show-works");
    if (showBtn) showBtn.textContent = "Show " + n + (n === 1 ? " work" : " works");
    if (push) writeUrl(state);
  }

  function closeDrawer() {
    form.classList.remove("is-open");
    document.body.classList.remove("drawer-open");
    if (opener) opener.setAttribute("aria-expanded", "false");
    if (backdrop && !document.getElementById("site-nav").classList.contains("is-open")) {
      backdrop.classList.remove("is-open");
    }
  }

  readUrl();
  apply(false);

  form.addEventListener("change", function () { apply(true); });
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    apply(true);
    closeDrawer();
  });
  var sortEl = document.getElementById("sort");
  var qEl = document.getElementById("q");
  if (sortEl) sortEl.addEventListener("change", function () { apply(true); });
  if (qEl) qEl.addEventListener("input", function () { apply(true); });

  if (opener) {
    opener.addEventListener("click", function () {
      var open = form.classList.toggle("is-open");
      opener.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("drawer-open", open);
      if (backdrop) backdrop.classList.toggle("is-open", open);
      if (open) {
        var field = form.querySelector("input, select");
        if (field) field.focus();
      }
    });
  }

  var closer = document.querySelector(".drawer-close");
  if (closer) closer.addEventListener("click", closeDrawer);

  document.getElementById("clear-filters").addEventListener("click", function () {
    form.reset();
    form.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(function (el) {
      el.checked = false;
    });
    var sort = document.getElementById("sort");
    if (sort) sort.value = "featured";
    var q = document.getElementById("q");
    if (q) q.value = "";
    if (new URLSearchParams(location.search).get("saved") === "1") {
      history.replaceState(null, "", location.pathname);
    }
    apply(true);
  });

  document.addEventListener("artvue:fav", function () {
    if (new URLSearchParams(location.search).get("saved") === "1") apply(false);
  });
})();
