# Methode: Knowledge Extract

Doel: kennis uit markdown in `overlay/` deterministisch extraheren naar losse knowledge points in YAML.

Input (optioneel):

- scope: pad onder `overlay/` (default: `overlay/`)
- include: glob patterns (default: `**/*.md`)
- exclude: glob patterns (default: `**/archive/**`, `**/*.bak.md`)
- mode: `full` | `incremental` (default: `incremental`)
- recall_profile: `balanced` | `high` (default: `high`)
- approval_mode: `per_point` | `batch` (default: `per_point`)

Output:

- per knowledge point 1 YAML-bestand
- output staat centraal in `overlay/knowledge/<type>/`
- bestandsnaam: `<bronnaam>.kp-<volgnummer>.yaml`
- schrijfactie vindt pas plaats na expliciete gebruikersgoedkeuring

Regels:

- Leest alleen markdown binnen `overlay/`.
- Schrijft alleen knowledge-point YAML-bestanden in `overlay/knowledge/<type>/`.
- Wijzigt nooit de markdown-broninhoud.
- Gebruikt verplicht schema uit `core/configuration/knowledge_point_schema.yaml`.
- Elke knowledge point bevat precies 1 atomaire claim.
- Elk YAML-bestand bevat precies 1 knowledge point.
- Elk punt krijgt exact 1 primair `type`.
- Elk punt bevat herleidbaarheid via `source_refs` (1..n bronnen).
- Bij herextractie worden bestaande punten niet stilzwijgend verwijderd; verouderde punten krijgen `status: superseded`.
- Voor elk gevonden knowledge point wordt eerst een voorstel getoond met type, statement, confidence, applies_to en bronquote.
- Zonder expliciete goedkeuring wordt geen nieuw bestand gemaakt en geen bestaand bestand aangepast.

Goedkeuringsworkflow:

- Stap 1: presenteer per kandidaat-point een voorstel met beoogde actie.
- Stap 2: vraag expliciet akkoord of aanpassing.
- Stap 3: voer pas na antwoord de actie uit.
- Ondersteunde acties per punt: `approve`, `edit`, `skip`, `merge`.
- `approve`: voorstel ongewijzigd uitvoeren.
- `edit`: voorstel eerst aanpassen volgens feedback, daarna opnieuw bevestigen.
- `skip`: punt niet vastleggen.
- `merge`: geen nieuw bestand, maar `source_refs` uitbreiden op bestaand equivalent punt.
- Defaultgedrag zonder antwoord is `skip`.

Voorsteltemplate per knowledge point:

- kandidaat-id
- type (voorgesteld)
- statement (voorgesteld)
- confidence (voorgesteld)
- applies_to (voorgesteld)
- source_ref (file, heading, quote)
- beoogde actie: `create` of `merge`
- vraag: "Akkoord, aanpassen of overslaan?"

Deduplicatie:

- Controleer altijd eerst of het knowledge point al bestaat binnen de gekozen scope.
- Bestaat het al: maak geen nieuw YAML-bestand aan.
- Bestaat het al: breid alleen de bronverwijzingen uit door een extra entry toe te voegen aan `source_refs`.
- Voeg dezelfde bron niet dubbel toe; broncombinatie `file + heading + quote` is uniek.
- Alleen bij afwezigheid van een bestaand equivalent punt mag een nieuw YAML-bestand worden aangemaakt.
- Ook bij een deduplicatie-match is expliciete gebruikersgoedkeuring vereist voordat `source_refs` wordt uitgebreid.

Interpretatieregels:

- `fact` en `observation` alleen gebruiken voor verifieerbare uitspraken.
- `opinion`, `assumption` en `hypothesis` krijgen standaard geen `high` confidence zonder expliciet bewijs.
- `requirement`, `constraint`, `decision` en `risk` krijgen prioriteit voor expliciete `source_refs.quote`.
- Ambigue samengestelde zinnen altijd opsplitsen in meerdere punten.
- Bij classificatietwijfel: kies conservatieve typering (`assumption` of `question`) boven over-assertie.

Extractiestrategie (high-recall):

- Voer extractie uit in 4 passes: structureel, normatief, relationeel en restscan.
- Pass 1 structureel: extraheer kandidaten uit headings, alinea-kernzinnen, opsommingen en tabellen.
- Pass 2 normatief: extraheer alle uitspraken met modaliteit zoals moet, mag niet, verplicht, altijd, nooit, vereist.
- Pass 3 relationeel: extraheer expliciete oorzaak-gevolg, afhankelijkheden, voorwaarden en uitzonderingen.
- Pass 4 restscan: controleer of alle informatieve zinnen zonder match alsnog als kandidaat zijn beoordeeld.

Dekkingsregels:

- Elke betekenisvolle bullet in een lijst wordt standaard een eigen kandidaat-point.
- Elke normatieve zin wordt altijd minimaal 1 kandidaat-point.
- Elke expliciete definitie, regel, anti-pattern, risico, open punt en succescriterium wordt apart vastgelegd.
- Samenvattingen mogen alleen als extra punt; ze vervangen geen onderliggende detailpunten.
- Doel is hoge dekking: liever te veel kandidaten en daarna deduplicatie dan te weinig extractie.

Kwaliteitsdrempels per bronbestand:

- Minimaal 1 knowledge point per betekenisvolle lijstitem-groep.
- Minimaal 1 knowledge point per sectie met regels, principes of criteria.
- Minimaal 1 knowledge point per expliciet genoemde anti-pattern of risico.
- Als output opvallend laag is t.o.v. bronlengte: voer automatisch een tweede high-recall pass uit.

Opsplitsregels:

- Zinnen met en/of, mits, tenzij, omdat, daarom, zodat worden opgesplitst zodra ze meerdere zelfstandige claims bevatten.
- Combinaties van regel + rationale worden in twee points gezet: `requirement/constraint` en `rationale`.
- Combinaties van observatie + oordeel worden opgesplitst in `observation` en `opinion` of `assumption`.

Equivalentiebepaling:

- Beschouw punten als equivalent als `type` gelijk is en de genormaliseerde kernclaim dezelfde betekenis heeft.
- Gebruik `applies_to` als extra check; bij conflict geen merge maar nieuw punt.
- Bij twijfel geen merge uitvoeren; maak dan een nieuw punt met lagere confidence.

Determinisme:

- Gebruik stabiele id's: `kp-<bronprefix>-<volgnummer>`.
- Gebruik volgnummer op basis van volgorde van voorkomen in de bron.
- Gebruik outputmap op basis van exact `type` (enum-waarde) als subfolder onder `overlay/knowledge/`.
- Hanteer consistente datumformaten (`generated_at` ISO-8601 UTC, `updated_at` YYYY-MM-DD).
- Gebruik consistente `applies_to` labels op basis van foldercontext en expliciete brontermen.

Validatie:

- Elk gegenereerd YAML-bestand moet schema-conform zijn.
- Bij validatiefouten: markeer bestand als niet geslaagd en rapporteer veldspecifieke afwijkingen.
- Elke `source_refs[*].file` moet verwijzen naar een markdownbestand in `overlay/`.
- Na elke goedgekeurde schrijfactie opnieuw valideren op schema-conformiteit.

Niet-doen:

- Geen semantische verrijking toevoegen die niet direct uit broninhoud of expliciet afleidbare context komt.
- Geen bundeling van meerdere knowledge points in 1 YAML-bestand.
- Geen nieuwe taxonomy of typecategorieen introduceren buiten de schema-enum.
