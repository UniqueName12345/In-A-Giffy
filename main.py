import argparse
import sys
import yaml
import os
import typing
import subprocess

# The below functions are related to the config file and ffmpeg path

def create_config_file() -> None:
    """
    Creates a config.yaml file if it doesn't exist.

    Args:
        None

    Returns:
        None
    """
    config_path: str = "config.yaml"
    if not os.path.exists(config_path):
        config: typing.Dict[str, str] = {"ffmpeg_path": ""}
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        print("Created config.yaml file.")
    else:
        print("config.yaml already exists.")

def lookup_ffmpeg_path() -> typing.Optional[str]:
    """
    This function looks up the path of the ffmpeg executable.

    Returns:
        Optional[str]: The path of the ffmpeg executable if found, else None.
    """
    with open("config.yaml", "r") as f:
        config: typing.Dict[str, typing.Any] = yaml.safe_load(f)
    if config.get("ffmpeg_path"):
        return config["ffmpeg_path"]
    for root, _, _ in os.walk("."):
        if "ffmpeg.exe" in os.listdir(root):
            return os.path.join(root, "ffmpeg.exe")
    return None


def set_ffmpeg_path(ffmpeg_path: str, config_path: str = "config.yaml") -> None:
    """
    Set the ffmpeg path in the config file.

    Args:
        ffmpeg_path (str): The path to ffmpeg.
        config_path (str, optional): The path to the config file. Defaults to "config.yaml".
    """
    with open(config_path, "r+") as f:
        config: typing.Dict[str, str] = yaml.safe_load(f)
        config["ffmpeg_path"] = ffmpeg_path
        f.seek(0)
        yaml.dump(config, f)
        f.truncate()

create_config_file()
ffmpeg_path = lookup_ffmpeg_path()
set_ffmpeg_path(ffmpeg_path)

# The two below functions are the meat and bones of the program
def convert_file(input_path: str, output_path: str, file_type: str) -> None:
    """
    Convert a file to the specified file type.

    Parameters:
        input_path (str): The path to the input file.
        output_path (str): The path to the output file.
        file_type (str): The type of file to convert to. Valid values are "mp4" or "gif".

    Returns:
        None
    """
    if ffmpeg_path is not None:
        if file_type == "mp4":
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
        elif file_type == "gif":
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
        else:
            raise ValueError("Invalid file type. Valid values are 'mp4' or 'gif'.")
        
        subprocess.run(command)


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
            output_path = input("Enter the output path (default: output/output.gif): ")
            convert_file(path, output_path, "gif")
            break
        elif choice.lower() == "gif":
            path = input("Enter the path to the GIF file: ")
            output_path = input("Enter the output path (default: output/output.mp4): ")
            convert_file(path, output_path, "mp4")
            break
        else:
            print("Invalid choice. Please enter 'mp4' or 'gif'.")



if __name__ == "__main__":
    main()
