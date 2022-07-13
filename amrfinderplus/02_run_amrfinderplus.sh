#!/bin/bash

DIR="~/data/split"

if [ "$(ls -A $DIR)" ]
then
  for infile in $(ls ${DIR})
    do
	  amrfinder -p ${DIR}/${infile} --threads 64 -o ~/data/result/${infile}.tsv
	done
fi