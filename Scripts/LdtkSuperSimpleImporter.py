import unreal
import math
import json
import pprint
import datetime
import os
import csv
import uuid
from enum import Enum
from typing import Any, List, Optional, Dict, TypeVar, Type, Callable, cast

from PIL import Image

def load_csv(file_path):
    grid = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Process each row and handle empty cells
            grid_row = []
            for cell in row:
                # Convert the cell to an integer if it's not empty
                if cell.strip() == '':
                    grid_row.append(0)  # Use a default value for empty cells
                else:
                    grid_row.append(int(cell))
            # Append the processed row to the grid
            grid.append(grid_row)
    return grid

def create_collision(actor: unreal.PaperSpriteActor, x, y, tile_size):
    initial_children_count = actor.root_component.get_num_children_components()

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root_data_handle = subsystem.k2_gather_subobject_data_for_instance(actor)[0]
    
    collision_component = unreal.BoxComponent()
    sub_handle, fail_reason = subsystem.add_new_subobject(params=unreal.AddNewSubobjectParams(parent_handle=root_data_handle, new_class=collision_component.get_class()))
    subsystem.rename_subobject(handle=sub_handle, new_name=unreal.Text(f"LDTK_Collision_{uuid.uuid4()}"))

    new_component: unreal.BoxComponent = actor.root_component.get_child_component(initial_children_count)

    new_component.set_box_extent(unreal.Vector(tile_size / 2, tile_size / 2, 0))
    new_component.set_relative_location_and_rotation(unreal.Vector((x + (tile_size / 2)), 10, -(y + (tile_size / 2))), unreal.Rotator(90, 0, 0),False, False)
    
def spawn_collisions_from_grid(grid, actor: unreal.PaperSpriteActor, composite_width, composite_height):
    tile_size = 16
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            x = (col_index * tile_size) - (composite_width / 2)
            y = row_index * tile_size - (composite_height / 2)

            if cell == 1:
                create_collision(actor, x, y, tile_size)

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
        root = os.path.normpath(root)
        
        filtered_files = [file for file in files if file.endswith(('_bg.png', '_composite.png', 'Bg_textures.png', 'Collisions.csv', 'Collisions.png', 'Collisions-int.png', 'data.json', 'Wall_shadows.png'))]

        if filtered_files:
            directory_contents[root] = {file: None for file in filtered_files}

    return directory_contents

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
        full_path_collisions = os.path.join(level_directory, directory_name, collisions_filename).replace("\\", "/")

        ## Creating Sprite ##

        composite_texture = load_texture_asset(full_path_composite)

        composite_sprite = create_sprite_from_texture(composite_texture, directory_name)

        print(f"composite sprite: {composite_sprite}")

        ## Reading JSON file ##

        data_file = open(full_path_data)
        data = json.load(data_file)
        composite_spawn_coords = (data['x'] + (data['width'] / 2), data['y'] + (data['height'] / 2), 0)

        loaded_data.append(data)

        sprite_scale = (1, 1, 1)

        spawned_composite_actor = spawn_sprite_in_world(composite_sprite, (composite_spawn_coords), sprite_scale)

        print(f"Spawned this actor: {spawned_composite_actor}")

        ## Spawning Collisions ##
        
        grid = load_csv(full_path_collisions)
        spawn_collisions_from_grid(grid, spawned_composite_actor, data['width'], data['height'])

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
        #unreal.facto
        sprite_package.set_editor_property("source_texture", texture_asset)

        print("Sprite saved at: ", sprite_path)
        return sprite_package
    except:
        pass
         
def spawn_sprite_in_world(sprite, location=(0, 0, 0), scale=(1, 1, 1)):

    spawn_location = unreal.Vector(location[0], location[1], location[2])
    
    scale_vector = unreal.Vector(scale[0], scale[1], scale[2])

    actor_transform = unreal.Transform(spawn_location, unreal.Rotator(0, 0, 0), scale_vector)
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(sprite, spawn_location)
    if actor:
        sprite_component = actor.render_component
        if sprite_component:

            sprite_component.set_sprite(sprite)
            
            actor.set_actor_scale3d(scale_vector)
            
            actor.set_actor_transform(actor_transform, False, True)
            
            return actor
    return None

#noinspection PyUnresolvedReferences
importWorld()

#noinspection PyUnresolvedReferences
# print(full_path) ## Value from locals given by unreal python node in the exec function
# print(project_dir_path)
print(datetime.datetime.now())