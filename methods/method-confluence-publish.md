# Methode: Confluence Publish

Doel: kennisdocumentatie uit `overlay/` publiceren en/of updaten als Confluence-paginastructuur met dezelfde content-mapping als de MkDocs-export.

Input (optioneel):

- scope: `overlay` (vast)
- include: glob patterns (default: leeg)
- exclude: glob patterns (default: o.a. `export/**`, `.git/**`, `node_modules/**`, `dist/**`)
- confluence_base_url: basis-URL van de Atlassian-tenant (bijv. `https://<tenant>.atlassian.net`)
- confluence_space_key: Confluence space key
- confluence_parent_page_id: optioneel parent page ID waaronder sectiepagina's worden geplaatst
- confluence_title_prefix: optionele prefix voor paginatitels
- confluence_dry_run: `true` | `false` (default: `true`)

Output:

- Confluence-pagina's per sectie uit `overlay/mkdocs_profile.json`
- upsert-rapport in `export/confluence-publish-YYYYMMDD-HHMM.json`

Regels:

- Schrijft lokaal niets buiten `export/`.
- Herschrijft broncontent uit `overlay/` naar coherente, informatieve tekst in plaats van letterlijk te kopieren.
- Publiceert uitsluitend kennis uit `overlay/`; content uit `core/` komt nooit in Confluence-output terecht.
- Sluit content uit `overlay/meetings` en `overlay/planning` uit; deze zijn niet bedoeld voor publicatie.
- Respecteert taxonomy: exporteert/publiceert geen content buiten de gekozen scope en houdt core/overlay strikt gescheiden.
- De informatie-architectuur komt uit `overlay/mkdocs_profile.json` (per overlay aanpasbaar).
- De publisher bewaart stabiele document-naar-sectie toewijzingen in `overlay/mkdocs_nav_lock.json` zodat kennis niet bij elke run van plek wisselt.
- Maakt ontbrekende doelpagina's toch aan met placeholdertekst zodat de publicatiestructuur stabiel blijft.
- Bij `confluence_dry_run=true` worden geen API-write calls uitgevoerd; alleen het rapport wordt geschreven.

Implementatie:

- De canonieke implementatie staat in `core/methods/confluence_publish.py`.
- Content-classificatie en section mapping volgen hetzelfde principe als `mkdocs_export.py`.
- Eigenstaand profiel: `overlay/confluence_profile.json` (optioneel; fallback op `overlay/mkdocs_profile.json` als niet aanwezig).
- Eigenstaande nav lock: `overlay/confluence_nav_lock.json` (apart van mkdocs-variant voor onafhankelijke klassificaties).
- Confluence-authenticatie verloopt via environment variabelen (`CONFLUENCE_BASE_URL`, `CONFLUENCE_SPACE_KEY`, `CONFLUENCE_USERNAME`, `CONFLUENCE_API_TOKEN`).
- Bij wijzigingen aan publicatiestructuur of configuratie wordt eerst de Python-implementatie aangepast; deze methode beschrijft alleen doel, input, output en regels.
