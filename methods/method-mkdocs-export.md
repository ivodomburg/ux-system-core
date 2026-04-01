# Methode: MkDocs Export

Doel: kennisdocumentatie exporteren als MkDocs-site in een downloadbare zip.

Input (optioneel):

- scope: `overlay` (vast)
- include: glob patterns (default: leeg)
- exclude: glob patterns (default: o.a. `export/**`, `.git/**`, `node_modules/**`, `dist/**`)

Output:

- 1 zip-bestand in `export/` (bijv. `export/mkdocs-export-YYYYMMDD-HHMM.zip`)
- in de zip:
  - `mkdocs.yml`
  - `docs/` met gekopieerde markdown
  - `README_EXPORT.md` met build/serve instructies

Regels:

- Schrijft niets buiten `export/`.
- Herschrijft broncontent uit `overlay/` naar coherente, informatieve tekst in plaats van letterlijk te kopiëren.
- Exporteert uitsluitend kennis uit `overlay/`; content uit `core/` komt nooit in de MkDocs-export terecht.
- Sluit content uit `overlay/meetings` en `overlay/planning` uit; deze zijn niet bedoeld voor publicatie.
- Behoudt bestaande relatieve links waar mogelijk; rapporteert gebroken links als waarschuwingen.
- Respecteert taxonomy: exporteert geen content buiten de gekozen scope en houdt core/overlay strikt gescheiden in de MkDocs structuur.
- Core bevat geen projectspecifieke navigatiestructuur.
- De informatie-architectuur komt uit `overlay/mkdocs_profile.json` (per overlay aanpasbaar).
- De exporter bewaart stabiele document-naar-sectie toewijzingen in `overlay/mkdocs_nav_lock.json` zodat kennis niet bij elke export van plek wisselt.
- Maakt ontbrekende doelpagina's toch aan met placeholdertekst zodat de navigatie ongewijzigd blijft.

Implementatie:

- De canonieke implementatie staat in `core/methods/mkdocs_export.py`.
- De inhoud van `mkdocs.yml` wordt opgebouwd uit `overlay/mkdocs_profile.json`.
- Sectie-indeling is overlay-specifiek; de engine in core is generiek en herbruikbaar.
- Bij wijzigingen aan exportstructuur of configuratie wordt eerst de Python-implementatie aangepast; deze methode beschrijft alleen doel, input, output en regels.
