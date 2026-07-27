# Pan-Species Immunological Response Tool

CLICK THIS LINK TO USE THE APP: https://pan-species-immunological-response-tool-mqpi484b7khep6deydiava.streamlit.app/

**The goal of this project**  
Animals handle infections from viruses or bacteria differently. I built this tool to take genetic data from humans and animals, match up the genes they share, and see if their cells fight back diseases the exact same way (conserved) or differently (divergent).

## How to read the graph:
* 🔴 **Human-Specific Hyperactivation:** The human body has a severe hyper-reactive response that may cause harm to the human cells rather than the pathogen.
* 🟢 **Conserved Immunity:** Both humans and the animals activate this gene equally to fight off the infection.
* 🔵 **Animal-Specific Protection:** The animal host activates defensive genes that protect it from getting sick, making it more tolerant to diseases.

## How to interact with it:
Use the sliders in the left sidebar to change how filtered the data is.

## Data Filters
* **Data Credibility (p-value):** This measures data credibility. Slide left to only look at guaranteed data points. Slide right to see a broader view.
* **Gene Activation Level (Log2 Fold Change):** This measures how intensely a gene woke up and started fighting after infection. Higher values only show massive cellular reactions.
* **Response Variance Margin (Divergence Delta):** The mathematical gap between species. Gene responses that exceed this setting are categorized as divergent.

## Vocabulary
### Biology Concepts:
* **Gene Symbol:** The unique code name assigned to a specific gene.
* **Conserved Immunity:** When humans and animals activate the exact same genes at the same intensity to fight off pathogens.
* **Divergent Immunity:** When humans and animals react to a pathogen very differently.

### Data & Control Settings:
* **Data Credibility (p-value):** The probability that a gene change was a random accident, where lower values mean more reliable data.
* **Gene Activation Level (Log2FC):** The baseline score showing how much a gene woke up and changed its behavior after infection.
* **Response Variance Margin (Divergence Delta):** The targeted mathematical gap size used to decide if the species reacted differently.

## Cited sources for this project:
NCBI GEO (Gene Expression Omnibus), Ensembl BioMart

---
*Pan-Species Immunological Response Tool | Independent Project*
