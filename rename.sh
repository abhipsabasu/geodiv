#!/bin/bash

list_of_nouns=(backyard bag car chair dog house storefront stove)
for noun in "${list_of_nouns[@]}"; do
    mv ../flash/flux1/${noun}/maintenance-prompt-dist-final.csv maintenance_${noun}_flux.1-dev.csv
done
mv "../flash/flux1/cooking pot/maintenance-prompt-dist-final.csv" "maintenance_cooking pot_flux.1-dev.csv"
mv "../flash/flux1/plate of food/maintenance-prompt-dist-final.csv" "maintenance_plate of food_flux.1-dev.csv"