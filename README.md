# LDtkToUE5

| Language | Documentation |
|----------|---------------|
| EN       | [Documentation (EN)](#documentation-en) |
| FR       | [Documentation (FR)](#documentation-fr) |


![LdtkToUE5-logo](https://github.com/cegepst/unreal-ldtk/assets/112954452/baf1a5d9-e663-48bb-95ae-830f5ee801e1)


# Documentation (EN)

   - [Description](#description)
   - [Video tutorial](#video-tutorial)
   - [Setup and Usage guide](#setup-and-usage-guide)
     - [Dependencies](#dependencies)
     - [Creating project and enabling Python editor scripting](#creating-project-and-enabling-python-editor-scripting)
     - [Add the importer to your project](#add-the-importer-to-your-project)
   - [Exporting your LDtk level correctly](#exporting-your-ldtk-level-correctly)
     - [File nomenclature](#file-nomenclature)
   - [Importing your exported LDtk level](#importing-your-exported-ldtk-level)

## Description

*LDtkToUE5* is a plugin that thrives to bring functionnalities similar to plugins for other game engines, such as LDtkToUnity, to Unreal Engine 5. 

Following the drama related to Unity introducing fees per downloads to games developers made, many made the jump to other popular game engines, such as Godot and Unreal Engine 5. Godot already having an integration for LDtk, it was in our interest to make one for UE5

Its primary functionnality is the dynamic importation of 2D levels exported from the LDtk software, using JSON and PNG files.

# Video tutorial
While we still recommend to read the complete documentation, here is a video tutorial to help illustrate the steps for using this tool: [Tutorial](https://www.youtube.com/watch?v=fVNpgvaT0aI)

## Setup and Usage guide

### Dependencies

- Python (included within UE5)
- Unreal Python API (Already installed)

### Creating project and enabling Python editor scripting

1. Create a new UE5 project, using the *blank template*
2. Navigate to `Edit > Plugins` ![Capture d’écran 2024-04-12 094112](https://github.com/cegepst/unreal-ldtk/assets/112954452/0a45893a-357c-417c-a233-a1bde611279d)
3. Make sure *Python Editor Scripting* is enabled
4. Navigate to `Edit > Editor Preferences > Python` 
    - On MacOS, click on *UnrealEditor* in the top bar, and then on *Preferences*
5. Enable the following: 

    - *Dev Mode*
    - *Content Browser Integration*
   
    ![Capture d’écran 2024-04-12 094607](https://github.com/cegepst/unreal-ldtk/assets/112954452/10454be7-3660-4c01-916d-5e614f0f7155)

6. Restart UE5

### Add the importer to your project

1. Locate the newly created Python folder inside of the editor's Content Browser
2. Create an empty folder inside of it

    - **This is important**, as it will not show in the operating system's content browser until there is content inside of it.

3. Download the project as a zip file
4. Extract the content
5. Open your projects Python folder inside of your operating system's file browser
7. Open the extracted files, and access the directory in which the python scripts and the widgets are contained (The files inside `unreal-ldtk-main`)
8. Drag and drop the extracted files (not the main folder, but the files within) into the Python folder
9. Restart UE5
10. When reopened, click *import* on the pop-up at the bottom right of the screen

## Exporting your LDtk level correctly

To correctly export your LDtk level for usage with our tool, you will need to use the *Super Simple Export* feature. As of writing this, this feature has a bug impacting the export of the files. We found a workaround for this, and opened an issue describing the bug (https://github.com/deepnight/ldtk/issues/1095)

The following steps account for the required workaround :

1. Open your LDtk level inside of the LDtk editor
2. Access the *project settings* menu
3. Enable *Super Simple Export* ![Capture d’écran 2024-04-12 095603](https://github.com/cegepst/unreal-ldtk/assets/112954452/40269705-94cd-473d-a082-a4fb4ae89b1a)

4. Click `Save As`
5. Close LDtk
6. Access your exported level inside of your operating system's file browser
7. Double-click on the LDtk file to reopen the level inside of the editor
8. Access the project settings menu
9. Click `Save Project`

The level will now correctly export

### File nomenclature and specific LDtk settings
The exported files shall be named correctly for the tool to work. If they do not match exactly what is specified here, the tool **WILL NOT WORK !**
- The intgrid containing the collision data: **Collisions.csv**
- The JSON file containing the level's overall data: **data.json**
- The composite of all of the layers: **_composite.png**

Your LDtk project settings should match these. Otherwise, the importer might not work as expected: 
- Workspace settings
  - Default layer grid = 16 px
  - Default entity size = 16 x 16 px

## Importing your exported LDtk level 

1. Open the UE5 editor
2. Access the `Content` directory in the content browser
3. Create a new folder, called exactly like the following:

```
LdtkFiles
```

4. Open the newly created `LdtkFiles` folder
5. Create a folder for your level. (Each new level will need it's own individual folder).

6. Inside of your operating system's file browser, access your exported level
7. Access the `simplified` folder

    - Keep it open, you'll need it later

8. Take the `simplified` folder, and drop it inside of UE5's content browser, inside of the `LdtkFiles/{YOUR_LEVEL_FOLDER}` folder ![Capture d’écran 2024-04-12 095954](https://github.com/cegepst/unreal-ldtk/assets/112954452/a9419e8d-bc77-4cbc-bcad-372d3761d671)

9. A menu will open asking to import. The selected option does not matter, but we recommend selecting `Data table` and `CollisionEvent` for the options, as we know they do not cause any issues
10. Import all of the prompted imports
11. When done, close UE5, and select `Save Selected`
12. Access the `LdtkFiles` folder inside of your operating system's file browser
13. Access the original `simplified` folder from your exported level, which you kept open earlier.
14. Add the folder to the UE5 project's `LdtkFiles/{YOUR_LEVEL_FOLDER}` folder.

    - **MacOS - IMPORTANT** Hold down the option key while dragging it into the project's folder. This will give you the option to merge both folders, as to not delete the previously imported `.uasset` files.
    - **Windows - IMPORTANT**, On Windows, you can also drag and drop the folder, but you will likely lose the original files from the export inside of the original directory, because they will be transferred over to the UE5 project.

    - **This copies over all the original files that are required for calculations by our Python script.** If not done, the script will return errors because it could not find the required files, like for example `data.json`, `Collisions.csv`, etc.

15. Reopen UE5
16. Click `Don't import` on the prompt at the bottom left of the screen when the editor opens
17. Access the `Python` folder inside of the content browser
18. Right-click on the `Main_Window` Editor Utility Widget
19. Click on `Run Editor Utility Widget` ![Capture d’écran 2024-04-12 100307](https://github.com/cegepst/unreal-ldtk/assets/112954452/59577f77-423b-442a-b2a8-c54ae8ee0b47)
20. Enter the name of the folder of the level you want to import
21. Click on the yellow `Import` button
22. Enjoy !





# Documentation (FR)

- [Description](#description-1)
- [Tutoriel vidéo](tutorial-video)
- [Guide d'installation et d'utilisation](#guide-dinstallation-et-dutilisation)
  - [Dépendances](#dépendances)
  - [Création du projet et activation de Python Editor Scripting](#création-du-projet-et-activation-de-python-editor-scripting)
  - [Ajouter l'outil d'importation à votre projet](#ajouter-loutil-dimportation-à-votre-projet)
- [L'exportation de votre niveau LDtk](#lexportation-de-votre-niveau-ldtk)
  - [Nomenclature des fichiers](#nomenclature-des-fichiers)
- [L'importation de votre niveau LDtk](#limportation-de-votre-niveau-ldtk)

## Description

*LDtkToUE5* est un *plugin* qui cherche à amener les fonctionnalités d’un *plugin* tel que *LDtkToUnity* au moteur de jeu Unreal Engine 5. 

À la suite de la polémique que la direction de *Unity* eu créé en essayant d’introduire des frais par téléchargements pour les développeurs, plusieurs furent le saut vers d’autres moteurs de jeux, tel que *Godot* et *Unreal Engine 5*. 
*Godot* ayant déjà une implémentation, il était de notre intérêt de l’intégrer à *UE5* aussi.

Sa principale fonctionnalité est l’importation dynamique de niveaux 2D créés à partir du logiciel *LDtk*, par fichier *JSON* et *PNG*.

# Tutoriel vidéo
Malgré que nous recommendons fortement de lire la documentation en son entièreté, voici une vidéo pour aider à illustrer les étapes d'utilisation de l'outil: [Tutoriel](https://www.youtube.com/watch?v=fVNpgvaT0aI)

## Guide d'installation et d'utilisation

### Dépendances

- Python (inclus avec UE5)
- Unreal Python API (Préinstallé)

### Création du projet et activation de Python Editor Scripting

1. Il faut premièrement créer un nouveau projet, en utilisant le *template Blank*
2. Naviguer vers `Edit > Plugins` ![Capture d’écran 2024-04-12 094112](https://github.com/cegepst/unreal-ldtk/assets/112954452/0a45893a-357c-417c-a233-a1bde611279d)
3. Assurez-vous que *Python Editor Scripting* est activé
4. Naviguer vers `Edit > Editor Preferences > Python` 
    - Sur MacOS, cliquer sur *UnrealEditor* dans la barre du haut, et puis sur *Preferences*
5. Activer les options ci-dessous: 
    - Dev Mode
    - Content Browser Integration
  
       ![Capture d’écran 2024-04-12 094607](https://github.com/cegepst/unreal-ldtk/assets/112954452/10454be7-3660-4c01-916d-5e614f0f7155)
6. Redémarrer UE5

### Ajouter l'outil d'importation à votre projet

1. Trouvez le dossier nouvellement créé, nommé Python, dans le *Content Browser* de l'éditeur
2. Créez un dossier vide à l'intérieur

    - **Ceci est important**, car sinon, le dossier ne s'affichera pas à l'intérieur de l'explorateur de fichier de votre système d'exploitation.

3. Téléchargez le projet en fichier zip
4. Extraire le contenu du zip
5. Ouvrez le dossier Python du projet à l'intérieur de l'explorateur de fichier de votre système d'exploitation
7. Ouvrez les fichiers extraits, et accédez au dossier dans lequel le script Python et le widget sont entreposés. (Les fichiers dans `unreal-ldtk-main`)
8. Prenez et déposez les fichiers extraits (pas le dossier principal, mais les fichiers à l'intérieur) dans le dossier Python
9. Redémarrez UE5
10. Lorsque réouvert, cliquez sur *import* sur le *pop-up* en bas à gauche de l'écran

## L'exportation de votre niveau LDtk

Pour correctement exporter votre niveau LDtk pour l'utiliser avec notre outil, il faut utiliser la fonctionnalité *Super Simple Export*. Au moment de l'écriture, cette fonctionnalité contient un bug qui impact l'exportation des fichiers. Nous avons trouvé une solution temporaire au problème, et nous avons ouvert une *issue*, décrivant le bug:
(https://github.com/deepnight/ldtk/issues/1095)

Les étapes ci-dessous prennent en compte notre solution temporaire :

1. Ouvrez votre niveau Ldtk à l'intérieur de l'éditeur LDtk
2. Accédez le menu *project settings*
3. Activez *Super Simple Export* ![Capture d’écran 2024-04-12 095603](https://github.com/cegepst/unreal-ldtk/assets/112954452/40269705-94cd-473d-a082-a4fb4ae89b1a)
4. Cliquez sur `Save As`
5. Fermez LDtk
6. Accédez le niveau exporté à partir de l'explorateur de fichiers de votre système d'exploitation
7. Double-cliquez sur le fichier LDtk de votre niveau pour le réouvrir à l'intérieur de l'éditeur LDtk
8. Accédez le menu *project settings*
9. Cliquez sur `Save Project`

Le niveau va dorénavant être correctement exporté.

### Nomenclature des fichiers et paramètres spécifique pour LDtk
Les fichiers exportées doivent être correctement nommés pour que l'outil fonctionne correctement. S'ils ne le sont pas, l'outil **NE FONCTIONNERA PAS**
- Le fichier contenant le *intgrid* pour les collisions: **Collisions.csv**
- Le fichier *JSON* contenant les données générales reliés au niveau: **data.json**
- Le fichier *composite* contenant toutes les couches en une seule image: **_composite.png**

Vos paramètres de projets pour LDtk doivent suivre ceux-ci. Sinon, l'outil d'importation pourrait ne pas fonctionner convenablement: 
- *Workspace settings*
  - *Default layer grid* = 16 px
  - *Default entity size* = 16 x 16 px

## L'importation de votre niveau LDtk

1. Ouvrez UE5
2. Accédez le dossier `Content` dans le *content browser*
3. Créez un nouveau dossier, appelé exactement comme ci-dessous:

```
LdtkFiles
```

4. Ouvrez le dossier nouvellement créé `LdtkFiles`
5. Créez un dossier pour votre niveau (Chaque nouveau niveau aura besoin d'un dossier séparé)

6. À partir de l'explorateur de fichier de votre système d'exploitation, ouvrez le dossier de votre niveau exporté
7. Accédez au dossier `simplified`

    - Gardez le ouvert, vous allez en avoir besoin plus tard

8. Prenez le dossier `simplified`, et déposez le dans le *content browser* de UE5, à l'intérieur du dossier `LdtkFiles/{VOTRE_NIVEAU}` ![Capture d’écran 2024-04-12 095954](https://github.com/cegepst/unreal-ldtk/assets/112954452/a9419e8d-bc77-4cbc-bcad-372d3761d671)
9. Un menu va ouvrir vous demandant des options pour l'importation de certains fichiers. Le choix n'importe peu, mais nous recommandons de choisir les options `Data table` et `CollisionEvent`, car nous savons qu'ils fonctionnent sans causer de problèmes
10. Importez tous les fichiers demandés
11. Lorsque fini, fermez UE5, et sélectionnez `Save Selected`
12. Accédez au dossier `LdtkFiles` à l'intérieur de l'explorateur de fichier de votre système d'exploitation
13. Accédez au dossier `simplified` original, provenant de votre niveau exporté, que vous avez gardez ouvert plus tôt
14. Ajouter le dossier au dossier `LdtkFiles/{VOTRE_NIVEAU}` du projet

    - **MacOS - IMPORTANT** Maintenez la touche Option et glissez le dossier dans le celui du projet. Cela va vous donner l'option de fusionner les dossiers, au lieu de remplacer les fichiers `.uasset` précédemment importés.
    - **Windows - IMPORTANT** Sur Windows, vous pouvez aussi prendre et déposer le dossier, mais vous risquez de perdre les fichiers exportés originaux, car ils seront transférés vers le projet UE5.

    - **Cela copie l'entièreté des fichiers originaux qui sont requis pour les calculs de notre script Python.** Si cette étape n'est pas suivie, notre script retournera une erreur, car il ne pourra pas trouver certain fichiers requis, comme par exemple `data.json`, `Collisions.csv`, etc.

15. Réouvrez UE5
16. Cliquez sur `Don't import` lorsque le message apparait au bas à droite de la page de l'éditeur
17. Accédez au dossier `Python` à l'intérieur du *content browser*
18. Faites un clique droit sur le *Editor Utility Widget* nommé `Main_Window`
19. Cliquez sur `Run Editor Utility Widget` ![Capture d’écran 2024-04-12 100307](https://github.com/cegepst/unreal-ldtk/assets/112954452/59577f77-423b-442a-b2a8-c54ae8ee0b47)
20. Écrivez le nom du dossier du niveau que vous voulez importer
21. Cliquez sur le bouton jaune `Importer`
22. Amusez-vous bien !



## Sources

- [Unreal Python API](https://docs.unrealengine.com/5.3/en-US/PythonAPI/)
- [Tutorial on how to setup UE5 with Unreal Engine](https://tuataragames.notion.site/Getting-started-with-Python-in-Unreal-Engine-5191d0a16b424d66b08b132d5764cefd)
- [Level Design toolkit (LDtk)](https://ldtk.io/)
