---
id: 222
title: "PROV-O: The PROV Ontology"
authors: "Timothy Lebo, Satya Sahoo, Deborah McGuinness (editors); W3C Provenance Working Group"
year: 2013
venue: "W3C Recommendation, 30 April 2013 (part of the W3C PROV family with PROV-DM and PROV-N)"
link: https://www.w3.org/TR/prov-o/
code: "Namespace http://www.w3.org/ns/prov# ; no reference implementation in the document (libraries such as the Python 'prov' package exist but were not checked here)"
category: data-infrastructure
era: historical
tags: [provenance, w3c-prov, ontology, owl2, rdf, audit-trail, entity-activity-agent, receipts, reproducibility]
verified: "2026-10-09 via WebFetch of https://www.w3.org/TR/prov-o/ (title, Recommendation status and date, editors, starting-point classes and properties, qualified terms, bundles, companion documents, scope exclusions)"
takeaway: "A standard vocabulary (Entity, Activity, Agent, used, wasGeneratedBy, wasDerivedFrom, wasAssociatedWith) for saying what produced what, from which inputs, by whom and when; SatClip's receipt should be a PROV document so any answer can be traced to scenes, code version and calibration set with off-the-shelf tools"
---

# W3C 2013, PROV-O

## Problem
Data on the web and in pipelines is reused without a record of where it came from, how it was transformed and who is responsible. Ad hoc logs cannot be exchanged or queried across systems.

## Approach
- Expresses the PROV Data Model (PROV-DM) in OWL2 so provenance can be written as RDF and exchanged.
- Starting-point classes: Entity (a thing with fixed aspects, such as a file or a value), Activity (something that happens over time and uses or generates entities), Agent (a person, organisation or software bearing responsibility).
- Starting-point properties: used, wasGeneratedBy, wasDerivedFrom, wasInformedBy, wasAttributedTo, wasAssociatedWith, actedOnBehalfOf, startedAtTime, endedAtTime.
- Expanded terms add Plan, SoftwareAgent, Collection, revision and primary-source links, generatedAtTime and invalidatedAtTime.
- A qualification pattern lets any relation carry extra detail (for example, the role a scene played in a run); Bundles let provenance itself have provenance.
- Companion documents cover PROV-DM, the human-readable PROV-N notation, constraints, XML serialisation, access and query, and a primer.

## Data and benchmarks
- A specification, not an empirical paper; no benchmarks. The document includes worked examples (informative only).

## Key results
- Stable W3C Recommendation since 2013 with a fixed namespace, which makes it a safe long-lived target for audit records.
- Mostly within the OWL-RL profile (five axioms outside), so standard reasoners and SPARQL can query provenance graphs.

## Limitations
- Location vocabulary is out of scope; geometry and region masks need another vocabulary (for example GeoSPARQL or STAC fields).
- Says nothing about how to make a run re-executable; it records lineage, not the environment.
- Encoding bundles in RDF is left open.
- Verbose if used naively; a minimal profile is needed for small receipts.

## What it means for SatClip
- Adopt: model each answer as a PROV graph: the answer number and mask are Entities wasGeneratedBy an analysis Activity that used specific Sentinel-1/2 scene Entities (by STAC item ID, entry 050), a model weights Entity (hash) and a calibration-set Entity (ID, alpha), wasAssociatedWith SatClip as a SoftwareAgent actedOnBehalfOf the requesting office.
- Adopt: serialise the receipt as compact PROV-JSON or JSON-LD alongside the human-readable card, and embed the openEO process graph (entry 121) or pipeline config as the Plan, so a third party can both trace and re-run.
- Adopt: use wasRevisionOf when an answer is recomputed after new scenes arrive, so fact-checkers see that an earlier card was superseded and why.
- Avoid: do not put region geometry into PROV terms; reference a GeoJSON mask Entity by hash.
