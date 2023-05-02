import glob
import re
import os

from typing import List


def write_to_file(content: str, output_file_path: str):
    with open(output_file_path, 'w') as output_file:
        output_file.write(content + '\n')
    print(f"Saved to {output_file_path}")


def get_nxt_output_idx(glob_folder: str, glob_key: str, idx_re_pattern: int):
    idx = -1
    for filename in glob.glob(f"{glob_folder}/*{glob_key}*"):
        m = re.search(idx_re_pattern, filename)
        if m:
            idx = max(idx, int(m.group(1)))
    return idx + 1


def get_nxt_desc_output_idx(glob_folder: str, desc_txt_key: str):
    return get_nxt_output_idx(glob_folder, desc_txt_key,
                              ".*/.*_(\d+)_desc.txt")


def create_folder_if_not_exits(folder_path_list: List[str]):
    for folder_path in folder_path_list:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


def setup_desc_audio_output_folder(base_dir: str):
    # always have these 2 folders as audio/text description generation pipeline
    output_dirs = [f"{base_dir}/audio", f"{base_dir}/desc"]
    create_folder_if_not_exits(output_dirs)
    return output_dirs


def gen_desc_audio_output_filename(base_dir: str, filename_key: str):
    # as you are creating multiple (audio, desc) based on a given input ...
    # function create the expected name for the file for you.
    # (Basically finding the correct index suffix for the filename_key)
    audio_folder, desc_folder = setup_desc_audio_output_folder(base_dir)
    idx = get_nxt_desc_output_idx(base_dir, filename_key)
    return f"{audio_folder}/{filename_key}_{idx}_sentence.mp3",\
           f"{desc_folder}/{filename_key}_{idx}_desc.txt"
