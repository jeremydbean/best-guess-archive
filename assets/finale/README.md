# Finale assets

## `crew-photo.jpg` (or `crew-photo.png`)

The cast-and-crew photo from the final episode, Friday, August 28, 2026 —
the moment Howie and Hunter called everyone in front of the camera during
the Outro.

Drop the file in here under either name. `_finalePhotoHtml()` in `index.html`
tries `.jpg` first, then `.png`, and removes the whole `<figure>` if neither
resolves — so the end-of-series card shows the photo as soon as the file
lands, and shows nothing (not a broken image) while it is missing.

Nothing else needs editing to turn it on.
