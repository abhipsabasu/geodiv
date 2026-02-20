#!/usr/bin/env python3
"""
Script to generate image_mapping.json by scanning the images_sub folder structure.
"""

import os
import json

# Base paths
IMAGES_SUB_DIR = "../images_sub"
MAPPING_FILE = "image_mapping.json"

# Models, entities, and countries
models = ['SDv2.1', 'SDv3m', 'SDv3.5', 'FLUX.1-Dev']
entities = ['backyard', 'bag', 'car', 'chair', 'cooking pot', 'dog', 'house', 'plate of food', 'storefront', 'stove']
countries = [
    'United States of America', 'Mexico', 'Colombia', 'United Kingdom', 
    'Italy', 'Spain', 'Japan', 'South Korea', 'Indonesia', 'China', 
    'India', 'United Arab Emirates', 'Turkey', 'Philippines', 'Egypt', 'Nigeria'
]

def main():
    mapping = {}
    
    # Iterate through all combinations
    for model in models:
        if model not in mapping:
            mapping[model] = {}
        model_path = os.path.join(IMAGES_SUB_DIR, model)
        
        if not os.path.exists(model_path):
            print(f"Model path not found: {model_path}")
            continue
            
        for entity in entities:
            if entity not in mapping[model]:
                mapping[model][entity] = {}
            entity_path = os.path.join(model_path, entity)
            
            if not os.path.exists(entity_path):
                print(f"Entity path not found: {entity_path}")
                continue
                
            for country in countries:
                country_path = os.path.join(entity_path, country)
                
                if os.path.exists(country_path):
                    # Get all PNG files
                    files = [f.replace('.png', '') for f in os.listdir(country_path) if f.endswith('.png')]
                    files = sorted(files, key=lambda x: int(x) if x.isdigit() else float('inf'))
                    
                    if files:
                        # Take first 25
                        mapping[model][entity][country] = files[:25]
                        print(f"Found {len(files)} images for {model}/{entity}/{country}, using first 25")
    
    # Save mapping to JSON file
    with open(MAPPING_FILE, 'w') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"\nMapping saved to {MAPPING_FILE}")

if __name__ == "__main__":
    main()
