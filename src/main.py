from pathlib import Path
from PIL import Image
import config
import os


def relative_path(path:str = ""):
    return Path.joinpath(Path(os.path.abspath(os.path.dirname(__file__))).parent, path)


def out_function(image:Image.Image, var_name:str):
    out = ""
    length = 0
    image = image.convert('L')  # Conversion to grayscale
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pixel = image.getpixel((x,y))
            out += ('' if config.no_spaces else ' ') + '{' + f"{x},{y},{pixel}" + '}'\
                   + (('' if config.no_spaces else ' ') if x == image.size[0]-1 and y == image.size[1]-1 else ",")
            length += 1
    return f"const PROGMEM {config.type_name} {var_name}[] = " + '{' + out + "};\n" \
           f"const PROGMEM {'int' if length > 255 else 'uint8_t'} {var_name}_length = {length};"


if __name__ == "__main__":
    # Most formats supported by Pillow (as of 8.2.0)
    supported_file_formats = ("bmp", "dib", "eps", "gif", "icns", "ico", "im", "jpeg", "jpg", "msp", "pcx", "png", "ppm", "sgi", "tga", "tiff", "webp", "xbm", "blp", "cur", "dcx", "dds", "fli", "flc", "psd", "wal", "wmf", "xpm")

    code = []
    for file in os.listdir(relative_path("input")):
        if os.path.splitext(file)[1][1:].lower() in supported_file_formats:
            _var_name = os.path.splitext(os.path.basename(os.path.join(relative_path("input"), file)))[0]
            var_name = ""
            for i in _var_name:
                if i.isalnum(): var_name += i
                elif i == ' ':  var_name += '_'

            # Name config
            if config.name_camelCase:
                var_name = var_name[0].lower() + ''.join(line.capitalize() for line in var_name.split('_'))[1:]
            if config.name_lower:
                var_name = var_name.lower()

            with Image.open(os.path.join(relative_path("input"), file)) as img:
                code.append(out_function(img, var_name) + ('\n' if not config.multiple_files else ''))
            if config.multiple_files:
                for line in code:
                    file_extension = config.multiple_files_extension if config.multiple_files_extension[0] == '.' else f".{config.multiple_files_extension}"
                    with open(os.path.join(relative_path("output"), var_name + file_extension), 'w') as f:
                        f.write(line)
                        code.clear()
    if not config.multiple_files:
        with open(os.path.join(relative_path("output"), config.out_filename), 'w') as f:
            f.write('\n'.join(code))