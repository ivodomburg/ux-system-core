---
title: Methode: Action Points — Actiepuntenbeheer
type: Methods
version: 1.0
language: nl
description: Systematische registratie, beheer en prioritering van actiepunten uit overlay-bronnen
---

# Methode: Action Points

Doel: actiepunten uit de overlay deterministisch vastleggen, beheren, prioriteren en verwijderen met behoud van status en traceerbaarheid.

## 1. Action Points opbouw

Elk actiepunt bevat verplicht:

- **id**: unieke identifier (bijv. `ap-2026-001`)
- **titel**: beschrijvende actie in 5-10 woorden
- **beschrijving**: korte inhoudelijke toelichting (1-2 alinea's)
- **bron**: referentie naar markdown bestand in `overlay/` (pad en optioneel heading)
- **status**: `todo` | `done`
- **prioriteit**: `hoog` | `middel` | `laag`
- **urgentie**: `onmiddellijk` | `korttermijn` | `middellang` | `langetermijn` (automatisch afgeleid of manueel)
- **impact**: `hoog` | `middel` | `laag` (automatisch afgeleid uit context of manueel)
- **aangemaakt_op**: ISO 8601 timestamp
- **gewijzigd_op**: ISO 8601 timestamp
- **afgerond_op**: ISO 8601 timestamp (null als status != done)

## 2. Opslaglocatie

- Databron: `overlay/action_points/action_points.json` — machine-leesbare canonical bron, schema-conform
- Leesbare weergave: `overlay/action_points/action_points.md` — automatisch gegenereerd na elke schrijfactie, nooit handmatig bewerken
- Elke export (mkdocs, confluence) **sluit** actiepunten uit (`overlay/action_points/` staat op exclude-lijst)

> `action_points.md` is altijd afgeleid van `action_points.json`. Wijzigingen uitsluitend via de methode.

## 3. Invoeg-methode: action-points-extract

### Input (optioneel):

- `scope`: pad onder `overlay/` (default: `overlay/`)
- `include`: glob patterns (default: `**/*.md`)
- `exclude`: glob patterns (default: `action_points/**`, `**/archive/**`, `**/*.bak.md`, `**/resources/**`)
- `mode`: `full` | `incremental` (default: `incremental`)
- `auto_extract`: `true` | `false` (default: `true`)

### Output:

- Actiepunten toegevoegd aan `overlay/action_points/action_points.json`
- Koppelingen naar bron via `bron` veld
- Voor elk nieuw actiepunt: voorstel met titel, beschrijving, bron en voorgestelde prioriteit
- Schrijfactie vindt plaats na expliciete gebruikersgoedkeuring

### Regels:

- Leest alleen markdown binnen `overlay/` (exclusief `action_points/`)
- Schrijft alleen naar `overlay/action_points/`
- Wijzigt nooit bron-markdown
- Detecteert potentiële actiepunten op basis van patronen:
  - Lijn begint met `[ ]` of `- [ ]` (onafgevinkte checklist-items)
  - Expliciet: "actiepunt", "todo", "action item", "volgende stap"
  - Impliciet: "moet nog", "dient te", "te doen", "open vraag", "beslissing nodig"
  - Risico's met mitigatie-acties
  - Gapanalyses met vervolgacties
- Voor elk gevonden kandidaat-actiepunt: toon voorstel met titel, beschrijving, bron en vraag om:
  - Goedkeuring (`approve`)
  - Afwijzing (`skip`)
  - Aanpassing (`edit`)
- Default gedrag zonder antwoord: `skip`
- Standaard prioriteit van nieuwe punten: `middel`, tenzij uit context `hoog` of `laag` duidelijk is
- Standaard urgentie: vraag manueel tenzij context expliciet is (bijv. "onmiddellijk", "volgende sprint")

### Voorsteltemplate:

```
ID: ap-<datum>-<nummer>
Titel: [voorgestelde titel]
Beschrijving: [voorgestelde beschrijving]
Bron: overlay/[pad].md#[heading]
Prioriteit (voorgesteld): middel
Urgentie (voorgesteld): [vraag aan gebruiker]

Vraag: Goedkeuren, aanpassen of overslaan?
```

---

## 4. Verwijder-methode: action-points-clear

Doel: afgemaakte actiepunten (status = `done`) verwijderen uit het register.

### Input (optioneel):

- `older_than`: aantal dagen (default: 7)
- `auto_clear`: `true` | `false` (default: `false`)

### Output:

- Gefilterde lijst van actiepunten die verwijderd zullen worden
- Bevestiging van verwijdering

### Regels:

- Verwijdert alleen punten met status = `done`
- Verwijdert alleen punten die langer dan `older_than` dagen geleden zijn afgerond
- Vraagt altijd expliciete bevestiging voordat in `action_points.json` wordt geschreven
- Maakt backup van vorige state in `overlay/action_points/.action_points.backup.json` (voor tracering)

### Workflow:

- Stap 1: Toon lijst met kandidaten (`status = done`, `afgerond_op` > N dagen geleden)
- Stap 2: Vraag bevestiging
- Stap 3: Voer verwijdering uit

---

## 5. Prioriteer-methode: action-points-prioritize

Doel: actiepunten re-prioriteren op basis van impact en urgentie.

### Input:

- `strategy`: `impact-urgency` | `impact` | `urgency` | `custom` (default: `impact-urgency`)
- `scope`: actiepunt-ID of lijst van IDs (default: alle met status = `todo`)
- `recalculate_all`: `true` | `false` (default: `false`)

### Output:

- Herziene prioriteiten per actiepunt
- Prioriteitsmatrix (impact vs urgentie)
- Top-3 volgende acties

### Regels:

- Prioriteitsmatrix:
  ```
  Urgentie ↓ / Impact →  Hoog        Middel         Laag
  Onmiddellijk           HOOG        HOOG           MIDDEL
  Korttermijn            HOOG        MIDDEL         MIDDEL
  Middellang             MIDDEL      MIDDEL         LAAG
  Langetermijn           MIDDEL      LAAG           LAAG
  ```
- Bij `auto_extract` kan urgentie niet automatisch uit bron afgeleid worden → vraag manueel
- Wijzigt `gewijzigd_op` timestamp bij elke herziening

### Workflow:

- Stap 1: Voorstel nieuwe prioriteit op basis van urgentie + impact matrix
- Stap 2: Vraag per actiepunt: goedkeuren of aanpassen?
- Stap 3: Update bij goedkeuring
- Stap 4: Toon herziene Top-3 volgende acties

---

## 6. Update-methode: action-points-update-status

Doel: status van een actiepunt wijzigen van `todo` naar `done` of vice versa.

### Input:

- `id`: actiepunt-ID
- `new_status`: `todo` | `done`
- `note` (optioneel): korte opmerking (bijv. "afgerond in sprint 4")

### Output:

- Updated actiepunt in `action_points.json`
- Timestamp `gewijzigd_op` geactualiseerd
- If `new_status = done`: timestamp `afgerond_op` ingevuld (UTC ISO 8601)

### Regels:

- Schrijfactie na bevestiging
- Toont oude en nieuwe waarde ter controle

---

## 7. Interpretatieregels

- **Bron-herkennning**: actiepunten zijn minder formeel dan knowledge points, maar dienen traceerbaar terug te leiden naar bron
- **Deduplicatie**: controleer eerst of een soortgelijk actiepunt al bestaat voordat je een nieuw punt aanmaakt
- **Status-behoud**: wijzig status van bestaande punten nooit automatisch; markeer als `superseded` in plaats van te verwijderen
- **Export-uitsluiting**: actiepunten mogen **nooit** in mkdocs/confluence exports verschijnen
- **Case-gevoeligheid**: prioriteiten altijd lowercase (`hoog`, `middel`, `laag`)
- **Urgentie-vraag**: als urgentie niet uit bron blijkt → vraag altijd manueel, om datarightigheid te waarborgen

---

## 8. Goedkeuringsprotocol

Alle acties op het action_points register vereisen expliciete gebruikersgoedkeuring:

1. Extract: per kandidaat-punt voorstel tonen en om goedkeuring vragen
2. Clear: kandidaten tonen en om bevestiging vragen
3. Prioritize: voorgestelde nieuwe prioriteiten tonen en per punt bevestigen
4. Update-status: oude en nieuwe status tonen en bevestigen

Default gedrag zonder respons: `skip` (niets uitvoeren).

---

## Implementatie

- Canonieke implementatie: `core/methods/action_points.py`
- Data-schema: `core/configuration/action_points_schema.yaml`
- Databron: `overlay/action_points/action_points.json` — canonical, schema-conform, versied via git
- Leesbare weergave: `overlay/action_points/action_points.md` — automatisch gegenereerd na elke schrijfactie, nooit handmatig bewerken
- Geen directe wijziging van overlay-bronnen door de methode
