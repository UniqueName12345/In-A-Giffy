# In A Giffy

**In A Giffy** is a Python CLI tool that uses FFmpeg to convert between MP4 and GIF.

## Note
In A Giffy does not come with FFmpeg pre-installed. You can download the build from the FFmpeg-build repository: https://github.com/absolllute/ffmpeg-build. This repository is mainly for Geometry Dash, but the build should work for all use cases.

Alternatively, you can simply run `python main.py -s` to be prompted for the custom FFmpeg.exe path. By default, In A Giffy will choose the current repository.

An automatic FFmpeg installer is under development, but it will be released in a separate repository as it is not specific to In A Giffy.

## Running

Firstly, you need to install the dependencies.

```
pip install -r requirements.txt
```

Then, you can run the program.

```
python main.py
```

The program will ask if you want to convert from MP4 to GIF or GIF to MP4. Then you can just follow the instructions. The output will be saved in the same directory as the input file.