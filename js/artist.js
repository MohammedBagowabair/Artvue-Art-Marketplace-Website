(function () {
  var root = document.getElementById("studio");
  if (!root || !window.ARTVUE) return;
  var data = window.ARTVUE;
  var id = new URLSearchParams(location.search).get("artist");
  var artist = data.artists.filter(function (item) { return item.id === id; })[0];

  function money(n) { return "$" + n.toLocaleString("en-US"); }
  function wa(text) { return "https://wa.me/967783964784?text=" + encodeURIComponent(text); }

  if (!artist) {
    document.title = "Artist not found — Artvue";
    root.innerHTML = '<div class="prose"><h1>This studio is not on the floor.</h1><p><a class="btn" href="index.html#artists">See the studios</a></p></div>';
    return;
  }

  var works = data.works.filter(function (item) { return item.artistId === artist.id; });
  document.title = artist.name + " — Artvue";
  var desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute("content", artist.name + ", " + artist.city + ". " + artist.bio);

  var lead = works[0];
  root.innerHTML =
    '<div class="artist-hero"><img src="images/art/' + lead.id + '-1100.webp" srcset="images/art/' + lead.id + '-640.webp 640w, images/art/' + lead.id + '-1100.webp 1100w" sizes="(max-width: 800px) 100vw, 42vw" width="' + lead.w + '" height="' + lead.h + '" alt="' + lead.alt + '"><div><p class="place">' + artist.city + ", " + artist.country + '</p><h1>' + artist.name + "</h1><p>" + artist.bio + '</p><p><a class="btn btn-wa" href="' + wa("Hello Artvue, I would like to request a commission with " + artist.name + ".") + '">Request a commission</a></p></div></div>' +
    '<div class="works">' + works.map(function (work) {
      return '<article class="card"><div class="card-visual"><a href="artwork.html?id=' + work.id + '"><img src="images/art/' + work.id + '-640.webp" srcset="images/art/' + work.id + '-640.webp 640w, images/art/' + work.id + '-1100.webp 1100w" sizes="(max-width: 640px) 100vw, 30vw" width="' + work.w + '" height="' + work.h + '" alt="' + work.alt + '" loading="lazy" decoding="async"></a>' +
        (work.sold ? '<p class="sold-mark">Sold</p>' : "") +
        '</div><div class="card-body"><h3><a href="artwork.html?id=' + work.id + '">' + work.title + '</a></h3><p class="meta">' + work.medium + " · " + work.size_label + '</p><p class="price">' + money(work.price) + "</p></div></article>";
    }).join("") + "</div>";
})();
