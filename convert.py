import sys
import os
from pathlib import Path


def process_directory(input_dir, output_dir, visibility_dict):

    # private by default
    directory_public = False

    # inherit parent visibility
    parent_dir = str(Path(input_dir).parent.absolute())

    if parent_dir in visibility_dict:
        directory_public = visibility_dict[parent_dir]

    # check for dotfile to overwrite directory visibility
    if os.path.isfile(os.path.join(input_dir, ".public")) or os.path.isfile(os.path.join(input_dir, ".public.md")):
        directory_public = True
    if os.path.isfile(os.path.join(input_dir, ".private")) or os.path.isfile(os.path.join(input_dir, ".private.md")):
        directory_public = False

    visibility_dict[input_dir] = directory_public

    for file in os.listdir(input_dir):
        curr_file_path = os.path.join(input_dir, file)

        if os.path.isdir(curr_file_path):
            process_directory(curr_file_path, output_dir, visibility_dict)
            continue

        if not file.endswith(".md") or file.startswith("."):

            continue

        with open(curr_file_path, "r") as f:
            content = f.read().lstrip().replace("&nbsp;", " ")
            title_clean = file[:-3].replace("&", "and")

            if content.startswith("---\n") and len(content.split("---\n")) >= 3:  # yaml already there
                if "public: " in content.split("---\n")[1]:
                    if not content.split("public: ")[1].startswith("yes"):
                        continue
                elif not directory_public:
                    continue

                output = f'---\ntitle: "{title_clean}"\n{content[4:]}'
            else:
                if not directory_public:
                    continue

                output = f'---\ntitle: "{title_clean}"\n---\n{content}'

        with open(os.path.join(output_dir, file.replace("&", "and")), "w") as f:
            f.write(output)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid number of commandline parameters")
        exit(1)

    input_dir = os.path.join(os.getcwd(), sys.argv[1])
    output_dir = os.path.join(os.getcwd(), sys.argv[2])

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    else:
        for f in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, f))

    visibility_dict = dict()
    process_directory(input_dir, output_dir, visibility_dict)
