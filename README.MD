# About:

Picture sort is a way to organize your photo library. 

This program works by sorting all your pictures by the EXIF data associated with them.
It runs BFS to find all images in the current directory as well as all subdirectories. 

to get started run `pip install -r requirements.txt`

## Usage:

This can be run in the directory/sub directories you would like to organize, or you can reference the directory you 
would like to start in.

usages:
`python main.py` \
`python main.py -h` \
`python main.py -p c:\Users` \
`python main.py --path c:\Users`
 
 
 #### Important variables:
 `FILES_TO_MOVE = ['.arw', '.jpg']` a list of files that will be moved \
 `FOLDER_EXCEPTIONS = ['edited', 'output', '.idea', 'venv', 'export', ]` a list of folders (and contents) that will not 
 be processed. Note these folders are checked for at every level \
 `OUTPUT_FOLDER = ...` this is where the all the images will be moved. 
 
 
 ### warning:
 
 Before running make sure you want to move **ALL** files in your current directory and subdirectories.
 
 
 ## input/output
 
 Example file output:
```
├───2017
│   ├───11 - November
│   │   └───5
│   ├───3 - March
│   │   ├───18
│   │   ├───19
│   │   ├───20
│   │   └───21
│   ├───4 - April
│   │   ├───14
│   │   ├───15
│   │   └───9
│   ├───5 - May
│   │   └───7
│   ├───6 - June
│   │   └───12
│   ├───7 - July
│   │   ├───3
│   │   └───4
│   └───8 - August
│       └───21
└───2018
    ├───4 - April
    │   └───22
    ├───5 - May
    │   ├───27
    │   └───28
    └───6 - June
        └───8
```

The file structure is assigned in `create_folder_and_move`

to simplify:

```
C:.
└───2018
    └───1 - January
        └───30

```