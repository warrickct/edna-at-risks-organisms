# eDNA At-risk Organism Finder

## How it works

    * Reads the input csv file within the root folder.

    * Segments each csv line into individual terms.

    * Removes terms that will yield broad results.

    * uses the eDNA term query REST API to retrieve all abundance entries within the eDNA database.

    * When there are organism abundances present, write the abundance values corresponding to a site, organism, searched term and original csv input.