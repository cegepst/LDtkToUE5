import unreal
import math
import json
import pprint
import datetime
import os
from enum import Enum
from typing import Any, List, Optional, Dict, TypeVar, Type, Callable, cast

def find_all_subfolders(path):
    # Initialize an empty list to store the subfolder paths
    subfolders = []
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(path): # Corrected line
        # For each directory in the tree, add its path to the list
        for dir in dirs:
            subfolders.append(os.path.join(root, dir))
    
    return subfolders



# Define a type alias for the directory contents structure
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
            # Convert backslashes to single backslashes
            # Add the directory and its contents to the dictionary
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
    # spawn_paper2d_image()
    content_directory = unreal.Paths.project_content_dir()
    level_files_location = "LdtkFiles/simplified"
    level_directory = os.path.join(content_directory, level_files_location)

    base_directory = "/Game"
    ldtk_files_directory = "LdtkFiles"
    ldtk_simplified_directory = "simplified"
    base_path = os.path.join(base_directory, ldtk_files_directory, ldtk_simplified_directory)

    composite_filename = "_composite"
    data_filename = "data.json"

    # Get the directories
    directories = find_all_subfolders(level_directory)

    for directory in directories:
        _, directory_name = os.path.split(directory)
        print(f"directoryName: {directory_name}")
        full_path_composite = os.path.join(base_path, directory_name, composite_filename)
        full_path_data = os.path.join(level_directory, directory_name, data_filename)

        compositeTexture = load_texture_asset(full_path_composite)

        compositeSprite = create_sprite_from_texture(compositeTexture, directory_name)

        print(f"composite sprite: {compositeSprite}")

        data_file = open(full_path_data)
        data = json.load(data_file)
        print(f"data x: {data['x']}")
        composite_spawn_coords = (data['x'], data['y'], 0)

        spawned_actor = spawn_sprite_in_world(compositeSprite, (composite_spawn_coords))

        print(spawned_actor)

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
    
def onButtonClick():
    project_dir = unreal.Paths.project_dir()
    widget_dir = project_dir + "Content/Python/m"
    widgetBlueprint = unreal.load_object(None, widget_dir)
    widget = unreal.EditorUserWidget.create_instance(widgetBlueprint)
    json = widget.get_named_slot_content('textBox').get_text().to_string()
    importWorld(json)

def load_texture_asset(texture_path):
    # Load the texture asset
    texture = unreal.EditorAssetLibrary.load_asset(texture_path)
    return texture

def create_sprite_from_texture(texture_asset: unreal.PaperSprite, world_name):
    try:
        # Specify the path where you want to save the sprite
        sprite_path = "/Game/LdtkFiles"
        sprite_name = f"{world_name}_{texture_asset.get_name()}_sprite"

        # Create a new package to store the sprite
        sprite_package = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=sprite_name, package_path=sprite_path, asset_class=unreal.PaperSprite, factory=unreal.PaperSpriteFactory())
        # Add the sprite to the package
        sprite_package.set_editor_property("source_texture", texture_asset)

        # Print the path where the sprite is saved
        print("Sprite saved at: ", sprite_path)
        return sprite_package
    except:
        pass
         
def spawn_sprite_in_world(sprite, location=(0, 0, 0), scale=1.0):
    # Spawn the sprite in the world at the specified location

    # world = unreal.EditorLevelLibrary.get_editor_world() TODO: determined if really useless or not 

    spawn_location = unreal.Vector(location[0], location[1], location[2])
    
    # Set the scale vector
    scale_vector = unreal.Vector(scale, scale, scale)
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(sprite, spawn_location, transient=False)
    if actor:
        # Get the PaperSpriteComponent attached to the actor
        sprite_component = actor.render_component
        if sprite_component:
            # Set the sprite for the PaperSpriteComponent
            sprite_component.set_sprite(sprite)
            
            # Set the scale of the actor
            actor.set_actor_scale3d(scale_vector)
            
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
            spawn_location = (0, 0, 0)  # Spawn location in the world
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
