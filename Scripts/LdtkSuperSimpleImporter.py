import unreal
import math
import json
import pprint
import datetime
import os

from enum import Enum
from typing import Any, List, Optional, Dict, TypeVar, Type, Callable, cast

def spawnCube(location=unreal.Vector(), rotation=unreal.Rotator()):
    editorActorSubs = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actorClass = unreal.StaticMeshActor
    staticMeshActor = editorActorSubs.spawn_actor_from_class(actorClass, location, rotation)
    staticMesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")

    # Correctly get the StaticMeshComponent and set the static mesh
    staticMeshComponent = staticMeshActor.get_component_by_class(unreal.StaticMeshComponent.static_class())
    staticMeshComponent.set_static_mesh(staticMesh)

def run():
    # Provide specific values for location and rotation if needed
    cube_count = 12
    circle_radius = 1000
    circle_center = unreal.Vector(0, 0, 0)

    for i in range(cube_count):
        circle_x_location = circle_radius * math.cos(math.radians(i * 360.0 / cube_count))
        circle_y_location = circle_radius * math.sin(math.radians(i * 360.0 / cube_count))
        location = unreal.Vector(circle_x_location, circle_y_location, 0)
        spawnCube(location)

def find_all_subfolders(path):
    # Go back 2 directories
    newPath = os.path.dirname(os.path.dirname(path))

    # Initialize an empty list to store the subfolder paths
    subfolders = []
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(newPath): # Corrected line
        # For each directory in the tree, add its path to the list
        for dir in dirs:
            subfolders.append(os.path.join(root, dir))
    
    return subfolders

import os
from typing import Dict, Any

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

def createLevelsDirectory():
    current_directory = unreal.Paths.project_content_dir()

    ## TODO: Find a way to not have to do this when the computer's local is not english, other wise it does not find the folder at the path
    current_directory = current_directory.replace("Users", "Utilisateurs")

    # Specify the directory name
    directory_name = "Levels"

    # Get the absolute path of the directory within the project
    directory_path = os.path.join(current_directory, directory_name)

    # Check if the directory already exists
    if not os.path.exists(directory_path):
        try:
            # Create the directory if it doesn't exist
            os.makedirs(directory_path)
            print(f"Directory '{directory_name}' created successfully at: {directory_path}")
        except Exception as e:
            # Print an error message if any error occurs
            print(f"An error occurred: {e}")
    else:
        print(f"Directory '{directory_name}' already exists at: {directory_path}")
    
def importWorld(simplifiedPath):
    spawn_paper2d_image("_bg.png")
    #Get the directories inside of the simplified folder path
    #directories = find_all_subfolders(simplifiedPath)

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

def create_sprite_from_texture(texture_asset: unreal.PaperSprite):

    try:
        # Specify the path where you want to save the sprite
        sprite_path = "/Game/LdtkFiles"
        sprite_name = f"{texture_asset.get_name()}_sprite"

        # Create a new package to store the sprite
        sprite_package = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=sprite_name, package_path=sprite_path, asset_class=unreal.PaperSprite, factory=unreal.PaperSpriteFactory())
        # Add the sprite to the package
        sprite_package.set_editor_property("source_texture", texture_asset)

        # Print the path where the sprite is saved
        print("Sprite saved at: ", sprite_path)
    except:
        pass
         

    

def spawn_sprite_in_world(sprite, location=(0, 0, 0), scale=100.0):
    # Spawn the sprite in the world at the specified location
    world = unreal.EditorLevelLibrary.get_editor_world()
    spawn_location = unreal.Vector(location[0], location[1], location[2])
    
    # Set the scale vector
    scale_vector = unreal.Vector(scale, scale, scale)
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PaperSpriteActor, spawn_location, transient=False)
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
importWorld(full_path)

#noinspection PyUnresolvedReferences
print(full_path) ## Value from locals given by unreal python node in the exec function
print(project_dir_path)
print(datetime.datetime.now())
