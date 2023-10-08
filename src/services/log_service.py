# TODO Use logging https://docs.python.org/3/howto/logging.html
import time


def print_logs_to_console(progress, elapsed, fps):
    print(f"Processed {progress}\
    Time elapsed: {elapsed}\
    Frames per second: {fps}", end='\r')


def write_logs_to_file(number, total, current_data_time, progress, elapsed, fps):
    with open('logs.txt', 'a') as f:
        if is_first_frame(number):
            f.write("\n")
            f.write(f"Process started in {current_data_time}")
            f.write("\n")

        f.write(f"Processed {progress} ")
        f.write(f"Time elapsed: {elapsed} ")
        f.write(f"Frames per second: {fps}")
        f.write("\n")

        if is_last_frame(number, total):
            f.write(f"Process ended in {current_data_time}")
            f.write("\n")
            f.write("\n")


def get_current_time_utc():
    return time.gmtime()


def is_first_frame(number):
    return number == 0


def is_last_frame(number, total):
    return number == total - 1


def calculate_progress(count, total):
    try:
        progress = (count / total) * 100
    except ZeroDivisionError:
        progress = 0
    return progress


def write_logs(frame_number, total_frames, frame_count, start_time):
    progress = calculate_progress(frame_count, total_frames)
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time
    elapsed_time_formatted = time.strftime(
        '%H:%M:%S', time.gmtime(elapsed_time))
    progress_formatted = f"{progress: .2f}%"
    fps_formatted = f"{fps: .2f}"
    current_data_time_formatted = time.strftime(
        '%m/%d/%Y %H:%M:%S', get_current_time_utc())

    print_logs_to_console(progress_formatted,
                          elapsed_time_formatted, fps_formatted)

    write_logs_to_file(frame_number, total_frames, current_data_time_formatted, progress_formatted,
                       elapsed_time_formatted, fps_formatted)
