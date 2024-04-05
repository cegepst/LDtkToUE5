import unreal
import math
import json
import pprint
import datetime
import os
from enum import Enum
from typing import Any, List, Optional, Dict, TypeVar, Type, Callable, cast

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
        #composite_spawn_coords = (data['x'], data['y'], 0)

        # if index == 0: 
        #     composite_spawn_coords = (data['x'], 0, data['y'])
        # else:
        #     xCoord = data['x'] + loaded_data[index - 1]['x'] / 2
        #     yCoord = data['y'] + loaded_data[index - 1]['y'] / 2
        #     composite_spawn_coords = (xCoord, 0, yCoord)

        loaded_data.append(data)

        sprite_scale = (1, 1, 1)

        spawned_composite_actor = spawn_sprite_in_world(composite_sprite, (composite_spawn_coords), sprite_scale)

        print(spawned_composite_actor)

        find_collision_areas(full_path_data)

    #Get all files for all directories and map them
    #newPath = os.path.dirname(os.path.dirname(simplifiedPath))
    #content = get_directory_contents(newPath)
    #first_directory = list(content.keys())[0]
    #composite_file = '_composite.png'
    #complete_file_path = os.path.join(first_directory, composite_file)

    #users_index = complete_file_path.find("LDtkToUE5")
    #if users_index != -1:
    #    complete_file_path = complete_file_path[users_index:]

    #complete_file_path = '\\' + complete_file_path

    #spawn_paper2d_image(complete_file_path)
    #spawn_paper2d_image("/ldtk_levels/test/simplified/Bottom/_bg.png")

    # #Get content of each directory
    # for directory in directories :
    #     content = get_directory_contents(newPath)


    ##check filetype
    # _, file_extension = os.path.splitext(ldtkFilePath)

    # if file_extension == '.ldtk': 

    #     print("Processing .ldtk file")

    #     with open(ldtkFilePath, 'r') as file:
    #         json_content = file.read()
    #     result = ldtk_json_from_dict(json.loads(json_content))
    #     print('LDtk levels loaded successfully: %s', result)
    #     pprint.pprint(vars(result))

    # # elif file_extension == '.json':

    # #     print("Processing .json file")

    # #     factory = unreal.PaperTiledImporterFactory
    # #     factory.asset_import_task()

    # #     with open(ldtkFilePath, 'r') as file:
    # #         json_content = file.read()
    # #     result = unreal.PaperTiledImporterFactory(json.loads(json_content))
    # #     print('Tiled JSON file loaded successfully: %s', result)
    # #     pprint.pprint(vars(result))
    
##run()

def load_texture_asset(texture_path):
    texture = unreal.EditorAssetLibrary.load_asset(texture_path)
    return texture

def create_sprite_from_texture(texture_asset: unreal.PaperSprite, world_name):
    try:
        # Specify the path where you want to save the sprite
        sprite_path = "/Game/LdtkFiles"
        sprite_name = f"LDtk_{world_name}_{texture_asset.get_name()}_sprite"

        # Create a new package to store the sprite
        sprite_package = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=sprite_name, package_path=sprite_path, asset_class=unreal.PaperSprite, factory=unreal.PaperSpriteFactory())
        # Add the sprite to the package
        sprite_package.set_editor_property("source_texture", texture_asset)

        # Print the path where the sprite is saved
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
print(full_path) ## Value from locals given by unreal python node in the exec function
print(project_dir_path)
print(datetime.datetime.now())
