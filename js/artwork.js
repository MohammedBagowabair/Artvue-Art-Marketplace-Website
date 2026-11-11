(function () {
  var root = document.getElementById("lot");
  if (!root || !window.ARTVUE) return;
  var data = window.ARTVUE;
  var id = new URLSearchParams(location.search).get("id");
  var work = data.works.filter(function (item) { return item.id === id; })[0];

  function money(n) {
    return "$" + n.toLocaleString("en-US");
  }

  function wa(text) {
    return "https://wa.me/967783964784?text=" + encodeURIComponent(text);
  }

  if (!work) {
    document.title = "Work not found — Artvue";
    root.innerHTML = '<div class="prose"><h1>This work is not in the catalogue.</h1><p>The link may be incomplete. The floor is still open.</p><p><a class="btn" href="browse.html">Browse the catalogue</a></p></div>';
    return;
  }

  var artist = data.artists.filter(function (item) { return item.id === work.artistId; })[0];
  document.title = work.title + " by " + artist.name + " — Artvue";
  var desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute("content", work.title + " by " + artist.name + ", " + work.medium + ", " + work.size_label + ". " + money(work.price) + ". Inquire on WhatsApp. Demo marketplace with illustrative prices.");

  var pageUrl = "https://mohammedbagowabair.github.io/Artvue-Art-Marketplace-Website/artwork.html?id=" + encodeURIComponent(work.id);
  var inquire = "Hello Artvue, I would like to inquire about \"" + work.title + "\" by " + artist.name + " (" + work.size_label + ", " + money(work.price) + "). " + pageUrl;
  var similar = "Hello Artvue, \"" + work.title + "\" by " + artist.name + " is marked sold. Is a similar piece available? " + pageUrl;
  var srcset = "images/art/" + work.id + "-640.webp 640w, images/art/" + work.id + "-1100.webp 1100w";
  var more = data.works.filter(function (item) {
    return item.artistId === work.artistId && item.id !== work.id;
  }).slice(0, 3);

  var facts = [
    ["Artist", '<a href="artist.html?artist=' + artist.id + '">' + artist.name + "</a>"],
    ["Category", work.category],
    ["Style", work.style],
    ["Medium", work.medium],
    ["Size", work.size_label],
    ["Orientation", work.orientation],
    ["Year", String(work.year)],
    ["Status", work.sold ? "Sold" : "Available to inquire"]
  ];

  root.innerHTML =
    '<figure class="lot-figure"><button type="button" class="zoom" id="open-lightbox" aria-haspopup="dialog"><img src="images/art/' + work.id + '-1100.webp" srcset="' + srcset + '" sizes="(max-width: 800px) 100vw, 62vw" width="' + work.w + '" height="' + work.h + '" alt="' + work.alt + '"></button></figure>' +
    '<div><p class="place">' + work.category + "</p><h1>" + work.title + "</h1>" +
    '<p class="artist-line"><a href="artist.html?artist=' + artist.id + '">' + artist.name + "</a> · " + artist.city + "</p>" +
    (work.sold ? '<p class="sold-inline" style="color:#6e2d2a;font-family:EB Garamond,Georgia,serif;font-style:italic;font-size:1.4rem;margin:10px 0 0">Sold</p>' : "") +
    '<p class="price-lg">' + money(work.price) + "</p>" +
    "<p>" + work.blurb + "</p>" +
    "<table class=\"lot-facts\"><tbody>" + facts.map(function (row) {
      return "<tr><th scope=\"row\">" + row[0] + "</th><td>" + row[1] + "</td></tr>";
    }).join("") + "</tbody></table>" +
    '<div class="lot-actions"><a class="btn btn-wa" href="' + wa(work.sold ? similar : inquire) + '">' + (work.sold ? "Ask about a similar piece" : "Buy / Inquire on WhatsApp") + "</a>" +
    '<button type="button" class="btn btn-ghost" data-fav="' + work.id + '" aria-pressed="false">Save this work</button>' +
    '<a class="btn btn-ghost" href="' + wa("Hello Artvue, I would like to request a commission" + (artist ? " with " + artist.name : "") + ".") + '">Request a commission</a></div>' +
    '<p class="note">Demo marketplace: fictional artists and illustrative prices. Nothing is purchased on this site.</p></div>';

  if (window.ARTVUE_FAV) window.ARTVUE_FAV.paint();

  var dialog = document.getElementById("lightbox");
  var lightImg = document.getElementById("lightbox-img");
  document.getElementById("open-lightbox").addEventListener("click", function () {
    lightImg.src = "images/art/" + work.id + "-1100.webp";
    lightImg.alt = work.alt;
    lightImg.classList.remove("is-zoomed");
    dialog.showModal();
  });
  lightImg.addEventListener("click", function () {
    lightImg.classList.toggle("is-zoomed");
  });
  document.getElementById("close-lightbox").addEventListener("click", function () {
    dialog.close();
  });

  var moreRoot = document.getElementById("more");
  if (!more.length) {
    moreRoot.hidden = true;
    return;
  }
  moreRoot.innerHTML = '<div class="section-head"><h2>More from ' + artist.name + '</h2><a href="artist.html?artist=' + artist.id + '">The studio</a></div><div class="more-grid">' +
    more.map(function (item) {
      return '<article class="card"><div class="card-visual"><a href="artwork.html?id=' + item.id + '"><img src="images/art/' + item.id + '-640.webp" srcset="images/art/' + item.id + '-640.webp 640w, images/art/' + item.id + '-1100.webp 1100w" sizes="(max-width: 700px) 100vw, 30vw" width="' + item.w + '" height="' + item.h + '" alt="' + item.alt + '" loading="lazy" decoding="async"></a></div><div class="card-body"><h3><a href="artwork.html?id=' + item.id + '">' + item.title + '</a></h3><p class="price">' + money(item.price) + "</p></div></article>";
    }).join("") + "</div>";
})();
