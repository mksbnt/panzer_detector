import multiprocessing
import time
import cv2
from multiprocessing import Pool
from src.constants.constants import BUFFER_VIDEO_DIR, OUTPUT_DIR
from src.services.frame_service import process_frame
from src.services.dir_service import replace_file, remove_file, get_file_path
from src.services.log_service import write_logs

# Define a function to write the processed video


def write_video(processed_file_name, fourcc, fps, width, height):
    out = cv2.VideoWriter(processed_file_name, fourcc, fps, (width, height))
    return out

# Define a wrapper function for the process_frame function


def process_frame_wrapper(args):
    return process_frame(*args)

# Define the main function to process the video


def process_video(input_file, templates, threshold):
    """
    This function processes a video file by reading each frame, processing it in parallel using the process_frame function, 
    and writing the processed frames to a new video file. The processed video is then saved to the output directory and the 
    original video file is deleted. The function also writes logs for each processed frame.
    """
    # Get the input file path and the processed file name
    input_file_path = get_file_path(input_file, BUFFER_VIDEO_DIR)
    processed_file_name = input_file_path.replace('.mp4', '_output.mp4')

    # Open the input file and get the necessary information
    cap = cv2.VideoCapture(input_file_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Write the processed video
    out = write_video(processed_file_name, fourcc, fps, width, height)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    start_time = time.time()
    frame_count = 0

    # Use multiprocessing to process the frames in parallel
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = []
        for frame_number in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break

            # Process the frame in parallel
            results.append(pool.apply_async(
                process_frame_wrapper, ((frame, templates, threshold),)))

        # Write the processed frames to the output video
        for result in results:
            processed_frame = result.get()
            out.write(processed_frame)
            frame_count += 1

            # Write logs for the processed frames
            write_logs(frame_number, total_frames, frame_count, start_time)

    # Release the input and output videos
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Replace the input file with the processed file
    replace_file(processed_file_name, OUTPUT_DIR)
    remove_file(input_file_path)
