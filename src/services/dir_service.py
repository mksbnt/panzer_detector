
import os
import cv2
import shutil
import subprocess
from src.constants.constants import BUFFER_VIDEO_DIR, INPUT_DIR


def get_input_templates(templates_dir):
    tank_template_files = [os.path.join(templates_dir, filename) for filename in os.listdir(templates_dir) if
                           filename.endswith('.png')]

    templates = [cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
                 for template_file in tank_template_files]

    return templates


def init_buffer(dirs):
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        if os.path.exists(directory):
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Failed to create directory '{directory}'.")
    fill_video_buffer()


def fill_video_buffer():
    input_video_files = get_input_files(INPUT_DIR, extension=('.mov', '.mp4'))

    for video in input_video_files:
        # Generate the output file name
        video_name = os.path.splitext(os.path.basename(video))[0]
        output_file = os.path.join(BUFFER_VIDEO_DIR, f"{video_name}.mp4")

        subprocess.run(['ffmpeg', '-i', video, '-qscale', '0', output_file])


def get_input_files(directory, extension='.mp4'):
    return [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(extension)]


def clear_buffer(dir):
    remove_folder(dir)


def remove_folder(folder_path):
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' has been removed.")
        except OSError as e:
            print(f"Error: {e}")
    else:
        print(f"Folder '{folder_path}' does not exist.")


def replace_file(source_file, destination_dir):
    try:
        destination_file = os.path.join(
            destination_dir, os.path.basename(source_file))
        shutil.copy2(source_file, destination_file)
        os.remove(source_file)
        print(f"Replaced file: {source_file} -> {destination_file}")
    except Exception as e:
        print(f"Failed to replace file: {source_file}, Error: {e}")


def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {e}")


def get_file_path(input_file, file_dir):
    return os.path.join(
        file_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}.mp4")
