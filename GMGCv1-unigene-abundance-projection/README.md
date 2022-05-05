# Unigene-based abundance estimates

This needs the big `GMGC10.sample-abundance.tsv.xz` file from GMGCv1

1. Run `to-ngless-tsv.py`. This will produce `GMGC10.AntibioticResistance.tsv`
2. Run `select-abundance.py`. This will filter the big `GMGC10.sample-abundance.tsv.xz` file
3. Run `project.py`. This will produce the downstream results

## Open questions

- How to summarize? Now, unigenes are first filtered by `unique_raw > 0` which
  has been used in previous manuscripts. Not clear that this is the best


