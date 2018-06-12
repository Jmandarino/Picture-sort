# python 3.6
import argparse
import calendar
import datetime
import os
import shutil
from queue import Queue

import exifread


def create_folder_and_move(output_directory, current_directory, filename):
    """
    for a given file creates appropriate folders for it and moves the file
    :param output_directory: Base directory where the file is going
    :param current_directory: the base directory where the file is currently located
    :param filename: the name of the file in the 'current_directory'
    :return:
    """
    f = open(os.path.join(current_directory, filename), 'rb')
    date = exifread.process_file(f, stop_tag='DateTimeOriginal', details=False)['EXIF DateTimeOriginal'] # https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif/datetimeoriginal.html
    f.close()
    # date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(current_directory, filename)))
    date = datetime.datetime.strptime(date.values, '%Y:%m:%d %H:%M:%S')
    # path's for file
    year_folder = os.path.join(output_directory, str(date.year))
    month_folder = os.path.join(year_folder, '{} - {}'.format(date.month, calendar.month_name[date.month]))
    day_folder = os.path.join(month_folder, str(date.day))

    try:
        os.makedirs(year_folder, exist_ok=True)
        os.makedirs(month_folder, exist_ok=True)
        os.makedirs(day_folder, exist_ok=True)
        shutil.move(os.path.join(current_directory, filename), os.path.join(day_folder, filename))
    except OSError as e:
        print('Could not make appropriate folders for {} ERROR:{}'.format(filename, e.strerror))


if __name__ == '__main__':
    # constants
    FILES_TO_MOVE = ['.arw', '.jpg']
    FOLDER_EXCEPTIONS = ['edited', 'output', '.idea', 'venv', 'export', ]
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    OUTPUT_FOLDER = os.path.join(CURRENT_DIR, 'output')

    parser = argparse.ArgumentParser(description='this program sorts images into proper folders')
    parser.add_argument('-p', '--path', nargs=None, dest='path', help='path to start this script from')

    args = parser.parse_args()
    if args.path:
        CURRENT_DIR = args.path

    # folder queue for BFS
    folder_queue = Queue()
    # we want to ignore the output_dir
    files = os.listdir(CURRENT_DIR)

    # make the output directory
    if not os.path.exists(OUTPUT_FOLDER):
        try:
            os.makedirs(OUTPUT_FOLDER)
        except OSError:
            print('Can\'t create directory in path: {}'.format(OUTPUT_FOLDER))

    # process current directory
    for file in files:
        # add file to queue
        if os.path.isdir(file) and file not in FOLDER_EXCEPTIONS:
            folder_queue.put((file, os.path.realpath(file)))
        # process file and move it
        ext = os.path.splitext(file)[-1].lower()
        if ext in FILES_TO_MOVE:
            create_folder_and_move(OUTPUT_FOLDER, CURRENT_DIR, file)

    # BFS traversal
    visited_folders = {}  # keep track of folders that have been processed
    while not folder_queue.empty():
        # pop folder and process
        folder_tup = folder_queue.get()
        visited_folders[folder_tup[1]] = 1

        files = os.listdir(folder_tup[1])
        # process files in directory we popped of the queue
        for file in files:
            if file == folder_tup[1]:
                continue
            file_path = os.path.realpath(folder_tup[1])  # the parent directory of 'file'
            # if the file is a dir and we haven't visited it yet add it to the queue
            if os.path.isdir(os.path.join(file_path, file)) and file.lower() not in FOLDER_EXCEPTIONS and \
                    visited_folders.get(os.path.join(file_path, file), None) is None:
                folder_queue.put((file, os.path.join(file_path, file)))
                continue
            ext = os.path.splitext(file)[-1].lower()
            if ext in FILES_TO_MOVE:
                create_folder_and_move(OUTPUT_FOLDER, file_path, file)
