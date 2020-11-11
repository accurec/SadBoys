# SadBoys
### Overview
This is a fun project done in [Python](https://www.python.org/). The goal of this project is to compile nostalgic/sad type of videos from the video and music inputs that the user chooses. The ideal output would be something like [this video](https://www.youtube.com/watch?v=cFpekJ5h1XY&list=RDC02WOL9lLx8&index=4) or [this one](https://www.youtube.com/watch?v=M9Y2p5l6IWU&list=RDC02WOL9lLx8&index=36). There are quite a lot of videos like that on YouTube and apparently they are quite popular having millions of views :) The project was very much inspired by the following [YouTube video](https://www.youtube.com/watch?v=EmZX9fgHoYk).
Now I am not saying that I'm a sad person, I simply found the idea quite entertaining and wanted to try coding the program myself using Python and explore a little bit of its capabilities as well as get familiar with Visual Studio Code IDE :)

### Program execution flow
The general flow of the program is to take 

### Installation/Setup
Components needed for the project to work:
1) MoviePy -> can be installed by using the folloiwng command:

    ```sh 
    pip install moviepy
    ```
    
2) [ImageMagick](https://imagemagick.org/)
3) _Optional_
Potentially you would need to configure Python to point to the proper ImageMagick .exe location. The config file to do this should be located in the following folder:

    ```{PathToPythonOnYourComputer}\Lib\site-packages\moviepy\config_defaults.py```

    In that file you would need to replace the path in the following line with the path on your computer:
    
    ```IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'C:\\Program Files\\ImageMagick-7.0.10-Q16-HDRI\\magick.exe')```

### Project components
The ```root``` folder contains the main executable script __SadBoysCompiler__ that has all code of the project.
The ```assets``` folder include folders that contain files as follows:

- ```music``` -> 
- ```overlayPics``` -> 
- ```overlayVids``` -> 
- ```overlayWords``` -> 
- ```vids``` -> 

The ```output``` folder contains compiled video examples of the program execution (as of right now these are just first program iteration passes :smiley:). If user chose to do so then the subsequent compiled videos would go into the same folder.

### SadBoysCompiler code components
```Sequence``` class
```InputAgent``` class
```SequenceManager``` class
```WordsGenerator``` class
```VideoCreator``` class

### Lessons learned
Working on this project allowed me to code in Python using external video processing library, explore its capabilities and have a glimpse of what it has to offer. In addition to that I also used Visual Studio Code IDE and got familiar with it as well as explored how to use different extensions for it and debug a Python program.

### Future improvements