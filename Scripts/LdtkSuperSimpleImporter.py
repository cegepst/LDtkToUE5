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

def load_csv(file_path):
    grid = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            grid_row = []
            for cell in row:
                if cell.strip() == '':
                    grid_row.append(0)
                else:
                    grid_row.append(int(cell))
            grid.append(grid_row)
    return grid

def create_collision(actor: unreal.PaperSpriteActor, x, y, tile_size):
    initial_children_count = actor.root_component.get_num_children_components()

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root_data_handle = subsystem.k2_gather_subobject_data_for_instance(actor)[0]
    
    collision_component = unreal.BoxComponent()
    sub_handle, _ = subsystem.add_new_subobject(params=unreal.AddNewSubobjectParams(parent_handle=root_data_handle, new_class=collision_component.get_class()))
    subsystem.rename_subobject(handle=sub_handle, new_name=unreal.Text(f"LDTK_Collision_{uuid.uuid4()}"))

    new_component: unreal.BoxComponent = actor.root_component.get_child_component(initial_children_count)

    new_component.set_box_extent(unreal.Vector(tile_size / 2, tile_size / 2, 64))
    new_component.set_relative_location_and_rotation(unreal.Vector((x + (tile_size / 2)), -32, -(y + (tile_size / 2))), unreal.Rotator(90, 0, 0),False, False)
    new_component.set_collision_profile_name("BlockAll")
    
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
    directory_contents = {}

    for root, _, files in os.walk(path):
        root = os.path.normpath(root)
        filtered_files = [file for file in files if file.endswith(('_bg.png', '_composite.png', 'Bg_textures.png', 'Collisions.csv', 'Collisions.png', 'Collisions-int.png', 'data.json', 'Wall_shadows.png'))]

        if filtered_files:
            directory_contents[root] = {file: None for file in filtered_files}

    return directory_contents

def importWorld():
    level_files_location = "LdtkFiles/simplified"
    base_directory = "/Game"
    ldtk_files_directory = "LdtkFiles"
    ldtk_simplified_directory = "simplified"
    composite_filename = "_composite"
    data_filename = "data.json"
    collisions_filename = "Collisions.csv"

    base_path = os.path.join(base_directory, ldtk_files_directory, ldtk_simplified_directory)
    content_directory = unreal.Paths.project_content_dir()
    level_directory = os.path.join(content_directory, level_files_location)
    directories = find_all_subfolders(level_directory)

    if directories.__len__() > 0:
        print(f"Unreal LDtk: Found {len(directories)} directories in {level_directory}. Beginning import...")
    else:
        print(f"Unreal LDtk: No directories found in {level_directory}. This might be because you are missing the LdtkFiles directory. Exiting...")
        return

    entity_index_counter = 0

    for index, directory in enumerate(directories):
        _, directory_name = os.path.split(directory)
        full_path_composite = os.path.join(base_path, directory_name, composite_filename)
        full_path_data = os.path.join(level_directory, directory_name, data_filename).replace("\\", "/")
        full_path_collisions = os.path.join(level_directory, directory_name, collisions_filename).replace("\\", "/")
        
        composite_exists = unreal.EditorAssetLibrary.does_asset_exist(full_path_composite)
        data_exists = os.path.exists(full_path_data)
        collisions_exists = os.path.exists(full_path_collisions)

        ## Creating Sprite ##
        if composite_exists:
            composite_texture = load_texture_asset(full_path_composite)

            composite_sprite = create_sprite_from_texture(composite_texture, directory_name)
        else:
            print(f"Unreal LDtk: Missing composite texture asset, skipping...")

        ## Reading JSON file ##
        if data_exists:
            data_file = open(full_path_data)
            data = json.load(data_file)
            data_file.close()
            composite_spawn_coords = (data['x'] + (data['width'] / 2), data['y'] + (data['height'] / 2), 0)
        else:
            print(f"Unreal LDtk: Missing data.json file, skipping...")

        if (composite_exists and data_exists):
            spawned_composite_actor = spawn_sprite_in_world(composite_sprite, (composite_spawn_coords))
            ## Spawning Entities ##
            for _, entities in data['entities'].items():
                for index, entity in enumerate(entities):
                    spawn_entity_in_world(f"LDtk_{entity['id']}_{entity_index_counter}", data['x'] + entity['x'], data['y'] + entity['y'])
                    entity_index_counter += 1
        else:
            print(f"Unreal LDtk: Missing composite and/or data.json file, skipping entities...")

        ## Spawning Collisions ##
        if composite_exists and collisions_exists:
            grid = load_csv(full_path_collisions)
            spawn_collisions_from_grid(grid, spawned_composite_actor, data['width'], data['height'])
        else: 
            print(f"Unreal LDtk: Missing Composite and/or Collisions.csv file, skipping collisions...")

def check_and_delete_existing_sprite(sprite_name):
    sprite_path = "/Game/LdtkFiles/" + sprite_name

    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for actor in all_actors:
        if actor.get_actor_label() == sprite_name:
            unreal.EditorLevelLibrary.destroy_actor(actor)
            print(f"Deleting existing composite sprite: {actor}")
            break

    if unreal.EditorAssetLibrary.does_asset_exist(sprite_path):
        unreal.EditorAssetLibrary.delete_asset(sprite_path)

def check_and_delete_existing_entity(entity_name):
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for actor in all_actors:
        if actor.get_actor_label() == entity_name:
            unreal.EditorLevelLibrary.destroy_actor(actor)
            print(f"Deleting existing entity: {actor}")
            break

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

def spawn_entity_in_world(name, x, y):
    location = unreal.Vector(x, 1, -y)

    check_and_delete_existing_entity(name)

    actor: unreal.Actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor().get_class(), location)

    if actor:
        actor.set_actor_label(name)
        print(f"Spawning entity: {actor.get_actor_label()}")

    return actor
         
def spawn_sprite_in_world(sprite, location=(0, 0, 0), scale=(1, 1, 1)):

    spawn_location = unreal.Vector(location[0], location[2], -location[1])
    
    scale_vector = unreal.Vector(scale[0], scale[1], scale[2])

    actor_transform = unreal.Transform(spawn_location, unreal.Rotator(0, 0, 0), scale_vector)
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(sprite, spawn_location)
    if actor:
        sprite_component = actor.render_component
        if sprite_component:

            sprite_component.set_sprite(sprite)
            
            actor.set_actor_scale3d(scale_vector)
            
            actor.set_actor_transform(actor_transform, False, True)
            
            print(f"Spawning composite sprite: {actor.get_actor_label()}")

            return actor
    return None

#noinspection PyUnresolvedReferences
importWorld()

#noinspection PyUnresolvedReferences
print(datetime.datetime.now())