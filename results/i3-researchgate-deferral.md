# I3 deferral: ResearchGate DOI

Date: 2026-10-16. Owner: the author, by proceeding on the integrity residual.

## What the scan found

`results/integrity_audit.json` reports I3 fail. Eight DOIs resolved through Crossref. One did not:

`10.13140/RG.2.2.30911.01443`

That is the DOI of Bilar (2024), Notes on Google Willow. ResearchGate DOIs are often absent from Crossref. The miss is a resolver gap. It is not evidence that the 2024 note was invented. The scan JSON is left as the scanner wrote it.

## What is deferred

Keep the DOI in the draft header and in reference [1]. The reader path is the ResearchGate page already linked there:

https://www.researchgate.net/publication/387576664_Notes_on_Google_Willow_2024_aka_Quantum_Error_Correction_Below_the_Surface_Code_Threshold

Do not replace the DOI with a made-up Crossref identifier.

## Grandfathered, 2026-10-19

The author made an exception. This 2024 publication is grandfathered. The DOI stays in reference [13]. The scan records WARN `grandfathered` from `i3_grandfathered` in `integrity-manifest.json`. That warning is not a blocking fail. The 2026-10-16 line that said not to mark I3 pass is superseded for this identifier only.

The same day's rescan found the DOI in DataCite, not Crossref. The record is findable, client `rg.rg`, issued 2024, title matching the 2024 note. The creator string there is "Daniel Yaacob Bilar," which is not the house byline. The reader path stays the ResearchGate URL. The note is still not scientifically verified.

## What this does not close

I1 stays limited: eight cited percents have no local results file. That is `i1_policy: advise` in `integrity-manifest.json`.

The note is evidence-ready under the paper runbook: the integrity failure is named and deferred. It is not scientifically verified. The Section V removal experiment is still unrun, and only the cultivation team can run it.
