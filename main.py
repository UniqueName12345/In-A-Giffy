import argparse
import sys
import yaml
import os

# Create a config.yaml file
# The config.yaml file should contain the following:
# - ffmpeg.exe path
def create_config_file():
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        config = {"ffmpeg_path": ""}
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        print("Created config.yaml file.")
    else:
        print("config.yaml already exists.")
def lookup_ffmpeg_path():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    if config.get("ffmpeg_path"):
        return config["ffmpeg_path"]
    for root, _, _ in os.walk("."):
        if "ffmpeg.exe" in os.listdir(root):
            return os.path.join(root, "ffmpeg.exe")
    return None

ffmpeg_path = lookup_ffmpeg_path()

# The two below functions are the meat and bones of the program
import subprocess

def gif_to_mp4(input_path, output_path="output/output.mp4"):
    if ffmpeg_path is not None:
        command = [
            ffmpeg_path,
            '-i',
            input_path,
            '-vf',
            'scale=trunc(iw/2)*2:trunc(ih/2)*2',
            '-c:v',
            'libx264',
            '-preset',
            'ultrafast',
            '-crf',
            '30',
            '-c:a',
            'copy',
            output_path
        ]
        subprocess.run(command)

def mp4_to_gif(input_path, output_path="output/output.gif"):
    if ffmpeg_path is not None:
        command = [
            ffmpeg_path,
            "-y",
            "-ss",
            "30",
            "-t",
            "3",
            "-i",
            input_path,
            "-vf",
            "fps=10,scale=320:-1:flags=lanczos",
            "-loop",
            "0",
            "-i",
            input_path,
            "-filter_complex",
            "fps=10,scale=320:-1:flags=lanczos[x];[x]split[x1][x2];[x1]palettegen[p];[x2][p]paletteuse",
            output_path
        ]
        subprocess.run(command)
create_config_file()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true", help="Specify custom ffmpeg.exe path")
    args = parser.parse_args()

    if args.s:
        custom_ffmpeg_path = input("Please enter the custom ffmpeg.exe path: ")
        with open("config.yaml", "w") as f:
            yaml.dump({"ffmpeg_path": custom_ffmpeg_path}, f)

    while True:
        choice = input("Do you want to convert MP4 to GIF or GIF to MP4? (mp4/gif): ")
        if choice.lower() == "mp4":
            path = input("Enter the path to the MP4 file: ")
            mp4_to_gif(path)
            break
        elif choice.lower() == "gif":
            path = input("Enter the path to the GIF file: ")
            gif_to_mp4(path)
            break
        else:
            print("Invalid choice. Please enter 'mp4' or 'gif'.")



if __name__ == "__main__":
    main()
