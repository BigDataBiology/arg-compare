# Using git-annex

You need access to `aws.big-data-biology.org` (for the moment)

Make sure that `git-annex` is installed and run

```bash
git-annex init
git-annex enableremote aws-data type=rsync rsyncurl=aws.big-data-biology.org:/share/work/arg-compare-data encryption=none
```

Now, you can retrieve individual `git-annex`-managed files using `git-annex get`. For example:

```bash
git-annex get GMGCv1-reads-mode/computed/deepARG-read-mode.mapping.ARG.xz
```

