from multiprocessing import freeze_support
from src.constants.constants import TEMPLATES_DIR, THRESHOLD, BUFFER_DIRS, BUFFER_VIDEO_DIR, BUFFER_DIR
from src.services.dir_service import get_input_templates, get_input_files, init_buffer, clear_buffer
from src.services.video_service import process_video


def main():
    init_buffer(BUFFER_DIRS)

    input_files = get_input_files(BUFFER_VIDEO_DIR)
    templates = get_input_templates(TEMPLATES_DIR)

    for input_file in input_files:
        process_video(input_file, templates, THRESHOLD)

    clear_buffer(BUFFER_DIR)


if __name__ == "__main__":
    freeze_support()
    main()
