| Language | Documentation |
|----------|---------------|
| EN       | [Documentation (EN)](#documentation-en) |
| FR       | [Documentation (FR)](#documentation-fr) |





## Documentation (EN)

### Description

TODO: Add project description...

### Setup and Usage guide

#### Dependencies

- Python (included within UE5)
- Unreal Python API (Already installed)

#### Creating project and enabling Python editor scripting

1. Create a new UE5 project, using the *blank template*
2. Navigate to `Edit > Plugins`
3. Make sure *Python Editor Scripting* is enabled
4. Navigate to `Edit > Editor Preferences > Python`
5. Enable the following: 

    - *Dev Mode*
    - *Content Browser Integration*

6. Restart UE5

#### Add the importer to your project

1. Locate the newly created Python folder inside of the editor's Content Browser
2. Create an empty folder inside of it

    - **This is important**, as it will not show in the operating system's content browser until there is content inside of it.

3. Download the project as a zip file
4. Extract the content
5. Open your projects Python folder inside of your operating system's file browser
7. Open the extracted files, and access the directory in which the python scripts and the widgets are contained (The files inside `unreal-ldtk-main`)
8. Drag and drop the extracted files (not the main folder, but the files within) into the Python folder
9. Restart UE5

## Exporting your LDtk level correctly

To correctly export your LDtk level for usage with our tool, you will need to use the *Super Simple Export* feature. As of writing this, this feature has a bug impacting the export of the files. We found a workaround for this, and opened an issue describing the bug (https://github.com/deepnight/ldtk/issues/1095)

The following steps account for the required workaround :

1. Open your LDtk level inside of the LDtk editor
2. Access the project settings menu
3. Enable Super Simple Export
4. Click `Save As`
5. Close LDtk
6. Access your exported level inside of your operating system's file browser
7. Double-click on the LDtk file to reopen the level inside of the editor
8. Access the project settings menu
9. Click `Save Project`

The level will now correctly export

## Importing your exported LDtk level 

1. Open the UE5 editor
2. Access the `Content` directory in the content browser
3. Create a new folder, called exactly like the following:

```
LdtkFiles
```

4. Open the newly created `LdtkFiles` folder

5. Inside of your operating system's file browser, access your exported level
6. Access the `simplified` folder

    - Keep it open, you'll need it later

7. Take the `simplified` folder, and drop it inside of UE5's content browser, inside of the `LdtkFiles` folder
8. A menu will open asking to import. The selected option does not matter, but we recommend selecting `Data table` and `CollisionEvent` for the options, as we know they do not cause any issues
9. Import all of the prompted imports
10. When done, close UE5, and select `Save Selected`
11. Access the `LdtkFiles` folder inside of your operating system's file browser
12. Access the original `simplified` folder from your exported level, which you kept open earlier.
13. Copy and Paste it into the UE5 project's `LdtkFiles` folder.

    - **This copies over all the original files that are required for calculations by our Python script.** If not done, the script will return errors because it could not find the required files, like for example `data.json`, `Collisions.csv`, etc.

    - You can also drag and drop the files, but you will likely lose the original files from the export inside of the original directory, because they will be transferred over to the UE5 project.

14. Reopen UE5
15. Click `Don't import` on the prompt at the bottom left of the screen when the editor opens
16. Access the `Python` folder inside of the content browser
17. Right-click on the `Main_Window` Editor Utility Widget
18. Click on `Run Editor Utility Widget`
19. Click on the yellow `Import` button
20. Enjoy !





## Documentation (FR)

### Description

TODO: Add project description...

### Guide d'installation et d'utilisation

#### Dépendances

- Python (inclus avec UE5)
- Unreal Python API (Préinstallé)

#### Création du projet et activation de Python Editor Scripting

1. Il faut premièrement créer un nouveau projet, en utilisant le *template Blank*
2. Naviguer vers `Edit > Plugins`
3. Assurez-vous que *Python Editor Scripting* est activé
4. Naviguer vers `Edit > Editor Preferences > Python`
5. Activer les options ci-dessous: 
    - Dev Mode
    - Content Browser Integration
6. Redémarrer UE5

#### Ajouter l'importeur à votre projet

1. Trouvez le dossier nouvellement créé, nommé Python, dans le *Content Browser* de l'éditeur
2. Créez un dossier vide à l'intérieur

    - **Ceci est important**, car sinon, le dossier ne s'affichera pas à l'intérieur de l'explorateur de fichier de votre système d'exploitation.

3. Téléchargez le projet en fichier zip
4. Extraire le contenu du zip
5. Ouvrez le dossier Python du projet à l'intérieur de l'explorateur de fichier de votre système d'exploitation
7. Ouvrez les fichiers extraits, et accédez au dossier dans lequel le script Python et le widget sont entreposés. (Les fichiers dans `unreal-ldtk-main`)
8. Prenez et déposez les fichiers extraits (pas le dossier principal, mais les fichiers à l'intérieur) dans le dossier Python
9. Redémarrez UE5

## L'exportation de votre niveau LDtk

Pour correctement exporter votre niveau LDtk pour l'utiliser avec notre outil, il faut utiliser la fonctionnalité *Super Simple Export*. Au moment de l'écriture, cette fonctionnalité contient un bug qui impact l'exportation des fichiers. Nous avons trouvé une solution temporaire au problème, et nous avons ouvert une *issue*, décrivant le bug:
(https://github.com/deepnight/ldtk/issues/1095)

Les étapes ci-dessous prennent en compte notre solution temporaire :

1. Ouvrez votre niveau Ldtk à l'intérieur de l'éditeur LDtk
2. Accédez le menu *project settings*
3. Activez *Super Simple Export*
4. Cliquez sur `Save As`
5. Fermez LDtk
6. Accédez le niveau exporté à partir de l'explorateur de fichiers de votre système d'exploitation
7. Double-cliquez sur le fichier LDtk de votre niveau pour le réouvrir à l'intérieur de l'éditeur LDtk
8. Accédez le menu *project settings*
9. Cliquez sur `Save Project`

Le niveau va dorénavant être correctement exporté.

## L'importation de votre niveau LDtk

1. Ouvrez UE5
2. Accédez le dossier `Content` dans le *content browser*
3. Créez un nouveau dossier, appelé exactement comme ci-dessous:

```
LdtkFiles
```

4. Ouvrez le dossier nouvellement créé `LdtkFiles`

5. À partir de l'explorateur de fichier de votre système d'exploitation, ouvrez le dossier de votre niveau exporté
6. Accédez au dossier `simplified`

    - Gardez le ouvert, vous allez en avoir besoin plus tard

7. Prenez le dossier `simplified`, et déposez le dans le *content browser* de UE5, à l'intérieur du dossier `LdtkFiles`
8. Un menu va ouvrir vous demandant des options pour l'importation de certains fichiers. Le choix n'importe peu, mais nous recommandons de choisir les options `Data table` et `CollisionEvent`, car nous savons qu'ils fonctionnent sans causer de problèmes
9. Importez tous les fichiers demandés
10. Lorsque fini, fermez UE5, et sélectionnez `Save Selected`
11. Accédez au dossier `LdtkFiles` à l'intérieur de l'explorateur de fichier de votre système d'exploitation
12. Accédez au dossier `simplified` original, provenant de votre niveau exporté, que vous avez gardez ouvert plus tôt
13. Copiez et collez le à l'intérieur de dossier `LdtkFiles` du projet

    - **Cela copie l'entièreté des fichiers originaux qui sont requis pour les calculs de notre script Python.** Si cette étape n'est pas suivie, notre script retournera une erreur, car il ne pourra pas trouver certain fichiers requis, comme par exemple `data.json`, `Collisions.csv`, etc.

    - Vous pouvez aussi prendre et déposer les fichiers, mais vous risquez de perdre les fichiers exportés originaux, car ils seront transférés vers le projet UE5.

14. Réouvrez UE5
15. Cliquez sur `Don't import` lorsque le message apparait au bas à droite de la page de l'éditeur
16. Accédez au dossier `Python` à l'intérieur du *content browser*
17. Faites un clique droit sur le *Editor Utility Widget* nommé `Main_Window`
18. Cliquez sur `Run Editor Utility Widget`
19. Cliquez sur le bouton jaune `Importer`
20. Amusez-vous bien avec votre nouveau dans UE5 !



## Sources

- [Unreal Python API](https://docs.unrealengine.com/5.3/en-US/PythonAPI/)
- [Tutorial on how to setup UE5 with Unreal Engine](https://tuataragames.notion.site/Getting-started-with-Python-in-Unreal-Engine-5191d0a16b424d66b08b132d5764cefd)
- [Level Design toolkit (LDtk)](https://ldtk.io/)
