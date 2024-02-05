"""
Course: CSE 251 
Lesson: L03 Prove
File:   prove.py
Author: <Add name here>

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment.
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment.
- Do not forget to complete any TODO comments.
"""

from matplotlib.pylab import plt  # load plot library
from setup import setup as ensure_assignment_is_setup
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4

# TODO Your final video needs to have 300 processed frames.
# However, while you are testing your code, set this much lower!
FRAME_COUNT = 300

# RGB values for reference
RED = 0
GREEN = 1
BLUE = 2

def create_new_frame(args):
    """"
    Creates a new image file from image_file and green_file.

    Parameters:
        args (tuple): Tuple containing (image_file, green_file, process_file)
    """
    image_file, green_file, process_file = args

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)

def process_frames_with_pool(cpu_count):
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []

    # all_process_time = timeit.default_timer()

    pool = mp.Pool(processes=cpu_count)
    
    # Generate the list of arguments for create_new_frame function
    args_list = [(f'elephant/image{i:03d}.png', f'green/image{i:03d}.png', f'processed/image{i:03d}.png') for i in range(1, FRAME_COUNT + 1)]

    start_time = timeit.default_timer()

    # Use pool.map() to process frames in parallel
    pool.map(create_new_frame, args_list)

    total_time = timeit.default_timer() - start_time

    xaxis_cpus.append(cpu_count)
    yaxis_times.append(total_time)

    # Log the total time this took
    log.write(f'Total Time for {cpu_count} CPU Cores: {total_time} seconds.')
    print()

    pool.close()
    pool.join()

    return xaxis_cpus, yaxis_times

def main():
    xaxis_cpus_all = []
    yaxis_times_all = []

    log = Log(show_terminal=True)

    # Process frames for each CPU core count from 1 to CPU_COUNT
    for cpu_count in range(1, CPU_COUNT + 1):
        xaxis_cpus, yaxis_times = process_frames_with_pool(cpu_count)
        xaxis_cpus_all.extend(xaxis_cpus)
        yaxis_times_all.extend(yaxis_times)

    # Calculate and print the total time
    total_time = sum(yaxis_times_all)
    log.write(f'Total Time for ALL PROCESSES: {total_time} seconds.')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus_all, yaxis_times_all, label=f'{FRAME_COUNT}')

    plt.title('CPU Core Times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()

if __name__ == "__main__":
    ensure_assignment_is_setup()
    main()
