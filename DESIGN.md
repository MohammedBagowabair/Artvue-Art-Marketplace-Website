# Artvue

Auction-catalogue register. Ivory ground, charcoal ink, one brass line. Paintings carry the colour.

## Colour

- Ivory `#f3efe6` page
- Ivory deep `#e8e2d4` image wells
- Ink `#1c1916` text, header note, primary buttons
- Soft ink `#3c372f` supporting copy
- Muted `#4a443c` meta
- Line `#d8d0c2`
- Brass `#8a7040` used as a 1px rule under the wordmark and under a few links, not as a fill
- Sold `#6e2d2a`
- WhatsApp `#0d5c45` with ivory text

## Type

- Display: EB Garamond italic 500, self-hosted. Headings and artwork titles.
- Prices and the wordmark: EB Garamond roman 500.
- UI: Source Sans 3, 400 body and 500 for navigation and buttons.
- Navigation and buttons: uppercase, about 0.14em tracking, 0.75–0.78rem.

## Layout

- Page padding `clamp(18px, 4vw, 72px)`.
- Home opens with a full-bleed painting, then a lot line on ivory. No text on the picture.
- Catalogue: sticky filter column from 901px, drawer below that.
- Cards are the picture, then italic title, artist, medium and size, price. No card shadow.
- Sections stack with large vertical padding. Rules are 1px.

## Motion

- The opening painting settles from a slight scale over 1.8s.
- Card images ease to 1.025 on hover over 0.7s.
- The filter drawer slides in over 0.45s.
- `prefers-reduced-motion: reduce` removes animation and transition.
