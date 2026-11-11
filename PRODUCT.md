# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

plain static HTML/CSS/vanilla JS, no framework and no build step. Deployed on GitHub Pages from the repository root on `main` at https://mohammedbagowabair.github.io/Artvue-Art-Marketplace-Website/

Inferred from the explicit brief. No structured question tool was available in this session, so nothing here was confirmed in a live interview.

## Users

A visitor browsing a demonstration art marketplace: looking at works, filtering the catalogue, opening an artwork or an artist, and starting a conversation on WhatsApp. A second audience is a fictional artist applicant who uses the sell page to open that same WhatsApp thread. Inferred from the brief’s page list and calls to action.

## Product Purpose

Artvue is a demo online marketplace for original art. It lets someone browse fictional works and inquire or request a commission on WhatsApp. Success is a fast, credible gallery visit that ends in a WhatsApp conversation, with no cart and no payment.

## Positioning

Inquiries go only to one WhatsApp number. The site does not take payment, hold stock, or pretend the artists are real. Prices are illustrative. A neighbouring storefront that checks out in-page could not truthfully copy that limit.

## Operating Context

Desktop and mobile browsers, including 360px widths. Visitors move through home, browse, artwork, artist, about, sell, and image credits. Favourites stay in localStorage on the device. Every commercial action opens WhatsApp with a prefilled message.

## Capabilities and Constraints

- Fictional brand name: Artvue. Do not copy Saatchi Art’s name, logo, copy, or images. Layout and browsing patterns may follow that kind of clean white premium marketplace: category navigation, editorial banners, shop-by facets, curated collections, artist highlights, artwork cards.
- Six to eight fictional artists from different countries. Twenty-four to thirty artworks across Painting, Drawing, Photography, Prints, and Sculpture, with styles Abstract, Figurative, Landscape, Pop, and Minimal.
- Each work shows title, artist, medium, size, orientation, year, USD price, and a Sold badge where marked.
- Site-wide note, verbatim: “Demo marketplace: fictional artists and illustrative prices.”
- Browse filters: category, style, medium, price range, size, orientation. Sort by price and newest. Result count. Filter state in the URL. Mobile filter drawer.
- Artwork page: large image, zoom or lightbox, details, more from this artist, WhatsApp actions. Artist page by query. About / how it works. Optional sell page with a WhatsApp application and no form backend.
- Favourites in localStorage are in scope. Cart, checkout, and payments are out of scope.
- The only WhatsApp number is 967783964784.
- Royalty-free photographs stored in the repo as optimised WebP with srcset, width, height, lazy loading, and a credits page.
- Accessibility and SEO: per-page title, meta description, Open Graph, alt text, semantic HTML, SVG favicon, contrast, visible focus, reduced motion. Responsive from 360px with no horizontal scroll. Lighthouse performance and SEO 90+ on home and browse.
- English only. USD display. Inferred.

## Brand Commitments

- Name: Artvue.
- Required disclaimer: “Demo marketplace: fictional artists and illustrative prices.”
- Binding reference: the information architecture and browsing patterns of a clean white premium art marketplace. Identity, wording, and pictures must be original.
- Voice: calm, specific, short. No borrowed slogans.

## Evidence on Hand

No real artists, artworks, prices, or testimonials exist for this brand. All catalogue content is fictional and must stay labelled as a demo. Photographs are stock sources credited on the credits page; they illustrate the catalogue and are not documents of the fictional artists’ hands.

## Product Principles

- The artwork is the product; chrome stays quiet.
- Every sale-shaped action is a WhatsApp inquiry, never a payment step.
- The demo limit is visible, not hidden in a footer only.
- Filters and facts (medium, size, price, availability) stay clearer than atmosphere.
- A page must stay usable with a keyboard, at 360px, and with motion reduced.

## Accessibility & Inclusion

Target includes Lighthouse SEO 90+, text alternatives, semantic structure, visible focus, contrast, and `prefers-reduced-motion`. No other assistive-technology standard was specified.
