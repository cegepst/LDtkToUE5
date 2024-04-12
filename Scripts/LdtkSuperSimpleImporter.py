import unreal
import math
import json
import pprint
import datetime
import os
import csv
from enum import Enum
from typing import Any, List, Optional, Dict, TypeVar, Type, Callable, cast

from PIL import Image

def find_adjacent_cells(data, x, y, visited=None):
    if visited is None:
        visited = set()
    
    # Base case: if the cell is not 1 or already visited, return an empty list
    if data[y][x] != '1' or (x, y) in visited:
        return []
    
    # Mark the current cell as visited
    visited.add((x, y))
    
    # List to hold the coordinates of the adjacent cells
    adjacent_cells = [(x, y)]
    
    # Directions to check for adjacent cells (up, down, left, right)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # Check if the new coordinates are within the bounds of the data list
        if 0 <= nx < len(data[0]) and 0 <= ny < len(data):
            adjacent_cells.extend(find_adjacent_cells(data, nx, ny, visited))
    
    return adjacent_cells

def add_colliders_from_csv(csv_path, sprite_actor):
    # Open the CSV file
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        # Convert the CSV data into a 2D list
        data = [list(row) for row in reader]
    
    # Iterate through each cell in the CSV data
    for y in range(len(data)):
        for x in range(len(data[y])): # Directly iterate over the cells in the row
            # If the cell's value is 1, find all adjacent cells with a value of 1
            if data[y][x] == '1':
                group = find_adjacent_cells(data, x, y)
                
                # Calculate the size and position of the collider based on the group
                min_x = min(cell[0] for cell in group)
                max_x = max(cell[0] for cell in group)
                min_y = min(cell[1] for cell in group)
                max_y = max(cell[1] for cell in group)
                
                collider_size = unreal.Vector((max_x - min_x + 1) * 16, (max_y - min_y + 1) * 16, 1)
                collider_position = unreal.Vector(min_x * 16, min_y * 16, 0)
                
                # Create a box collider for the group
                collider = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.BoxComponent, collider_position, unreal.Rotator(0, 0, 0))
                
                # Set the size of the collider
                collider.set_editor_property('relative_scale_3d', collider_size)
                
                # Attach the collider to the sprite actor
                collider.attach_to_actor(sprite_actor, '', unreal.AttachmentRule.KEEP_RELATIVE, '')

def convert_transparent_to_black_and_white(image_path, save_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    
    for x in range(img.width):
        for y in range(img.height):
            r, g, b, a = img.getpixel((x, y))
            if a == 0:
                new_img.putpixel((x, y), (0, 0, 0, 255))
            else:
                new_img.putpixel((x, y), (255, 255, 255, 255))
    
    new_img.save(save_path)

def find_all_subfolders(path):
    subfolders = []
    
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            subfolders.append(os.path.join(root, dir))
    
    return subfolders


DirectoryContents = Dict[str, Dict[str, Any]]

def get_directory_contents(path: str) -> dict:
    """
    Returns a nested dictionary where each key is a directory path, and the value is a dictionary
    containing the names of the files in that directory as keys, with empty values.
    """
    directory_contents = {}

    for root, dirs, files in os.walk(path):
        # Normalize the root path to avoid double backslashes
        root = os.path.normpath(root)
        
        # Filter out files that do not match the specified names
        filtered_files = [file for file in files if file.endswith(('_bg.png', '_composite.png', 'Bg_textures.png', 'Collisions.csv', 'Collisions.png', 'Collisions-int.png', 'data.json', 'Wall_shadows.png'))]

        if filtered_files:
            directory_contents[root] = {file: None for file in filtered_files}

    return directory_contents

# TODO : determine if needed

# def createLevelsDirectory():
#     current_directory = unreal.Paths.project_content_dir()

#     ## TODO: Find a way to not have to do this when the computer's local is not english, other wise it does not find the folder at the path
#     current_directory = current_directory.replace("Users", "Utilisateurs")

#     # Specify the directory name
#     directory_name = "Levels"

#     # Get the absolute path of the directory within the project
#     directory_path = os.path.join(current_directory, directory_name)

#     # Check if the directory already exists
#     if not os.path.exists(directory_path):
#         try:
#             # Create the directory if it doesn't exist
#             os.makedirs(directory_path)
#             print(f"Directory '{directory_name}' created successfully at: {directory_path}")
#         except Exception as e:
#             # Print an error message if any error occurs
#             print(f"An error occurred: {e}")
#     else:
#         print(f"Directory '{directory_name}' already exists at: {directory_path}")
    
def importWorld():
    content_directory = unreal.Paths.project_content_dir()
    level_files_location = "LdtkFiles/simplified"
    level_directory = os.path.join(content_directory, level_files_location)

    base_directory = "/Game"
    ldtk_files_directory = "LdtkFiles"
    ldtk_simplified_directory = "simplified"
    base_path = os.path.join(base_directory, ldtk_files_directory, ldtk_simplified_directory)

    composite_filename = "_composite"
    data_filename = "data.json"
    collisions_filename = "Collisions.csv"

    directories = find_all_subfolders(level_directory)
    print("Level directory: " + level_directory)

    loaded_data = []

    for index, directory in enumerate(directories):
        _, directory_name = os.path.split(directory)
        print(f"directoryName: {directory_name}")
        full_path_composite = os.path.join(base_path, directory_name, composite_filename)
        full_path_data = os.path.join(level_directory, directory_name, data_filename).replace("\\", "/")

        composite_texture = load_texture_asset(full_path_composite)

        composite_sprite = create_sprite_from_texture(composite_texture, directory_name)

        print(f"composite sprite: {composite_sprite}")

        data_file = open(full_path_data)
        data = json.load(data_file)
        composite_spawn_coords = (data['x'] + (data['width'] / 2), data['y'] + (data['height'] / 2), 0)

        loaded_data.append(data)

        sprite_scale = (1, 1, 1)

        spawned_composite_actor = spawn_sprite_in_world(composite_sprite, (composite_spawn_coords), sprite_scale)

        print(f"Spawned this actor: {spawned_composite_actor}")

        collisions_csv = os.path.join(level_directory, directory_name, collisions_filename).replace("\\", "/")

        # TODO: make this work ! add_colliders_from_csv(collisions_csv, spawned_composite_actor)

        #find_collision_areas(full_path_data)
    
##run()

def check_and_delete_existing_sprite(sprite_name):
    sprite_path = "/Game/LdtkFiles/" + sprite_name

    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for actor in all_actors:
        if actor.get_actor_label() == sprite_name:
            unreal.EditorLevelLibrary.destroy_actor(actor)
            break

    if unreal.EditorAssetLibrary.does_asset_exist(sprite_path):
        unreal.EditorAssetLibrary.delete_asset(sprite_path)
    

def load_texture_asset(texture_path):
    texture = unreal.EditorAssetLibrary.load_asset(texture_path)
    return texture

def create_sprite_from_texture(texture_asset: unreal.PaperSprite, world_name):
    try:
        sprite_path = "/Game/LdtkFiles"
        sprite_name = f"LDtk_{world_name}_{texture_asset.get_name()}_sprite"

        check_and_delete_existing_sprite(sprite_name=sprite_name)

        sprite_package = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=sprite_name, package_path=sprite_path, asset_class=unreal.PaperSprite, factory=unreal.PaperSpriteFactory())
        sprite_package.set_editor_property("source_texture", texture_asset)

        print("Sprite saved at: ", sprite_path)
        return sprite_package
    except:
        pass
         
def spawn_sprite_in_world(sprite, location=(0, 0, 0), scale=(1, 1, 1)):

    # world = unreal.EditorLevelLibrary.get_editor_world() TODO: determined if really useless or not 
    
    spawn_location = unreal.Vector(location[0], location[1], location[2])
    
    scale_vector = unreal.Vector(scale[0], scale[1], scale[2])

    actor_transform = unreal.Transform(spawn_location, unreal.Rotator(270, 0, 0), scale_vector)
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(sprite, spawn_location)
    if actor:
        # Get the PaperSpriteComponent attached to the actor
        sprite_component = actor.render_component
        if sprite_component:

            sprite_component.set_sprite(sprite)
            
            actor.set_actor_scale3d(scale_vector)
            
            actor.set_actor_transform(actor_transform, False, True)
            
            return actor
    return None

def spawn_paper2d_image(png_path, position=(0, 0, 0), scale=(1, 1, 1)):
    base_directory = "/Game"
    ldtk_files_path = "LdtkFiles"
    filename = "amogus"
    full_path = os.path.join(base_directory, ldtk_files_path, filename)

    texture_asset = load_texture_asset(full_path)
    if texture_asset:
        sprite = create_sprite_from_texture(texture_asset)
        if sprite:
            spawn_location = (0, 0, 0) 
            spawned_actor = spawn_sprite_in_world(sprite, spawn_location)
            if spawned_actor:
                print("Sprite spawned successfully.")
            else:
                print("Failed to spawn sprite in the world.")
        else:
            print("Failed to create sprite.")
    else:
        print("Failed to load texture asset.")


    # project_dir = unreal.Paths.project_dir().lstrip("../")
    # file_path = os.path.join(project_dir, png_path)

    # print("Searching for: " + file_path)
    # if os.path.isfile(file_path):
    #     relative_path = os.path.join(png_path)
    #     texture = unreal.EditorAssetLibrary.load_asset(relative_path)

    # else:
    #     unreal.log_warning(f"File not found: {file_path}")

    # project_dir = unreal.Paths.project_dir()
    # absolute_path = os.path.join(project_dir, png_path)

    # print(f"Absolute path : {absolute_path}")

    # # Check if the file exists
    # if not os.path.isfile(absolute_path):
    #     unreal.log_warning(f"File not found: {absolute_path}")
    #     return None

    # # Load the PNG file as a texture
    # relative_path = os.path.join(png_path)
    # texture2d = unreal.EditorAssetLibrary.load_asset(relative_path)

    # # Check if the texture is valid
    # if not texture2d:
    #     unreal.log_warning(f"Failed to load the texture from path: {absolute_path}")
    #     return None

#noinspection PyUnresolvedReferences
importWorld()

#noinspection PyUnresolvedReferences
# print(full_path) ## Value from locals given by unreal python node in the exec function
# print(project_dir_path)
print(datetime.datetime.now())
convert_transparent_to_black_and_white("C:/Users/Isabel/Desktop/tests/tmp/simplified/Bottom/Collisions.png", "C:/Users/Isabel/Desktop/tests/output.png")

