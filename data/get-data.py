from jug.utils import jug_execute

DATAFILES = [
        'http://gmgc.embl.de/downloads/v1.0/subcatalogs/GMGC10.wastewater.95nr.fna.gz',
        ]

for df in DATAFILES:
    jug_execute(['wget', df])
