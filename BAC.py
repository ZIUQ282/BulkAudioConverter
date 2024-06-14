import os
import sys
import ffmpeg
from tqdm import tqdm


ffmpeg_audio_codecs = {
    'mp3': 'libmp3lame',            # MP3
    'aac': 'aac',                   # AAC
    'wav': 'pcm_s16le',             # WAV
    'flac': 'flac',                 # FLAC
    'ogg': 'libvorbis',             # Ogg Vorbis
    'm4a': 'aac',                   # M4A (typically AAC)
    'wma': 'wmav2',                 # WMA
    'opus': 'libopus',              # Opus
    'aiff': 'pcm_s16be',            # AIFF
    'amr': 'libopencore_amrnb',     # AMR
    'alac': 'alac',                 # ALAC
    '*': ''                         # wildcard for all files
}


def main():

    inputformat = outputformat = delagree = ""

    print("List of supported audio files: ")
    for key, val in ffmpeg_audio_codecs:
        print("."+key)

    # input files extension
    while inputformat not in ffmpeg_audio_codecs.keys():
        inputformat = str(
            input("Files with what extension do you wish to convert? (using * will convert all files in the directory) ")).strip('.')

    # output extension
    while outputformat not in ffmpeg_audio_codecs.keys() - {'*'}:
        outputformat = str(input(
            "What should be the output files extension do you wish to convert to? ")).strip('.')

    # delete files after conversion
    while delagree.lower() not in ["y", "n"]:
        delagree = str(input(
            "Do you want to delete original files after conversion? This action is irreversible! (y/n) ")).lower()

    delagree = True if delagree == "y" else False

    # path to this file
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # detecting files in the directory
    audiofiles = detect_files(folder_path)

    # filter out files without given extension
    audiofiles = filter_files(audiofiles, inputformat)

    # convert files with given extension
    if inputformat != "*":
        for inp in tqdm(audiofiles, desc="Converting files", dynamic_ncols=True):
            out = inp.replace(inputformat, outputformat)
            convert_audio(inp, out, delagree,
                          ffmpeg_audio_codecs[outputformat])

    # convert all files
    else:
        for inp in tqdm(audiofiles, desc="Converting files", dynamic_ncols=True):
            inputformat = inp.split('.')[-1]
            out = inp.replace(inputformat, outputformat)
            convert_audio(inp, out, delagree,
                          ffmpeg_audio_codecs[outputformat])

    return 0


def detect_files(folder_path):
    try:
        # check if the given path is a folder
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"{folder_path} is not a directory.")

        # iterate through the paths in a folder and add to the list
        files = list()
        for filename in os.listdir(folder_path):
            files.append(os.path.join(folder_path, filename))

        # filter out paths which are not files
        files = [file for file in files if os.path.isfile(file)]

        return files

    except Exception as e:
        print(f"An error occurred: {e}")


def filter_files(files, extension):
    filtered_files = list()
    try:
        # filtering files with a given extension
        if extension != "*":
            filtered_files = [
                file for file in files if file.endswith(f".{extension}")]
        # filtering all files when input extension is *
        else:
            for f in files:
                extension = f.split('.')[-1]
                if extension in ffmpeg_audio_codecs.keys():
                    filtered_files.append(f)
        return filtered_files

    except Exception as e:
        print(f"An error occurred: {e}")


def convert_audio(input_file, output_file, delete, codec):
    try:
        # converting audio files using ffmpeg
        (
            ffmpeg
            .input(input_file)
            .output(output_file, acodec=codec)
            .run(overwrite_output=True, quiet=True)
        )

        # removing original files after conversion
        if delete:
            print(f"Removing {input_file}...")
            os.remove(input_file)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    sys.exit(main())
