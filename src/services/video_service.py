import multiprocessing
import time
from multiprocessing import Pool
import cv2
from src.constants.constants import BUFFER_VIDEO_DIR, OUTPUT_DIR
from src.services.frame_service import process_frame
from src.services.log_service import write_logs
from src.services.dir_service import replace_file, remove_file, get_file_path


def write_video(processed_file_name, fourcc, fps, width, height):
    out = cv2.VideoWriter(processed_file_name, fourcc, fps, (width, height))
    return out


def process_frame_wrapper(args):
    return process_frame(*args)


def process_video(input_file, templates, threshold):
    input_file_path = get_file_path(input_file, BUFFER_VIDEO_DIR)
    processed_file_name = input_file_path.replace('.mp4', '_output.mp4')
    cap = cv2.VideoCapture(input_file_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = write_video(processed_file_name, fourcc, fps, width, height)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    start_time = time.time()

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        for frame_number in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = pool.apply(
                process_frame_wrapper, ((frame, templates, threshold),))
            out.write(processed_frame)
            frame_count = frame_number + 1
            write_logs(frame_number, total_frames, frame_count, start_time)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    replace_file(processed_file_name, OUTPUT_DIR)
    remove_file(input_file_path)
