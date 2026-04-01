---
title: Method Registry — Generiek UX Kennissysteem
type: Methods
version: 2.2
language: nl
description: Overzicht van toegestane methodes met taxonomy-aware gedrag
---

# Method Registry — Generiek UX Kennissysteem

## Doel

Dit bestand definieert alle toegestane methodes die gebruikt mogen worden via:

i: methodenaam

Het zorgt voor:

- gecontroleerd AI-gedrag  
- consistente output  
- herbruikbare workflows  
- semantisch correcte interpretatie van bronnen  

---

## Gebruik

Een methode wordt aangeroepen via:

i: methodenaam

Regels:

- Alleen methodes in deze registry zijn geldig  
- Bestaat een methode niet → niet uitvoeren  
- Output volgt altijd de gedefinieerde structuur  

---

## Methode structuur

Elke methode bevat:

- naam  
- doel  
- input (optioneel)  
- output (vorm + regels)  
- interpretatieregels  

---

# Taxonomy-aware gedrag

Methodes interpreteren bronnen op basis van type en subtype.

## Gewicht per hoofdcategorie

1. Project Configuration → leidend  
2. Methods → stuurt verwerking  
3. Architecture → bepaalt structuur  
4. Design Documentation → concrete uitwerking  
5. UX Analysis → inzichten en onderbouwing  

## Interpretatie per categorie

### Project Configuration
- bepaalt gedrag en regels  
- overschrijft andere interpretaties  

### Methods
- bepaalt hoe informatie wordt verwerkt  
- stuurt outputvorm  

### Architecture
- bepaalt structuur en relaties  
- is leidend boven design  

### Design Documentation
- beschrijft concrete oplossingen  
- heeft hoge specificiteit  

### UX Analysis
- bevat inzichten, geen harde feiten  
- moet gecombineerd worden met andere bronnen  

---

# Beschikbare methodes

---

## recap

Naam: recap  
Doel: snelle context reset  

Output:
- korte bullets  
- geen lange tekst  

Interpretatie:
- geen diepe analyse  
- alleen samenvatten  

Bron: method-recap.md  [oai_citation:0‡method-recap.md](method-recap.md)  

---

## analyse

Naam: analyse  
Doel: inhoud analyseren op basis van meerdere bronnen  

Input:
- vraag of onderwerp  

Output:
- gestructureerde analyse  
- combineert meerdere bronnen  
- expliciteert aannames  

Interpretatieregels:

- gebruikt altijd meerdere bronnen  
- herkent type en subtype  
- weegt bronnen volgens taxonomy  [oai_citation:1‡taxonomy.md](../configuration/taxonomy.md)  

Gedrag:

- UX Analysis → inzichten, niet absoluut  
- Design Documentation → concrete oplossingen  
- Architecture → structuurleidend  
- Configuration → bepaalt grenzen  

---

## structure

Naam: structure  
Doel: structureren van content of systeem  

Input:
- ongestructureerde of bestaande content  

Output:
- hiërarchische structuur  
- logisch gegroepeerd  

Interpretatieregels:

- groepeert op basis van taxonomy  
- scheidt analyse, design en architectuur  
- bewaakt consistentie tussen lagen  

---

## generate

Naam: generate  
Doel: genereren van nieuwe content  

Input:
- opdracht of type output  

Output:
- consistente content  
- afgestemd op bestaande structuur  

Interpretatieregels:

- volgt taxonomy voor type output  
- respecteert bestaande structuur  
- introduceert geen nieuwe logica buiten core  

---

## validate

Naam: validate  
Doel: controleren of iets voldoet aan de core  

Input:
- bestand of structuur  

Output:
- voldoet / voldoet niet  
- afwijkingen  
- verbeterpunten  

Interpretatieregels:

- controleert type en subtype consistentie  
- accepteert `type` als hoofdcategorie of als gedefinieerd subtype uit taxonomy  
- gebruikt foldercontext als aanvullende classificatiehint bij twijfel  
- detecteert mismatch tussen inhoud en classificatie  
- controleert relatie met core  

Extra checks:

- ontbrekende categorieën (bijv. design zonder analyse)  
- conflicten met core_contract  [oai_citation:2‡core_contract.md](../governance/core_contract.md)  
- periodieke overlay-check: valideer bij nieuwe bestanden, bij typewijzigingen en vóór afronding van grotere updates  

---

## transform

Naam: transform  
Doel: omzetten van content naar andere vorm  

Input:
- broncontent  
- gewenste vorm  

Output:
- inhoud blijft gelijk  
- vorm verandert  

Interpretatieregels:

- behoudt oorspronkelijke betekenis  
- past vorm aan naar taxonomy  

---

## mkdocs_export

Naam: mkdocs_export  
Doel: exporteren van kennisdocumentatie als MkDocs-site in een downloadbare zip  

Input (optioneel):

- scope: `all` | `overlay` | `core` (default: `all`)
- include/exclude patterns

Output:

- 1 zip-bestand in `export/`
- bevat `mkdocs.yml` + `docs/` structuur

Interpretatieregels:

- schrijft niets buiten `export/`
- kopieert/structureert, wijzigt geen broncontent
- respecteert taxonomy en scope bij selectie en navigatie

Bron: method-mkdocs-export.md  

---

## extend

Naam: extend  
Doel: uitbreiden van bestaande structuur  

Input:
- bestaande structuur  
- uitbreidingsvraag  

Output:
- consistente uitbreiding  

Interpretatieregels:

- sluit aan op bestaande taxonomy  
- respecteert core-structuur  [oai_citation:3‡core_structure.md](../architecture/core_structure.md)  

---

## explain

Naam: explain  
Doel: uitleggen van onderdelen van het systeem  

Input:
- vraag of onderdeel  

Output:
- heldere uitleg  
- inclusief systeemcontext  

Interpretatieregels:

- gebruikt transfer context voor samenhang  [oai_citation:4‡transfer_context_ux_system.md](../configuration/transfer_context_ux_system.md)  
- vermijdt losse uitleg zonder systeemcontext  

---

## compare

Naam: compare  
Doel: vergelijken van opties of structuren  

Input:
- meerdere varianten  

Output:
- verschillen  
- overeenkomsten  
- implicaties  

Interpretatieregels:

- vergelijkt binnen dezelfde categorie  
- maakt verschillen expliciet op basis van type  

---

# Methoderegels

## Validatie

- Methoden mogen alleen worden uitgevoerd als ze in deze registry staan  
- Onbekende methode → expliciet melden  

---

## Consistentie

Methoden volgen altijd:

- purpose  [oai_citation:5‡purpose.md](../configuration/purpose.md)  
- instructions  [oai_citation:6‡instructions.md](../configuration/instructions.md)  
- taxonomy  [oai_citation:7‡taxonomy.md](../configuration/taxonomy.md)  
- transfer context  [oai_citation:8‡transfer_context_ux_system.md](../configuration/transfer_context_ux_system.md)  
- core_contract  [oai_citation:9‡core_contract.md](../governance/core_contract.md)  

---

## Grenzen

- Methoden mogen de core niet wijzigen  
- Methoden respecteren core-contract  
- Methoden opereren binnen systeemdefinitie  

---

## Uitbreiding

Nieuwe methodes:

- worden toegevoegd aan deze registry  
- volgen dezelfde structuur  
- zijn taxonomy-aware  

---

## Doel van de registry

Zorgen dat:

- AI-interacties voorspelbaar zijn  
- workflows herbruikbaar zijn  
- interpretatie semantisch correct is  
- systeem consistent blijft werken  

---
