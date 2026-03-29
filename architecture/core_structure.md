---
title: Core Structure — Generiek UX Kennissysteem
type: Architecture
version: 1.0
language: nl
description: Structurele opbouw van de generieke core en relatie tussen core, methodes en overlay
---

# Core Structure — Generiek UX Kennissysteem

## Doel

Dit bestand definieert de structurele opbouw van de generieke core.

Het doel is:

- de minimale kernstructuur expliciet maken
- relaties tussen kernbestanden vastleggen
- hergebruik en upgrades ondersteunen
- overlays voorspelbaar laten aansluiten op de core

---

## Positie in het systeem

Dit bestand wordt gelezen na:

- purpose
- instructions
- taxonomy
- transfer context

Dit bestand werkt samen met:

- core_contract
- method_registry

Dit bestand structureert de overgang naar:

- overlay

---

## Ontwerpprincipes

De core-structuur volgt deze principes:

- systeem boven losse bestanden
- minimale maar volledige kernset
- configuratie stuurt interpretatie
- structuur moet overdraagbaar en versioneerbaar zijn
- overlay bouwt voort op core, niet andersom

---

## Kernlagen

De core bestaat uit drie structurele lagen:

### 1. Configuration layer

Deze laag definieert betekenis, gedrag en interpretatie.

Bestanden:

- purpose
- instructions
- taxonomy
- transfer_context

Functie:

- bepaalt waarom het systeem bestaat
- bepaalt hoe AI zich gedraagt
- bepaalt hoe bestanden worden geïnterpreteerd
- bepaalt hoe het systeem als geheel begrepen moet worden

---

### 2. Governance and structure layer

Deze laag borgt structuur, grenzen en uitbreidbaarheid.

Bestanden:

- core_structure
- core_contract

Functie:

- definieert de opbouw van de core
- legt grenzen tussen core en overlay vast
- beschermt de integriteit van het systeem
- maakt upgrades beheersbaar

---

### 3. Method layer

Deze laag definieert toegestane acties binnen het systeem.

Bestanden:

- method_registry
- optionele afzonderlijke methodebestanden

Functie:

- bepaalt welke methodes geldig zijn
- borgt voorspelbaar AI-gedrag
- maakt herbruikbare workflows mogelijk

---

## Minimale verplichte core-bestanden

Een geldige generieke core bevat minimaal:

- purpose.md
- instructions.md
- taxonomy.md
- transfer_context.md
- core_structure.md
- core_contract.md
- method_registry.md

Zonder deze set is de core incompleet.

---

## Optionele core-bestanden

De core mag worden uitgebreid met aanvullende generieke bestanden, zolang zij de kernstructuur niet ondermijnen.

Voorbeelden van toegestane uitbreidingen:

- aanvullende methodebestanden
- governance-bestanden
- patroonbibliotheken
- architectuurtoelichtingen
- generieke templates

Voorwaarde:

- ze blijven generiek
- ze overschrijven geen bestaande core-logica
- ze passen binnen taxonomy en core_contract

---

## Relaties tussen kernbestanden

### purpose
Bepaalt waarom het systeem bestaat.

### instructions
Bepaalt hoe AI met het systeem omgaat.

### taxonomy
Bepaalt hoe bestanden worden geclassificeerd en gewogen.

### transfer_context
Bepaalt hoe het systeem als geheel begrepen en overgedragen wordt.

### core_structure
Bepaalt welke kernbestanden en lagen het systeem bevat.

### core_contract
Bepaalt welke grenzen gelden tussen core en overlay.

### method_registry
Bepaalt welke methodes geldig zijn binnen het systeem.

---

## Interpretatievolgorde

De interpretatievolgorde van de core is:

1. purpose
2. instructions
3. taxonomy
4. transfer_context
5. core_structure
6. core_contract
7. method_registry

Daarna volgt pas de overlay.

Deze volgorde is leidend voor correcte systeeminterpretatie.

---

## Overlay-aansluiting

De overlay sluit altijd aan ná de core.

De overlay:

- gebruikt de definities van de core
- voegt projectspecifieke inhoud toe
- respecteert de grenzen uit core_contract
- gebruikt alleen geldige methodes uit method_registry

De overlay bevat geen alternatieve kernstructuur.

---

## Structuurregels

### Bestandsniveau

- Elk kernbestand heeft een duidelijke, enkelvoudige rol
- Kritieke kernbestanden mogen niet dubbel voorkomen
- Bestandsnamen blijven stabiel waar mogelijk

### Systeemniveau

- Structuur heeft voorrang op ad-hoc uitbreiding
- Nieuwe kernonderdelen worden expliciet toegevoegd
- Relaties tussen lagen moeten duidelijk blijven

### Uitbreidingsniveau

- Uitbreiding gebeurt via nieuwe bestanden of nieuwe methodes
- Niet via impliciete uitzonderingen
- Niet via overlay-logica die de core vervangt

---

## Aanbevolen directory-logica

De core hoeft niet aan één vaste mapstructuur gebonden te zijn, maar de volgende logica wordt aanbevolen:

- configuration/
- architecture/
- methods/
- overlay/

Doel van deze logica:

- snelle herkenbaarheid
- scheiding tussen kernlagen
- betere overdraagbaarheid naar nieuwe projecten

Bestandsplaatsing is ondergeschikt aan systeembetekenis: classificatie en rol zijn belangrijker dan mapnaam.

---

## Stabiliteitsregels

De volgende onderdelen moeten zo stabiel mogelijk blijven:

- purpose
- instructions
- taxonomy
- transfer_context
- core_structure
- core_contract
- method_registry

Wijzigingen aan deze onderdelen:

- gebeuren expliciet
- zijn versioneerbaar
- worden als core-update behandeld

---

## Upgrade-principe

De structuur van de core moet zodanig ontworpen zijn dat:

- nieuwe core-versies overlays niet onnodig breken
- uitbreidingen centraal kunnen worden toegevoegd
- overlays kunnen meebewegen zonder herontwerp van de basis

Structurele wijzigingen aan de core moeten daarom:

- terughoudend zijn
- duidelijk gedocumenteerd zijn
- compatibiliteit zoveel mogelijk bewaren

---

## Validatiecriteria

Een structuur is geldig als:

- alle verplichte kernbestanden aanwezig zijn
- de interpretatievolgorde intact is
- core en overlay gescheiden blijven
- methodes via method_registry worden bestuurd
- nieuwe uitbreidingen expliciet zijn gedefinieerd

---

## Doel van deze structuur

Zorgen dat het UX-kennissysteem:

- overdraagbaar is
- begrijpelijk blijft als samenhangend systeem
- stabiel kan groeien
- veilig herbruikbaar is
- upgradebaar blijft over meerdere projecten heen

---