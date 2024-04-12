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

def find_collision_areas(collisions_filepath):
    def find_connected_components(grid):
        visited = set()
        components = []

        def dfs(x, y):
            if (x, y) not in grid or grid[(x, y)] != 1 or (x, y) in visited:
                return

            visited.add((x, y))
            component.append((x, y))

            dfs(x-1, y)
            dfs(x+1, y)
            dfs(x, y-1)
            dfs(x, y+1)

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[(x, y)] == 1 and (x, y) not in visited:
                    component = []
                    dfs(x, y)
                    components.append(component)

        return components

    with open(collisions_filepath, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    grid = {}
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            grid[(x, y)] = int(value)

    return find_connected_components(grid)

def spawn_collision_object(x, y, composite_actor):
    collider = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.BoxComponent, (x, y, 0), (0, 0, 0))
    collider.set_actor_scale3d(unreal.Vector(1, 1, 1))
    collider.attach_to_actor(composite_actor, '', unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, True)

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
        # collision_areas = find_collision_areas(collisions_csv)
        # for area in collision_areas:
        #     for x, y in area:
        #         spawn_collision_object(x, y, spawned_composite_actor)

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

    spawn_location = unreal.Vector(location[0], location[1], location[2])
    
    scale_vector = unreal.Vector(scale[0], scale[1], scale[2])

    actor_transform = unreal.Transform(spawn_location, unreal.Rotator(270, 0, 0), scale_vector)
    
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