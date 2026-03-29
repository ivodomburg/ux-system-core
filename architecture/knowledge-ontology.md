---
title: Knowledge Ontology — Generiek UX Kennissysteem
type: Architecture
version: 1.0
language: nl
description: Ontologie van kennistypen, lagen, relaties en circulatie in het UX-kennissysteem
---

# Knowledge Ontology — Generiek UX Kennissysteem

## Doel

Dit document beschrijft de structuur van kennis in het systeem:

- welke kennistypen bestaan
- hoe ze zich tot elkaar verhouden
- hoe kennis stroomt en circuleert
- welke kardinaliteiten gelden
- wat valid onderdeel is van het systeem

Dit vormt de basis voor consistent interpreteren van bronnen en het sturen van methodes.

---

## Positie in het systeem

Interpretatievolgorde:

1. purpose
2. instructions
3. taxonomy (classificatie)
4. **knowledge-ontology** (relaties en circulatie) ← dit bestand
5. transfer_context
6. core_structure
7. core_contract
8. method_registry

---

## Kernidee

Kennis in dit systeem is niet statisch, maar circulerend:

- Normatieve kennis (doctrines) leidt richtinggevend
- Feitelijke kennis (reviews, data) vormt grond
- Interpretatie (analysis) verbindt feiten met principes
- Hypothesen (designs, flows) testen de interpretatie
- Validatie (tests) verfijnt alles
- Voortgang (meetings, planning, goals) houdt het systeem in beweging

---

# Kennislagen

## Laag 1: Normatief (leidend, stabiel)

Bepaalt wat mag en waar naar gestreefd wordt.

Kennistypen:
- **Doctrines** — UX-principes, architectuurvolen, richtlijnen
- **Principles** — Geconsolideerde samenvatting van doctrines

Eigenschappen:
- Gegeven en niet ter discussie
- Leidend voor alle andere lagen
- Stabiel over projecten heen

Dependencies:
- Alles afhankelijk van deze laag

Cardinal iteit:
- 1 doctrine per domein (bijv. "Data Product & Consent Platform")
- 1 principles-samenvatting per context (bijv. consent portal)

---

## Laag 2: Factueel (grond, gegeven)

Objectieve waarnemingen, data, inzichten over wat is.

Kennistypen:
- **Resources** — Externe kennisbronnen (platforms, organisaties, APIs)
- **Personas** — Gebruikerssegmenten en hun karakteristieken
- **Data** — Ruwe onderzoeksgegevens, statistieken
- **Reviews** — Observaties van huidigetoestand, bevindingen

Eigenschappen:
- Vastgesteld, niet speculatief
- Basis voor verdere analyse
- Context voor ontwerp

Dependencies:
- Input voor analysis
- Moeten aligned zijn met doctrines

Kardinaliteit:
- N resources (extern)
- N personas per context
- N datasets
- N reviews per probleem

---

## Laag 3: Interpretatief (synthese, verbinding)

Wat betekenen de feiten als je ze leest met de lens van de principes?

Kennistypen:
- **Analysis** — Synthese van feiten + personas + reviews → kernspanningen, kansen
- **Meetings** — Dialoog en samenhanging: voorbereiding + notes + besluiten

Eigenschappen:
- Verbindt factueel en normatief
- Contextafhankelijk
- Sturing voor volgende lagen

Dependencies:
- Input: doctrines (hoe te interpreteren) + laag 2 (wat interpreteren)
- Output: stuurt designs/flows/requirements

Kardinaliteit:
- N analyses per project
- N meetings per iteratie

---

## Laag 4: Hypothetisch (mogelijke wegen)

"Stel dat we dit doen..." — voorstellen geleidt door analyse.

Kennistypen:
- **Designs** — UI-hypothesen, wireframes, mockups
- **Flows** — Scenario-hypothesen, stap-voor-stap flows
- **Requirements** — Functionele eisen, user stories

Eigenschappen:
- Geleidt door analysis en doctrines
- Testbaar
- Nog niet gevalideerd

Dependencies:
- Input: analysis (wat moet veranderen), doctrines (hoe moet het)
- Input: personas (wie betreft het)

Kardinaliteit:
- N designs per focus area
- N flows per user journey
- N requirements per feature

---

## Laag 5: Validatie (klopt het?)

Testen of hypothesen standhouden in werkelijkheid.

Kennistypen:
- **Tests** — Usability tests, user research, expertenreviews

Eigenschappen:
- Geeft feedback aan hypothetisch
- Kan laag 2/3 aanscherpen

Dependencies:
- Input: designs/flows/requirements om te testen
- Output: naar analysis (inzichten) of terug naar designs (iteratie)

Kardinaliteit:
- N tests per hypothesis

---

## Laag 6: Organisatie & voortgang (hoe bewegen we)

Timing, prioratie, keuzes over volgorde.

Kennistypen:
- **Goals** — Gewenste eindtoestand, success criteria
- **Planning** — Roadmap, sprints, prioriteiten
- **Meetings** — Voorbereiding + notes (ook organisatorisch)

Eigenschappen:
- Bepaalt timing en volgorde
- Feed-forward (waar naartoe) en feed-back (waar waren we)
- Praktisch, niet conceptueel

Dependencies:
- Input: analysis (wel/niet gewenst), tests (wat werkt/niet)
- Output: bepaalt volgende iteratie

Kardinaliteit:
- 1 set goals per project-fase
- N planning-items
- Timing-afhankelijk

---

# Relaties en Kausaliteit

```
Laag 1: Normatief
    │ (leidend)
    ↓
Laag 2: Factueel ← Resources, Personas, Data, Reviews
    │
    ├──────────────────────┐
    │                      │
    ↓                      ↓
Laag 3: Interpretatief → Analysis + Meetings (voorbereiding)
    │
    ├────────── steert ──────────┐
    │                           │
    ↓                           ↓
Laag 4: Hypothetisch → Designs, Flows, Requirements
    │
    ├──────── test ──────┐
    │                   │
    ↓                   ↓
Laag 5: Validatie → Tests
    │
    ├──── feedback ─────┐
    │                  │
    └──→ Laag 3 (nieuwe insights)
    
    
Laag 6: Organisatie ← Goals, Planning, Meetings (voortgang)
    │
    └──→ Timing & volgende ronde
```

---

# Kardinaliteit-Model

| Kennistype | Kardinaliteit | Afhankelijkheden |
|-----------|---------------|-----------------|
| Doctrines | 1 per domein | Geen |
| Principles | 1+ per context | 1:1 met doctrines |
| Resources | N | Gegeven |
| Personas | N per context | 1:1 met doctrines |
| Data | N | Gegeven |
| Reviews | N per vraag | Moet aligned zijn doctrines |
| Analysis | N per iteratie | Doctrines + Laag 2 |
| Designs | N per focus | Analysis + Personas |
| Flows | N per journey | Analysis + Personas |
| Requirements | N per feature | Analysis + Doctrines |
| Tests | N per hypothesis | Designs/Flows/Requirements |
| Goals | 1-3 per fase | Project-scope |
| Planning | N | Goals + Tests |
| Meetings | N per iteratie | Organisatorisch noodzakelijk |

---

# Circulatielogica

Kennis stroomt in een cycle:

1. **Start**: Doctrines bepalen compass
2. **Verzamelen**: Laag 2 data verzamelen
3. **Interpreteren**: Analysis maakt betekenis
4. **Hypotheseren**: Designs/Flows voorstellen alternatieven
5. **Valideren**: Tests geven feedback
6. **Leren**: Meetings consolideren inzichten
7. **Organiseren**: Planning bepaalt volgende ronde
8. **Herhalen**: Terug naar stap 3, geleidt door nieuwe inzichten

Dit is geen lineair waterfall, maar een iteratieve spiral.

---

# Validatieregels

Kennis is valide als:

- **Laag 1** staat: doctrines zijn gegeven en stabiel
- **Laag 2** staat: resources/personas/data/reviews zijn intern consistent
- **Laag 3** staat: analysis volgt logical uit Laag 1 + 2
- **Laag 4** staat: designs/flows passen binnen doctrines en analysis
- **Laag 5** staat: tests valideren Laag 4 tegen realiteit
- **Laag 6** staat: goals/planning zijn haalbaar gegeven vorige lagen

Bij conflict:
- Laag 1 wint van alle lagen
- Laag 2 (feiten) wint van Laag 4-6 (hypothesen)
- Laag 5 (tests) kan alle vorige lagen verfijnen

---

# Implicaties voor methodes

Dit ontologiemodel stuurt methode-gedrag:

- `analyse` volgt dit circulatiemodel: verzamel Laag 2 → interpret via Laag 1
- `generate` produceert kennis in juiste laag
- `validate` controleert op breuk tussen lagen
- `structure` organiseert kennis volgens ontologie

---

# Doel van deze ontologie

Zorgen dat:

- kennis consistent circuleert
- relaties tussen bestanden expliciet zijn
- AI begrijpt prioriteitslogica tussen lagen
- gebruikers zien hoe hun output aansluit
- het systeem schaalbaar blijft
- feedback-loops mogelijk blijven

---
