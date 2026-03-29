---
title: Transfer Context — Generiek UX Kennissysteem
type: Project Configuration
version: 2.0
language: nl
description: Overdraagbare interpretatie- en gebruikscontext voor generiek UX-kennissysteem
---

# Transfer Context — Generiek UX Kennissysteem

## Doel
Overdraagbare, generieke context voor het correct begrijpen en toepassen van dit UX-kennissysteem in nieuwe projecten.

---

## Rol van dit bestand

Dit bestand definieert hoe het systeem als geheel begrepen en gebruikt moet worden.

Het:
- fungeert als overdraagbare instaplaag
- borgt consistente interpretatie van alle bronnen
- voorkomt dat het systeem wordt gezien als losse documenten
- maakt hergebruik en opschaling mogelijk zonder kennisverlies

---

## Positie in het systeem

Interpretatievolgorde:

1. purpose → waarom het systeem bestaat  
2. instructions → hoe AI zich gedraagt  
3. taxonomy → hoe bestanden worden geïnterpreteerd  
4. knowledge-ontology → hoe kennistypen samenhangen en circuleren  
5. transfer context → hoe het systeem als geheel moet worden begrepen en toegepast  

Daarna volgen:
- core structuur en contract
- methodes
- overlay (projectspecifieke invulling)

---

## Kernidee

- Geen losse docs → systeem  
- Markdown = bronlaag  
- AI = interpreteerder  
- Relaties tussen bestanden zijn cruciaal  

Het systeem ontstaat niet uit individuele bestanden, maar uit de samenhang ertussen.

---

## Bestandstypen

Gebruik de taxonomy om bestanden te classificeren en interpreteren:

- Configuration → stuurt gedrag  
- Doctrine → principes  
- Architecture → structuur  
- Analysis → inzichten  
- Methods → workflows  

Configuratiebestanden hebben altijd prioriteit bij interpretatie.

---

## Functionele rol

Transfer context:

- vertaalt de core naar een begrijpbaar systeemmodel  
- definieert hoe verschillende bronnen gecombineerd moeten worden  
- voorkomt verkeerde interpretatie van losse bestanden  
- zorgt dat nieuwe projecten direct correct starten  

Zonder dit bestand:
- wordt het systeem geïnterpreteerd als losse markdownbestanden  
- ontstaat inconsistente toepassing  
- neemt afhankelijkheid van impliciete kennis toe  

---

## Belangrijke regels

- Single source of truth: gebruik altijd bronbestanden  
- Frontmatter is verplicht voor classificatie en interpretatie  
- Combineer altijd meerdere bronnen voor analyse  
- `i:` = methode-aanroep en volgt gedefinieerde methodes  

---

## Relatie met methodes

- Methodes opereren altijd binnen dit systeemmodel  
- Transfer context bepaalt hoe input uit meerdere bronnen gecombineerd wordt  
- Methodes zonder deze context leiden tot inconsistente of onjuiste uitkomsten  

---

## Core vs Overlay

Dit bestand behoort tot de core.

### Core
- definieert structuur, gedrag en interpretatie  
- is generiek en herbruikbaar  
- wordt centraal beheerd  

### Overlay
- bevat projectspecifieke invulling  
- bouwt voort op de core  
- mag de core niet overschrijven  

### Regels

- Dit bestand wordt niet projectspecifiek aangepast  
- Wijzigingen gebeuren alleen via core-updates  
- Overlay mag geen wijzigingen aanbrengen in dit bestand  
- Overlay mag alleen aanvullingen doen in eigen bestanden  

---

## Governance

- Bescherm kritieke configuratiebestanden  
- Wijzigingen alleen expliciet en gecontroleerd  
- Geef altijd volledige bestanden terug bij updates  

---

## Boilerplate principe

- Core (generiek, stabiel, herbruikbaar)  
- Overlay (flexibel, projectspecifiek)  

Ontwerp het systeem zodanig dat:
- upgrades in de core doorwerken naar overlays  
- overlays uitbreiden zonder de core te breken  

---

## Doel van het systeem

Een onderhoudbaar, versioneerbaar UX-kennissysteem dat:

- herbruikbaar is over projecten heen  
- consistent geïnterpreteerd wordt door AI  
- schaalbaar is in structuur en gebruik  
- geschikt is voor iteratieve verbetering  