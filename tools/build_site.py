#!/usr/bin/env python3
"""Download catalogue photographs, write WebP sizes, and emit static pages."""

import json
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "images" / "art"
HIRES = Path("/tmp/artvue-hires")
BASE = "https://mohammedbagowabair.github.io/Artvue-Art-Marketplace-Website"
PHONE = "967783964784"
UA = {"User-Agent": "Mozilla/5.0 (compatible; ArtvueDemo/1.0)"}

ARTISTS = [
    {
        "id": "lina-voss",
        "name": "Lina Voss",
        "city": "Berlin",
        "country": "Germany",
        "bio": "Lina Voss paints with a loaded brush and leaves the weave of the canvas in the picture. The works are built from rooms, weather, and the edge where two colours meet.",
    },
    {
        "id": "priya-menon",
        "name": "Priya Menon",
        "city": "Kochi",
        "country": "India",
        "bio": "Priya Menon works in oil and acrylic from the coast at Kochi. Harbours, rain, and the colour of water after dark give the paintings their structure.",
    },
    {
        "id": "mateo-ruiz",
        "name": "Mateo Ruiz",
        "city": "Oaxaca",
        "country": "Mexico",
        "bio": "Mateo Ruiz paints tables, fruit, and profiles. The figures stay close to still life: recognisable, then reduced to colour and the weight of the paint.",
    },
    {
        "id": "jonah-adeyemi",
        "name": "Jonah Adeyemi",
        "city": "Lagos",
        "country": "Nigeria",
        "bio": "Jonah Adeyemi scrapes acrylic back and draws into it again. The paintings carry the noise of a street without describing a particular corner of it.",
    },
    {
        "id": "kenji-mori",
        "name": "Kenji Mori",
        "city": "Kyoto",
        "country": "Japan",
        "bio": "Kenji Mori works with ink and water on a nearly empty sheet. What remains is a stain, a tide line, or a field of pale colour.",
    },
    {
        "id": "amina-diallo",
        "name": "Amina Diallo",
        "city": "Dakar",
        "country": "Senegal",
        "bio": "Amina Diallo photographs places at the hour when detail drops out: a gate in still water, a storm over stone, a coast under green light. The prints are archival pigment.",
    },
    {
        "id": "ines-laurent",
        "name": "Inès Laurent",
        "city": "Lyon",
        "country": "France",
        "bio": "Inès Laurent builds flat colour into a wall-sized geometry. The print in this catalogue is meant to sit without a heavy frame.",
    },
    {
        "id": "soren-hale",
        "name": "Soren Hale",
        "city": "Reykjavík",
        "country": "Iceland",
        "bio": "Soren Hale makes stoneware vessels with a low profile and a speckled skin. They are sculpture you can walk around, not a table setting.",
    },
]

# long_cm is the longer side. Orientation is measured from the file.
WORKS = [
    dict(id="harbour-weather", title="Harbour Weather", artist="priya-menon", category="Painting", style="Landscape", medium="Oil on canvas", medium_group="Oil", year=2025, price=6400, sold=False, long_cm=140, kind="pexels", pid="1070534", blurb="Thick oil, laid in bands of teal and red, the way a harbour looks when the light breaks after rain."),
    dict(id="north-wall", title="Room with a North Wall", artist="lina-voss", category="Painting", style="Abstract", medium="Oil on linen", medium_group="Oil", year=2025, price=4800, sold=False, long_cm=130, kind="unsplash", pid="1618331835717-801e976710b2", blurb="Blocks of linen colour, scraped and repainted, as if a room had been taken apart and put back by the light."),
    dict(id="after-the-fair", title="After the Fair", artist="lina-voss", category="Painting", style="Abstract", medium="Oil on canvas", medium_group="Oil", year=2023, price=3600, sold=False, long_cm=110, kind="unsplash", pid="1541961017774-22349e4a1262", blurb="Impasto in yellow, green, and a hot red. The paint sits proud of the weave."),
    dict(id="peaches", title="Peaches and Two Bottles", artist="mateo-ruiz", category="Painting", style="Figurative", medium="Acrylic on canvas", medium_group="Acrylic", year=2024, price=3900, sold=True, long_cm=100, kind="pexels", pid="2086361", blurb="A table after a meal: fruit, two bottles, and a cloth that refuses to lie flat."),
    dict(id="night-harbour", title="Night Harbour", artist="lina-voss", category="Painting", style="Abstract", medium="Oil on canvas", medium_group="Oil", year=2026, price=5200, sold=False, long_cm=150, kind="unsplash", pid="1536924940846-227afb31e2a5", blurb="A dark ground with a single orange mast of paint. The rest is blue, almost black."),
    dict(id="monsoon-field", title="Monsoon Field", artist="priya-menon", category="Painting", style="Landscape", medium="Oil on linen", medium_group="Oil", year=2024, price=4100, sold=False, long_cm=120, kind="unsplash", pid="1515405295579-ba7b45403062", blurb="Horizontal strokes, white over blue, the surface of water rather than a view of it."),
    dict(id="salt-grammar", title="Salt Grammar", artist="jonah-adeyemi", category="Painting", style="Abstract", medium="Acrylic on canvas", medium_group="Acrylic", year=2025, price=3100, sold=False, long_cm=120, kind="pexels", pid="1266808", blurb="Red notes over a blue-grey field, with lines that read like scaffolding left in the picture."),
    dict(id="procession", title="Procession Yellow", artist="mateo-ruiz", category="Painting", style="Abstract", medium="Oil on canvas", medium_group="Oil", year=2026, price=4400, sold=False, long_cm=140, kind="unsplash", pid="1544967082-d9d25d867d66", blurb="A crowd reduced to scratches of white across orange, magenta, and violet."),
    dict(id="profile-august", title="Profile in August", artist="mateo-ruiz", category="Painting", style="Figurative", medium="Acrylic on canvas", medium_group="Acrylic", year=2025, price=2750, sold=False, long_cm=90, kind="unsplash", pid="1533158326339-7f3cf2404354", blurb="A head, almost. Blue at the brow, a pink cheek, and a dark mouth that never quite arrives."),
    dict(id="soft-partition", title="Soft Partition", artist="jonah-adeyemi", category="Painting", style="Abstract", medium="Acrylic and ink on canvas", medium_group="Acrylic", year=2024, price=1980, sold=False, long_cm=90, kind="unsplash", pid="1547826039-bfc35e0f1ea8", blurb="Broad colour, then a few ink lines drawn across it, as if correcting a map."),
    dict(id="lampblack", title="Lampblack and Lemon", artist="jonah-adeyemi", category="Painting", style="Abstract", medium="Acrylic on canvas", medium_group="Acrylic", year=2026, price=2400, sold=False, long_cm=100, kind="unsplash", pid="1561214115-f2f134cc4912", blurb="A pour of lemon, lampblack, and white. The cells of the paint stay visible."),
    dict(id="heat-on-water", title="Heat on the Water", artist="priya-menon", category="Painting", style="Abstract", medium="Acrylic on canvas", medium_group="Acrylic", year=2026, price=2200, sold=False, long_cm=90, kind="pexels", pid="5603660", blurb="Orange and red dragged through white. The lower half of the canvas is left almost bare."),
    dict(id="canal-red", title="Canal After Red", artist="priya-menon", category="Painting", style="Abstract", medium="Acrylic on canvas", medium_group="Acrylic", year=2023, price=2650, sold=True, long_cm=110, kind="unsplash", pid="1604871000636-074fa5117945", blurb="A current of blue and a thread of red. Sold. Ask if a related canvas is still in the studio."),
    dict(id="violet-current", title="Violet Current", artist="lina-voss", category="Painting", style="Abstract", medium="Acrylic on canvas", medium_group="Acrylic", year=2024, price=1850, sold=True, long_cm=80, kind="pexels", pid="3109807", blurb="A violet pour with a mineral shine. The canvas has left the studio."),
    dict(id="suspended-ink", title="Suspended Ink", artist="kenji-mori", category="Drawing", style="Abstract", medium="Ink, archival print", medium_group="Ink", year=2025, price=860, sold=False, long_cm=70, kind="unsplash", pid="1541701494587-cb58502866ab", blurb="Ink released into water and stopped. Printed once, on cotton rag, from the study."),
    dict(id="fourth-wash", title="Fourth Wash", artist="kenji-mori", category="Drawing", style="Minimal", medium="Watercolour on paper", medium_group="Watercolour", year=2024, price=460, sold=False, long_cm=42, kind="unsplash", pid="1528459801416-a9e53bbf4e17", blurb="A pale sheet with a few stains of blue and a scatter of red. Most of the paper is untouched."),
    dict(id="bloc-notes", title="Bloc Notes", artist="ines-laurent", category="Prints", style="Pop", medium="Pigment print", medium_group="Pigment print", year=2025, price=380, sold=True, long_cm=70, kind="unsplash", pid="1554188248-986adbb73be4", blurb="Constructed colour: planes of red, blue, and pink locked into a shallow relief. The edition noted here is sold."),
    dict(id="five-vessels", title="Five Vessels", artist="soren-hale", category="Sculpture", style="Minimal", medium="Stoneware", medium_group="Ceramic", year=2025, price=1280, sold=False, long_cm=36, kind="unsplash", pid="1610701596007-11502861dcfa", blurb="Five cups and a cylinder, speckled stoneware, meant to be seen against a plain wall."),
    dict(id="gate-early", title="A Gate, Early", artist="amina-diallo", category="Photography", style="Minimal", medium="Archival pigment print", medium_group="Photograph", year=2025, price=1800, sold=True, long_cm=80, kind="pexels", pid="301614", blurb="A single gate in still water, printed large. The print offered here has sold."),
    dict(id="inside-weather", title="Inside the Weather", artist="amina-diallo", category="Photography", style="Landscape", medium="Archival pigment print", medium_group="Photograph", year=2024, price=1200, sold=False, long_cm=90, kind="pexels", pid="167699", blurb="Fir trees losing their edges in fog. A quiet print, not a view from a roadside."),
    dict(id="before-the-crack", title="Before the Crack", artist="amina-diallo", category="Photography", style="Landscape", medium="Archival pigment print", medium_group="Photograph", year=2022, price=2600, sold=False, long_cm=110, kind="pexels", pid="3244513", blurb="Stone, a dirt track, and one strike of light. Printed on cotton rag."),
    dict(id="green-hour", title="Green Hour", artist="amina-diallo", category="Photography", style="Landscape", medium="Archival pigment print", medium_group="Photograph", year=2026, price=2400, sold=False, long_cm=100, kind="pexels", pid="1933239", blurb="A coast under a green sky. The exposure is long enough that the water goes still."),
    dict(id="repeated-bay", title="Repeated Bay", artist="jonah-adeyemi", category="Photography", style="Minimal", medium="Archival pigment print", medium_group="Photograph", year=2023, price=980, sold=False, long_cm=70, kind="pexels", pid="1738986", blurb="A corridor of repeated concrete bays. One figure, small, at the far light."),
    dict(id="cloud-floor", title="Cloud Floor", artist="amina-diallo", category="Photography", style="Landscape", medium="Archival pigment print", medium_group="Photograph", year=2021, price=1500, sold=False, long_cm=100, kind="pexels", pid="325185", blurb="A city cut off at the knees by cloud. The print is about the floor of weather, not the skyline."),
]


def source_url(work):
    if work["kind"] == "pexels":
        return f"https://images.pexels.com/photos/{work['pid']}/pexels-photo-{work['pid']}.jpeg?auto=compress&cs=tinysrgb&w=2000"
    return f"https://images.unsplash.com/photo-{work['pid']}?auto=format&fit=max&w=2000&q=82"


def credit_page(work):
    if work["kind"] == "pexels":
        return f"https://www.pexels.com/photo/{work['pid']}/"
    return f"https://unsplash.com/photos/{work['pid']}"


def download(work):
    HIRES.mkdir(parents=True, exist_ok=True)
    dest = HIRES / f"{work['id']}.jpg"
    if dest.exists() and dest.stat().st_size > 20000:
        return work["id"]
    req = urllib.request.Request(source_url(work), headers=UA)
    with urllib.request.urlopen(req, timeout=40) as res:
        data = res.read()
    if len(data) < 8000:
        raise RuntimeError(f"small file {work['id']}")
    dest.write_bytes(data)
    return work["id"]


def run(cmd):
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL)


def to_webp(work):
    src = HIRES / f"{work['id']}.jpg"
    IMG.mkdir(parents=True, exist_ok=True)
    widths = [640, 1100]
    if work["id"] == "harbour-weather":
        widths.append(1700)
    for width in widths:
        out = IMG / f"{work['id']}-{width}.webp"
        run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
            "-vf", f"scale='min({width},iw)':-2:flags=lanczos",
            "-c:v", "libwebp", "-quality", "76", "-compression_level", "6",
            str(out),
        ])
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x",
        str(IMG / f"{work['id']}-1100.webp"),
    ], text=True).strip()
    w, h = [int(n) for n in probe.split("x")]
    return w, h


def dims(w, h, long_cm):
    if w >= h:
        width_cm = long_cm
        height_cm = max(1, round(long_cm * h / w))
    else:
        height_cm = long_cm
        width_cm = max(1, round(long_cm * w / h))
    longest = max(width_cm, height_cm)
    shortest = min(width_cm, height_cm)
    if abs(w - h) / max(w, h) < 0.06:
        orientation = "Square"
    elif w > h:
        orientation = "Landscape"
    else:
        orientation = "Portrait"
    if longest < 50:
        size = "Small"
    elif longest <= 100:
        size = "Medium"
    else:
        size = "Large"
    label = f"{width_cm} × {height_cm} cm"
    return width_cm, height_cm, orientation, size, label, shortest


def money(n):
    return f"${n:,}"


def wa(text):
    from urllib.parse import quote
    return f"https://wa.me/{PHONE}?text={quote(text)}"


def page_url(path):
    if path == "index.html":
        return BASE + "/"
    return BASE + "/" + path


HEART = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 20s-7-4.4-7-9a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 4.6-7 9-7 9z"></path></svg>'
CHAT = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#f7f4ed" stroke-width="1.6"><path d="M5 16.5 3.5 20.5 8 18.5A8 8 0 1 0 5 16.5Z"></path></svg>'

CONTACT = wa("Hello Artvue, I have a question about the marketplace.")
COMMISSION = wa("Hello Artvue, I would like to request a commission.")
SELL = wa("Hello Artvue, I would like to apply to sell my art. I will send my name, city, and three works.")


def inquire(work, artist):
    url = page_url(f"artwork.html?id={work['id']}")
    if work["sold"]:
        text = f'Hello Artvue, "{work["title"]}" by {artist["name"]} is marked sold ({work["size_label"]}, {money(work["price"])}). Is a similar piece available? {url}'
    else:
        text = f'Hello Artvue, I would like to inquire about "{work["title"]}" by {artist["name"]} ({work["size_label"]}, {money(work["price"])}). {url}'
    return wa(text)


def nav(current):
    items = [
        ("browse.html?category=Painting", "Paintings"),
        ("browse.html?category=Drawing", "Drawings"),
        ("browse.html?category=Photography", "Photography"),
        ("browse.html?category=Prints", "Prints"),
        ("browse.html?category=Sculpture", "Sculpture"),
        ("index.html#artists", "Artists"),
        ("about.html", "About"),
        ("sell.html", "Sell"),
    ]
    links = []
    for href, label in items:
        links.append(f'<a href="{href}">{label}</a>')
    return f'''
<a class="skip" href="#content">Skip to content</a>
<p class="demo-note">Demo marketplace: fictional artists and illustrative prices.</p>
<header class="site-header">
  <a class="logo" href="index.html">Artvue<span></span></a>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav id="site-nav" aria-label="Primary">{''.join(links)}</nav>
  <div class="header-tools">
    <a class="tool-search" href="browse.html">Search</a>
    <a href="browse.html?saved=1">Saved <span class="saved-count" id="saved-count">0</span></a>
    <a href="{CONTACT}">Contact</a>
  </div>
</header>
<div class="backdrop"></div>'''


def footer():
    return f'''
<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <h2>Artvue</h2>
      <p>Demo marketplace: fictional artists and illustrative prices. A catalogue for looking, and for a conversation on WhatsApp. No cart and no payment.</p>
    </div>
    <div>
      <a href="browse.html">Catalogue</a>
      <a href="about.html">How it works</a>
      <a href="sell.html">Sell your art</a>
      <a href="credits.html">Image credits</a>
    </div>
    <div>
      <a href="browse.html?category=Painting">Paintings</a>
      <a href="browse.html?category=Drawing">Drawings</a>
      <a href="browse.html?category=Photography">Photography</a>
      <a href="browse.html?style=Abstract">Abstract</a>
    </div>
    <div>
      <a href="{CONTACT}">Contact on WhatsApp</a>
      <a href="{COMMISSION}">Request a commission</a>
      <a href="{SELL}">Artist application</a>
    </div>
  </div>
  <p class="fine">© 2026 Artvue. Fictional artists. Photographs are stock sources listed on the credits page, used here as illustrations.</p>
</footer>
<a class="wa-float" href="{CONTACT}" aria-label="Contact Artvue on WhatsApp">{CHAT}</a>'''


def head(title, description, path, preload=False):
    canon = page_url(path)
    og = f"{BASE}/images/art/harbour-weather-1100.webp"
    preload_tags = ""
    if preload:
        preload_tags = '''
  <link rel="preload" href="fonts/eb-garamond-500-italic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" as="image" href="images/art/harbour-weather-1700.webp" imagesrcset="images/art/harbour-weather-1100.webp 1100w, images/art/harbour-weather-1700.webp 1700w" imagesizes="100vw">'''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{canon}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{og}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#f3efe6">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/styles.css">{preload_tags}
</head>
<body>'''


def document(title, description, path, body, scripts, preload=False):
    script_tags = "\n".join(f'  <script src="{src}"></script>' for src in scripts)
    return head(title, description, path, preload) + nav(path) + body + footer() + "\n" + script_tags + "\n</body>\n</html>\n"


def card(work, artist, eager=False):
    loading = "eager" if eager else "lazy"
    fetch = ' fetchpriority="high"' if eager else ""
    sold = '<p class="sold-mark">Sold</p>' if work["sold"] else ""
    return f'''<article class="card" data-id="{work['id']}" data-title="{escape(work['title'])}" data-artist-name="{escape(artist['name'])}" data-category="{work['category']}" data-style="{work['style']}" data-medium="{escape(work['medium_group'])}" data-size="{work['size']}" data-orientation="{work['orientation']}" data-price="{work['price']}" data-year="{work['year']}" data-order="{work['order']}">
  <div class="card-visual">
    <a href="artwork.html?id={work['id']}"><img src="images/art/{work['id']}-640.webp" srcset="images/art/{work['id']}-640.webp 640w, images/art/{work['id']}-1100.webp 1100w" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 46vw, 30vw" width="{work['w']}" height="{work['h']}" alt="{escape(work['alt'])}" loading="{loading}" decoding="async"{fetch}></a>
    {sold}
    <button class="fav" type="button" data-fav="{work['id']}" aria-pressed="false" aria-label="Save {escape(work['title'])}">{HEART}</button>
  </div>
  <div class="card-body">
    <h3><a href="artwork.html?id={work['id']}">{escape(work['title'])}</a></h3>
    <p class="by"><a href="artist.html?artist={artist['id']}">{escape(artist['name'])}</a></p>
    <p class="meta">{escape(work['medium'])} · {escape(work['size_label'])}</p>
    <p class="price">{money(work['price'])}</p>
  </div>
</article>'''


def checkbox(name, value, label=None):
    label = label or value
    return f'<label><input type="checkbox" name="{name}" value="{escape(value)}"> {escape(label)}</label>'


def build_pages(works, artists):
    by_id = {a["id"]: a for a in artists}
    by_work = {w["id"]: w for w in works}

    def count(key, value):
        return sum(1 for w in works if w[key] == value)

    hero = by_work["harbour-weather"]
    hero_artist = by_id[hero["artist"]]
    cats = [
        ("Painting", "Paintings", "harbour-weather"),
        ("Drawing", "Drawings", "fourth-wash"),
        ("Photography", "Photography", "gate-early"),
        ("Prints", "Prints", "bloc-notes"),
        ("Sculpture", "Sculpture", "five-vessels"),
    ]
    cat_html = []
    for key, label, wid in cats:
        w = by_work[wid]
        cat_html.append(f'''<a class="cat-tile" href="browse.html?category={key}"><img src="images/art/{w['id']}-640.webp" srcset="images/art/{w['id']}-640.webp 640w, images/art/{w['id']}-1100.webp 1100w" sizes="(max-width: 640px) 46vw, 18vw" width="{w['w']}" height="{w['h']}" alt="{escape(w['alt'])}" loading="lazy" decoding="async"><span>{label}</span><small>{count('category', key)} works</small></a>''')

    north_ids = ["north-wall", "night-harbour", "after-the-fair"]
    lead = card(by_work["monsoon-field"], by_id["priya-menon"], eager=False)
    # monsoon as lead image in the feature - actually use north-wall as lead
    lead = card(by_work["north-wall"], by_id["lina-voss"])
    side = "".join(card(by_work[i], by_id[by_work[i]["artist"]]) for i in ["night-harbour", "after-the-fair"])

    styles = ["Abstract", "Figurative", "Landscape", "Pop", "Minimal"]
    style_html = "".join(
        f'<a class="style-row" href="browse.html?style={s}"><span>{s}</span><small>{count("style", s)} works</small></a>'
        for s in styles
    )

    bands = [
        ("Under $500", "under-500", "fourth-wash"),
        ("$500 to $1,500", "500-1500", "five-vessels"),
        ("Above $4,000", "over-4000", "harbour-weather"),
    ]
    band_html = []
    for label, key, wid in bands:
        w = by_work[wid]
        if key == "under-500":
            n = sum(1 for item in works if item["price"] < 500)
        elif key == "500-1500":
            n = sum(1 for item in works if 500 <= item["price"] <= 1500)
        else:
            n = sum(1 for item in works if item["price"] > 4000)
        band_html.append(f'''<a class="band" href="browse.html?price={key}"><img src="images/art/{w['id']}-640.webp" srcset="images/art/{w['id']}-640.webp 640w, images/art/{w['id']}-1100.webp 1100w" sizes="(max-width: 800px) 100vw, 30vw" width="{w['w']}" height="{w['h']}" alt="{escape(w['alt'])}" loading="lazy" decoding="async"><strong>{label}</strong><span>{n} works</span></a>''')

    def artist_card(aid):
        a = by_id[aid]
        w = next(item for item in works if item["artist"] == aid)
        return f'''<a class="artist-card" href="artist.html?artist={a['id']}"><img src="images/art/{w['id']}-640.webp" srcset="images/art/{w['id']}-640.webp 640w, images/art/{w['id']}-1100.webp 1100w" sizes="(max-width: 700px) 46vw, 22vw" width="{w['w']}" height="{w['h']}" alt="{escape(w['alt'])}" loading="lazy" decoding="async"><h3>{escape(a['name'])}</h3><p>{escape(a['city'])}, {escape(a['country'])}</p></a>'''

    featured = "".join(artist_card(i) for i in ["priya-menon", "lina-voss", "mateo-ruiz", "jonah-adeyemi"])
    watch = "".join(artist_card(i) for i in ["kenji-mori", "amina-diallo", "ines-laurent", "soren-hale"])

    index = f'''
<main id="content">
  <figure class="hero-media">
    <img src="images/art/harbour-weather-1700.webp" srcset="images/art/harbour-weather-1100.webp 1100w, images/art/harbour-weather-1700.webp 1700w" sizes="100vw" width="{hero['w']}" height="{hero['h']}" alt="{escape(hero['alt'])}" fetchpriority="high" decoding="async">
  </figure>
  <div class="hero-caption">
    <div>
      <h1>Original paintings, offered quietly.</h1>
      <p class="lede">Harbour Weather, oil on canvas, {escape(hero_artist['name'])}. Eight studios. The prices are illustrative. Every inquiry opens on WhatsApp, with the piece named in the message.</p>
    </div>
    <div class="hero-actions">
      <a class="btn" href="artwork.html?id=harbour-weather">View this work</a>
      <a class="btn btn-ghost" href="browse.html">Browse the catalogue</a>
    </div>
  </div>
  <section class="section" aria-labelledby="shop-cat">
    <div class="section-head"><h2 id="shop-cat">Shop by category</h2></div>
    <div class="cat-grid">{''.join(cat_html)}</div>
  </section>
  <section class="section" aria-labelledby="north">
    <div class="section-head"><h2 id="north">The north room</h2><a href="browse.html?style=Abstract">Abstract work</a></div>
    <div class="feature-grid"><div class="lead">{lead}</div><div class="stack">{side}</div></div>
  </section>
  <section class="section" aria-labelledby="styles">
    <div class="section-head"><h2 id="styles">Shop by style</h2></div>
    <div class="style-list">{style_html}</div>
  </section>
  <section class="section" aria-labelledby="price-bands">
    <div class="section-head"><h2 id="price-bands">Shop by price</h2></div>
    <div class="band-grid">{''.join(band_html)}</div>
  </section>
  <section class="section" id="artists" aria-labelledby="featured-artists">
    <div class="section-head"><h2 id="featured-artists">Featured artists</h2></div>
    <div class="artist-grid">{featured}</div>
  </section>
  <section class="section" aria-labelledby="watch">
    <div class="section-head"><h2 id="watch">Artists to watch</h2></div>
    <div class="artist-grid">{watch}</div>
  </section>
  <section class="commission">
    <div>
      <h2>A piece made for a particular wall.</h2>
      <p>Tell us the room, the light, and the scale. We will open a WhatsApp note to the studio. This is a commission inquiry, not a checkout.</p>
    </div>
    <a class="btn" href="{COMMISSION}">Request a commission</a>
  </section>
</main>'''

    (ROOT / "index.html").write_text(document(
        "Artvue — Original paintings, offered by inquiry",
        "Artvue is a demo art marketplace. Browse fictional paintings, drawings, photographs, prints, and sculpture, then inquire on WhatsApp. Illustrative prices. No checkout.",
        "index.html",
        index,
        ["js/site.js"],
        preload=True,
    ), encoding="utf-8")

    mediums = ["Oil", "Acrylic", "Watercolour", "Ink", "Photograph", "Pigment print", "Ceramic"]
    sizes = ["Small", "Medium", "Large"]
    orients = ["Portrait", "Landscape", "Square"]
    prices = [
        ("under-500", "Under $500"),
        ("500-1500", "$500 – $1,500"),
        ("1500-4000", "$1,500 – $4,000"),
        ("over-4000", "Above $4,000"),
    ]
    filters = f'''
<form id="filters" class="filters" action="browse.html" method="get">
  <div class="drawer-bar">
    <h2>Filters</h2>
    <button class="drawer-close" type="button">Close</button>
  </div>
  <fieldset><legend>Category</legend>{''.join(checkbox('category', c) for c in ['Painting','Drawing','Photography','Prints','Sculpture'])}</fieldset>
  <fieldset><legend>Style</legend>{''.join(checkbox('style', s) for s in styles)}</fieldset>
  <fieldset><legend>Medium</legend>{''.join(checkbox('medium', m) for m in mediums)}</fieldset>
  <fieldset><legend>Price</legend>{''.join(f'<label><input type="radio" name="price" value="{v}"> {escape(lab)}</label>' for v, lab in prices)}</fieldset>
  <fieldset><legend>Size</legend>{''.join(checkbox('size', s) for s in sizes)}</fieldset>
  <fieldset><legend>Orientation</legend>{''.join(checkbox('orientation', o) for o in orients)}</fieldset>
  <p style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px"><button class="btn" id="show-works" type="submit">Show works</button><button class="btn btn-ghost" id="clear-filters" type="button">Clear</button></p>
</form>'''

    cards = "".join(card(w, by_id[w["artist"]], eager=(i < 3)) for i, w in enumerate(works))
    browse = f'''
<main id="content" class="page">
  <h1 class="page-title">The catalogue</h1>
  <p class="page-intro">Filter by category, style, medium, price, size, and orientation. Sort by price or year. Saving a work keeps it on this device.</p>
  <div class="browse-layout">
    {filters}
    <div>
      <div class="toolbar">
        <button class="btn btn-ghost filter-open" type="button" aria-expanded="false" aria-controls="filters">Filters</button>
        <p id="result-count">{len(works)} works</p>
        <label class="sort-field">Search
          <input id="q" type="search" name="q" placeholder="Title or artist" aria-label="Search title or artist">
        </label>
        <label class="sort-field">Sort
          <select id="sort" name="sort" aria-label="Sort works">
            <option value="featured">Featured</option>
            <option value="price-asc">Price, low to high</option>
            <option value="price-desc">Price, high to low</option>
            <option value="newest">Newest</option>
          </select>
        </label>
      </div>
      <div class="works" id="works">{cards}</div>
      <div class="empty" id="empty" hidden>
        <h2>Nothing in this edit.</h2>
        <p>Clear a filter, or return to the full catalogue.</p>
      </div>
    </div>
  </div>
</main>'''
    (ROOT / "browse.html").write_text(document(
        "Browse the catalogue — Artvue",
        "Filter Artvue’s demo catalogue by category, style, medium, price, size, and orientation. Fictional artists, illustrative prices, WhatsApp inquiries.",
        "browse.html",
        browse,
        ["js/site.js", "js/browse.js"],
    ), encoding="utf-8")

    artwork = '''
<main id="content" class="page">
  <article class="lot" id="lot"><p>Opening the work…</p></article>
  <section class="more" id="more" aria-label="More from this artist"></section>
  <dialog class="lightbox" id="lightbox" aria-label="Enlarged view">
    <div class="lightbox-bar">
      <p id="lightbox-caption" style="margin:0">Click the picture to look closer.</p>
      <button class="btn btn-ghost" type="button" id="close-lightbox">Close</button>
    </div>
    <div class="lightbox-frame"><img id="lightbox-img" alt=""></div>
  </dialog>
</main>'''
    (ROOT / "artwork.html").write_text(document(
        "Artwork — Artvue",
        "View a work from the Artvue demo catalogue: image, medium, size, and price, then inquire on WhatsApp.",
        "artwork.html",
        artwork,
        ["js/catalog.js", "js/site.js", "js/artwork.js"],
    ), encoding="utf-8")

    artist = '''
<main id="content" class="page" id="studio"><p>Opening the studio…</p></main>'''
    (ROOT / "artist.html").write_text(document(
        "Artist — Artvue",
        "A fictional artist on Artvue, with the works currently in the demo catalogue.",
        "artist.html",
        artist,
        ["js/catalog.js", "js/site.js", "js/artist.js"],
    ), encoding="utf-8")

    about = f'''
<main id="content" class="page prose">
  <h1 class="page-title">How Artvue works</h1>
  <p class="page-intro">Artvue is a demonstration gallery. The artists are invented. The prices are there so the catalogue can be read the way a real one is read. You cannot pay here.</p>
  <div class="steps">
    <article class="step"><h2>Look</h2><p>Use the catalogue. Category, style, medium, price, size, and orientation all narrow the same floor. The address bar keeps the edit you made, so a link can be sent as-is.</p></article>
    <article class="step"><h2>Read the lot line</h2><p>Each work carries a title, an artist, a medium, a size, a year, and a price in US dollars. A sold work stays visible, marked, so the wall does not pretend it is still free.</p></article>
    <article class="step"><h2>Inquire</h2><p>Buy / Inquire on WhatsApp opens a message that already names the piece, the artist, the size, the price, and this page. A person replies. There is no cart.</p></article>
    <article class="step"><h2>Commission, if you need a specific wall</h2><p><a href="{COMMISSION}">Request a commission</a> starts a separate note. Say the room and the scale. The studio side of that conversation is also fictional in this demo.</p></article>
  </div>
  <p>Demo marketplace: fictional artists and illustrative prices.</p>
</main>'''
    (ROOT / "about.html").write_text(document(
        "How Artvue works — Artvue",
        "How the Artvue demo works: browse the catalogue, read the lot line, and inquire on WhatsApp. No cart and no payment.",
        "about.html",
        about,
        ["js/site.js"],
    ), encoding="utf-8")

    sell = f'''
<main id="content" class="page prose">
  <h1 class="page-title">Sell your art</h1>
  <p class="page-intro">Artvue is not taking applications into a live market. This page shows how an artist would ask to be included. There is no form and no account. The note goes to WhatsApp.</p>
  <div class="steps">
    <article class="step"><h2>What to send</h2><p>Your name, the city you work in, a link if you have one, and three works with medium and size. A sentence on what you want the work to do in a room is enough.</p></article>
    <article class="step"><h2>What this demo will not do</h2><p>It will not store the message, invoice a buyer, or ship a crate. The number on the button is the only contact, and it belongs to this demonstration.</p></article>
  </div>
  <p><a class="btn btn-wa" href="{SELL}">Apply on WhatsApp</a></p>
</main>'''
    (ROOT / "sell.html").write_text(document(
        "Sell your art — Artvue",
        "Apply to show work on the Artvue demo. The application opens WhatsApp. There is no form backend.",
        "sell.html",
        sell,
        ["js/site.js"],
    ), encoding="utf-8")

    rows = []
    for w in works:
        license_name = "Pexels License" if w["kind"] == "pexels" else "Unsplash License"
        rows.append(
            f'<tr><td>{escape(w["title"])}</td><td>{escape(w["kind"].title())}</td><td>{escape(w["pid"])}</td><td><a href="{credit_page(w)}">Source page</a></td><td>{license_name}</td></tr>'
        )
    credits = f'''
<main id="content" class="page">
  <h1 class="page-title">Image credits</h1>
  <p class="page-intro">Every picture on Artvue is a stock photograph used as an illustration. The artists named beside them are fictional. The photographs are not documents of those artists’ hands.</p>
  <table class="credits">
    <thead><tr><th>Shown as</th><th>Source</th><th>Photo id</th><th>Link</th><th>License</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <p class="fine">Pexels license: <a href="https://www.pexels.com/license/">pexels.com/license</a>. Unsplash license: <a href="https://unsplash.com/license">unsplash.com/license</a>.</p>
</main>'''
    (ROOT / "credits.html").write_text(document(
        "Image credits — Artvue",
        "Sources for the photographs illustrating the Artvue demo catalogue, with photo ids and license links.",
        "credits.html",
        credits,
        ["js/site.js"],
    ), encoding="utf-8")


def main():
    print("downloading", len(WORKS))
    with ThreadPoolExecutor(8) as pool:
        list(pool.map(download, WORKS))
    artists = {a["id"]: a for a in ARTISTS}
    catalog_works = []
    for order, work in enumerate(WORKS):
        w, h = to_webp(work)
        width_cm, height_cm, orientation, size, label, _ = dims(w, h, work["long_cm"])
        artist = artists[work["artist"]]
        item = {
            "id": work["id"],
            "title": work["title"],
            "artistId": work["artist"],
            "artist": work["artist"],
            "category": work["category"],
            "style": work["style"],
            "medium": work["medium"],
            "medium_group": work["medium_group"],
            "year": work["year"],
            "price": work["price"],
            "sold": work["sold"],
            "orientation": orientation,
            "size": size,
            "size_label": label,
            "width_cm": width_cm,
            "height_cm": height_cm,
            "w": w,
            "h": h,
            "order": order,
            "blurb": work["blurb"],
            "alt": f"{work['title']}, {work['medium']} by {artist['name']}",
            "kind": work["kind"],
            "pid": work["pid"],
        }
        catalog_works.append(item)
        print(f"{item['id']}: {w}x{h} {orientation} {size} {label}")

    public_works = []
    for item in catalog_works:
        public_works.append({k: item[k] for k in [
            "id", "title", "artistId", "category", "style", "medium", "medium_group",
            "year", "price", "sold", "orientation", "size", "size_label", "w", "h",
            "order", "blurb", "alt",
        ]})
    payload = {"artists": ARTISTS, "works": public_works}
    (ROOT / "js" / "catalog.js").write_text(
        "window.ARTVUE = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    sources = []
    for item in catalog_works:
        sources.append({
            "file": f"images/art/{item['id']}-640.webp",
            "also": f"images/art/{item['id']}-1100.webp",
            "source": item["kind"],
            "photoId": item["pid"],
            "sourcePage": credit_page(item),
            "originUrl": source_url(item),
            "license": "Pexels License" if item["kind"] == "pexels" else "Unsplash License",
            "note": "Stock photograph used as an illustration for a fictional catalogue entry.",
        })
    (IMG / "SOURCES.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")
    build_pages(catalog_works, ARTISTS)
    (ROOT / "favicon.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" fill="#f3efe6"/>
  <rect x="3.5" y="3.5" width="25" height="25" fill="none" stroke="#1c1916" stroke-width="1.25"/>
  <path d="M9 24 L16 7.5 L23 24" fill="none" stroke="#1c1916" stroke-width="1.25"/>
  <path d="M11.6 18.2 H20.4" stroke="#8a7040" stroke-width="1.25"/>
</svg>
''', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    urls = ["", "browse.html", "artwork.html", "artist.html", "about.html", "sell.html", "credits.html"]
    body = "\n".join(f"  <url><loc>{BASE}/{u}</loc></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("pages written", len(catalog_works), "works")


if __name__ == "__main__":
    main()
