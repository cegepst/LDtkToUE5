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


## Documentation (FR)

### Description



### Guide d'installation et d'utilisation

#### Dépendances



## Sources

- Unreal Python API (LINK HERE)
- Tutorial on how to setup UE5 with Unreal Engine (LINK HERE)
