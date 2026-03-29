---
title: Core Contract — Generiek UX Kennissysteem
type: Project Configuration
version: 1.2
language: nl
description: Contract tussen core en overlay voor structuur, gedrag en upgradebaarheid
---

# Core Contract — Generiek UX Kennissysteem

## Doel

Dit contract definieert de regels en grenzen tussen:

- de core (generieke boilerplate)
- de overlay (projectspecifieke invulling)

Het doel is:

- consistent gedrag van het systeem  
- veilige herbruikbaarheid  
- upgradebaarheid zonder breuk  

---

## Positie in het systeem

Dit bestand wordt geïnterpreteerd na:

- purpose  
- instructions  
- taxonomy  
- knowledge-ontology  
- transfer context  

En vóór:

- method_registry  
- overlay  

---

## Definitie

### Core

De core bevat:

- systeemdefinitie  
- interpretatieregels  
- structuur  
- methodes  

Eigenschappen:

- generiek  
- herbruikbaar  
- versiegestuurd  
- centraal beheerd  

---

### Overlay

De overlay bevat:

- projectspecifieke content  
- UX-uitwerkingen  
- analyses  
- flows  
- velddefinities  

Eigenschappen:

- contextafhankelijk  
- uitbreidbaar  
- vervangbaar per project  

---

## Hoofdregel

**Overlay mag de core niet wijzigen, alleen gebruiken en uitbreiden.**

---

## Toegestane acties (overlay)

Overlay mag:

- nieuwe bestanden toevoegen  
- bestaande structuren gebruiken  
- analyses uitvoeren op basis van core  
- methodes toepassen  
- eigen documentatie en definities toevoegen  

---

## Verboden acties (overlay)

Overlay mag NIET:

- core-bestanden aanpassen  
- interpretatieregels overschrijven  
- taxonomy wijzigen  
- methodes veranderen of redefiniëren  
- systeemgedrag beïnvloeden via alternatieve logica  

---

## Core integriteit

De volgende bestanden zijn beschermd:

- purpose  
- instructions  
- taxonomy  
- knowledge-ontology  
- transfer_context  
- core_structure  
- core_contract  
- method_registry  

Wijzigingen aan deze bestanden:

- gebeuren alleen in de core  
- zijn versioned  
- worden expliciet doorgevoerd  

---

## Uitbreidingsmodel

Nieuwe functionaliteit wordt toegevoegd via:

- nieuwe methodes (method_registry)  
- uitbreiding van taxonomy  
- uitbreiding van knowledge-ontology  
- uitbreiding van core_structure  

Niet via:

- impliciete interpretaties  
- overlay-specifieke logica die coregedrag beïnvloedt  

---

## Upgrade model

### Core updates

Bij een nieuwe core-versie:

- blijft overlay intact  
- worden verbeteringen automatisch overgenomen  
- worden breaking changes expliciet gemaakt  

---

### Compatibiliteit

Core-updates moeten:

- backward compatible zijn waar mogelijk  
- breaking changes expliciet maken  
- migratierichtlijnen bevatten  

---

### Verantwoordelijkheid overlay

Overlay moet:

- core-regels respecteren  
- geen afhankelijkheden creëren die upgrades blokkeren  
- compatibel blijven met nieuwe core-versies  

---

## Methodes

- Alleen methodes uit method_registry zijn toegestaan  
- `i:`-aanroepen buiten de registry zijn ongeldig  
- Methodes opereren altijd binnen core-definitie  

---

## Interpretatieregels

- Configuration-bestanden hebben prioriteit  
- Bronnen worden altijd gecombineerd geïnterpreteerd  
- Instructions bepalen gedrag  

---

## Conflictregels

Bij conflicten:

- core wint van overlay  
- configuration wint van andere bestandstypen  
- instructions winnen bij gedragsconflicten  

---

## Governance

Wijzigingen aan de core:

- worden expliciet voorgesteld  
- worden niet stilzwijgend doorgevoerd  
- leveren altijd volledige bestanden op  

---

## Doel van dit contract

Zorgen dat:

- het systeem consistent blijft werken  
- projecten schaalbaar blijven  
- upgrades veilig kunnen plaatsvinden  
- AI voorspelbaar gedrag vertoont  

---