#!/usr/bin/env python3
"""
Script to create 5x5 grid images from individual images in images_sub folder.
Each grid combines 25 images for a specific model-entity-country combination.
"""

import os
from PIL import Image
import json

# Base paths
IMAGES_SUB_DIR = "../images_sub"
OUTPUT_DIR = "grid_images"
MAPPING_FILE = "image_mapping.json"

# Models, entities, and countries
models = ['SDv2.1', 'SDv3m', 'SDv3.5', 'FLUX.1-Dev']
entities = ['backyard', 'bag', 'car', 'chair', 'cooking pot', 'dog', 'house', 'plate of food', 'storefront', 'stove']
countries = [
    'United States of America', 'Mexico', 'Colombia', 'United Kingdom', 
    'Italy', 'Spain', 'Japan', 'South Korea', 'Indonesia', 'China', 
    'India', 'United Arab Emirates', 'Turkey', 'Philippines', 'Egypt', 'Nigeria'
]

def create_grid_image(image_paths, output_path, grid_size=5, cell_size=256):
    """
    Create a grid image from a list of image paths.
    
    Args:
        image_paths: List of paths to individual images
        output_path: Path to save the grid image
        grid_size: Size of the grid (5x5)
        cell_size: Size of each cell in the grid
    """
    # Create a new image for the grid
    grid_width = grid_size * cell_size
    grid_height = grid_size * cell_size
    grid_image = Image.new('RGB', (grid_width, grid_height), color='white')
    
    # Load and paste images into grid
    for idx, img_path in enumerate(image_paths):
        if not os.path.exists(img_path):
            print(f"Warning: Image not found: {img_path}")
            continue
            
        try:
            # Calculate grid position
            row = idx // grid_size
            col = idx % grid_size
            
            # Load and resize image
            img = Image.open(img_path)
            img = img.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
            
            # Paste into grid
            x = col * cell_size
            y = row * cell_size
            grid_image.paste(img, (x, y))
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            continue
    
    # Save the grid image
    grid_image.save(output_path, 'PNG', quality=95)
    print(f"Created grid: {output_path}")

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load image mapping
    if not os.path.exists(MAPPING_FILE):
        print(f"Error: {MAPPING_FILE} not found!")
        return
    
    with open(MAPPING_FILE, 'r') as f:
        image_mapping = json.load(f)
    
    total_combinations = 0
    created = 0
    
    # Iterate through all combinations
    for model in models:
        if model not in image_mapping:
            continue
            
        for entity in entities:
            if entity not in image_mapping[model]:
                continue
                
            for country in countries:
                if country not in image_mapping[model][entity]:
                    continue
                
                total_combinations += 1
                
                # Get image filenames
                image_files = image_mapping[model][entity][country]
                if len(image_files) < 25:
                    print(f"Skipping {model}/{entity}/{country}: Only {len(image_files)} images")
                    continue
                
                # Take first 25 images
                image_files = image_files[:25]
                
                # Construct paths
                base_path = os.path.join(IMAGES_SUB_DIR, model, entity, country)
                image_paths = [os.path.join(base_path, f"{f}.png") for f in image_files]
                
                # Create output filename (sanitize for filesystem)
                safe_entity = entity.replace(' ', '_')
                safe_country = country.replace(' ', '_')
                output_filename = f"{model}_{safe_entity}_{safe_country}.png"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                
                # Create grid image
                create_grid_image(image_paths, output_path)
                created += 1
    
    print(f"\nCompleted! Created {created} grid images out of {total_combinations} combinations.")

if __name__ == "__main__":
    main()
