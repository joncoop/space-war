import os
import platform

platform = platform.system()

if platform == 'Linux':
    folder_name = os.path.expanduser('~/.spacewar/')
    file_name = 'scores.txt'
elif platform == 'Windows':
    folder_name = os.path.expanduser('~\\AppData\\Local\\Space War\\')
    file_name = 'scores.txt'


def read_high_score():
    full_path = folder_name + file_name

    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            score = int(f.read())
    else:
        score = 0

    return int(score)


def save_high_score(score):
    full_path = folder_name + file_name

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    with open(full_path, 'w') as f:
        f.write(str(score))
