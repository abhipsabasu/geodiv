#!/bin/bash

list_of_nouns=(backyard bag car chair dog house storefront stove)
for noun in "${list_of_nouns[@]}"; do
    mv ../flash/sd35/${noun}/affluence-prompt-dist-final.csv affluence_${noun}_sdv3.5.csv
done
mv "../flash/sd35/cooking pot/affluence-prompt-dist-final.csv" "affluence_cooking pot_sdv3.5.csv"
mv "../flash/sd35/plate of food/affluence-prompt-dist-final.csv" "affluence_plate of food_sdv3.5.csv"