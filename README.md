# Frontier 1905

An interactive map of the ideas that led to Einstein's special relativity (received by Annalen der Physik on 30 June 1905).

The circle is the edge of human knowledge in 1905, with time running outward from the centre. Each dot is an idea, placed by field and date. Choose any idea to see what it was built on and what it led to. Special relativity sits on the swell in the rim, where synthesis across fields pushed the frontier outward. The hatched shapes beyond the rim are ideas that came after.

## Files

- `index.html` is the public page. It is self-contained: code, data, images and fonts are all inside it, so it works offline and on any static host.
- `src/frontier-1905.html` is the design source. It includes the colour editor and loads fonts from Google Fonts.
- `src/head.html` holds the page title, description and sharing tags.
- `build.py` makes `index.html` from `src/`. Run `python3 build.py` after changing the source.
- `assets/` holds the social preview image and icons.

## Credits

Images come from Wikimedia Commons; each one's source and licence is listed in the page under "Image credits". Fonts are Libre Caslon Text (Pablo Impallari and Rodrigo Fuenzalida) and IBM Plex Sans Condensed and IBM Plex Mono (IBM), all under the SIL Open Font License 1.1.
