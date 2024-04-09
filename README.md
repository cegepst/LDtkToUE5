| Language | Documentation |
|----------|---------------|
| EN       | [Documentation (EN)](#documentation-en) |
| FR       | [Documentation (FR)](#documentation-fr) |





## Documentation (EN)

### Description


### Setup and Usage guide

#### Dependencies

- Python (included within UE5)
- Unreal Python API (Already installed)

#### Creating project and enabling Python editor scripting

1. Create a new UE5 project, using the blank template
2. Navigate to `Edit > Plugins`
3. Make sure *Python Editor Scripting* is enabled
4. Navigate to `Edit > Editor Preferences > Python`
5. Enable the following: 
- Dev Mode
- Content Browser Integration
6. Restart UE5

#### Add the importer to your project

1. Locate the newly created Python folder inside of the editor's Content Browser
2. Create an empty folder inside of it
- This is important, as it will not show in the operating system's content browser until there is content inside of it.
3. Download the project as a zip file
4. Extract the content
5. Open your projects Python folder inside of your operating system's file browser
7. Open the extracted files, and access the directory in which the python scripts and the widgets are contained (The files inside `unreal-ldtk-main`)
8. Drag and drop the extracted files (not the main folder, but the files within) into the Python folder
9. Restart UE5

## Exporting your LDtk level correctly

To correctly export your LDtk level for usage with our tool, you will need to use the Super Simple Export feature. As of writing this, this feature has a bug impacting the export of the files. We found a workaround for this, and opened an issue describing the bug (https://github.com/deepnight/ldtk/issues/1095)

The following steps account for the required workaround

1. Open your LDtk level inside of the LDtk editor
2. Access the project settings menu
3. Enable Super Simple Export
4. Click `Save As`
5. Close LDtk
6. Access your exported level inside of your operating system's file browser
7. Double-click on the LDtk file to reopen the level inside of the editor
8. Access the project settings menu
9. Click `Save Project`

- The level will now correctly export

## Importing your exported LDtk level 

1. Open the UE5 editor
2. Access the `Content` directory in the content browser
3. Create a new folder, called exactly like the following:

- `LdtkFiles`

4. Open the newly created `LdtkFiles` folder

5. Inside of your operating system's file browser, access your exported level
6. Access the `simplified` folder

- Keep it open, you'll need it later

7. Take the `simplified` folder, and drop it inside of UE5's content browser, inside of the `LdtkFiles` folder
8. A menu will open asking to import. The selected option does not matter, but I recommend selecting `Data table` and `CollisionEvent` for the options, as we know they do not cause any issues
9. Import all of the prompted imports
10. When done, close UE5, and select `Save Selected`
11. Access the `LdtkFiles` folder inside of your operating system's file browser
12. Access the original `simplified` folder from your exported level, which you kept open earlier.
13. Copy and Paste it into the UE5 project's `LdtkFiles` folder.

- This copies over all the original files that are required for calculations by our Python script. If not done, the script will return errors because it could not find the required files, like for example `data.json`, `Collisions.csv`, etc.
- You can also drag and drop the files, but you will likely lose the original files from the export inside of the original directory, because they will be transferred over.

14. Reopen UE5
15. Click `Don't import` on the prompt at the bottom left of the screen when the editor opens
16. Access the `Python` folder inside of the content browser
17. Right-click on the `Main_Window` Editor Utility Widget
18. Click on `Run Editor Utility Widget`
19. Click on the yellow `Import` button
20. Enjoy !

## Documentation (FR)

### Description



### Guide d'installation et d'utilisation

#### Dépendances



## Sources

- Unreal Python API (LINK HERE)
- Tutorial on how to setup UE5 with Unreal Engine (LINK HERE)
