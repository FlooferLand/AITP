# Arduino Image To Pixels (AITP)
Customizable Python program that converts images into C++ arrays.

### How to use (Default settings):
1. Put your image(s) into the `input` directory
2. Run `src/main.py` and every image in the `input` directory will be converted to a C/C++ header file `.h`
3. Move the header files into your Arduino project, `#include` the images you need, and loop trough the pixels in your image.

### Examples:
Struct used (defined in the Arduino script)
```arduino
struct Pixel {
  uint8_t m_x, m_y, m_color;
  uint8_t x()     const { return pgm_read_byte(&m_x);     }
  uint8_t y()     const { return pgm_read_byte(&m_y);     }
  uint8_t color() const { return pgm_read_byte(&m_color); }
};
```
```arduino
// AITP output:
const PROGMEM Pixel checkerPattern[] = { {0,0,255}, {1,0,0}, {0,1,0}, {1,1,255} };
const PROGMEM uint8_t checkerPattern_length = 4;
```
AITP outputs header files containing arrays of Pixel objects and their lengths by default.\
Allowing you to easily `#include` images in.

You may also want to change uint8_t to int if you have more than 256 LEDs, or if your LEDs are brighter than a stellar explosion.\
(LED brightness only goes from 0 to 255 so i wouldn't recommend you do that).

### How this works:
AITP goes through each pixel of your images using the Pillow Python module and gets the color of the pixel, gets the info it needs (such as the type it should use) from the config.py file, adds C++ code to a `code` variable, and writes the code to a file or to multiple files.
<br>
The actual program is a bit more complex but that's the gist of it.

### The future of this project
If a few people decide to use or contribute to this project i may add in more features in the future such as RGB colors, animation, storage optimizations, and image manipulation.

#### Report any issues in the <a href="https://github.com/flarfmatter/AITP/issues">Issues<a/> tab
