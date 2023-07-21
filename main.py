from PIL import Image


def lerp(
    from_range_start: int,
    from_range_stop: int,
    to_range_start: int,
    to_range_stop: int,
    value: int,
):
    percent = value / (from_range_stop - from_range_start)
    return percent * (to_range_stop - to_range_start)


def get_image_brightness(path_to_img: str):
    with Image.open(path_to_img) as image:
        width, height = image.size
        data = list(image.getdata())
        pixels: list[list[float]] = []
        for y in range(height):
            pixels.append([])
            for x in range(width):
                pixel = data[(y * width) + x]
                pixels[y].append(get_pixel_brightness(pixel))
    return pixels, image.size


def get_pixel_brightness(pixel: tuple[int, int, int, int]):
    if isinstance(pixel, int):
        return pixel
    return (pixel[0] + pixel[1] + pixel[2]) / 3


def resize_image(
    start_image_width: int,
    start_image_height: int,
    end_image_width: int,
    end_image_height: int,
    image: list[list[float]],
):
    if 0 in (end_image_width, end_image_height):
        print("Invalid parameters")
        return image
    if end_image_height >= start_image_height or end_image_width >= start_image_width:
        print("Cannot increase image size")
        return image
    new_image: list[list[float]] = []
    x_range = int(start_image_width / end_image_width)
    y_range = int(start_image_height / end_image_height)
    y_chunk_range = range(int(len(image) / y_range))
    x_chunk_range = range(int(len(image[0]) / x_range))
    for y_chunk in y_chunk_range:
        new_image.append([])
        for x_chunk in x_chunk_range:
            value: float = 0
            count: int = 0
            for y in range(y_range * y_chunk, y_range * (y_chunk + 1)):
                for x in range(x_range * x_chunk, x_range * (x_chunk + 1)):
                    value += image[y][x]
                    count += 1
            new_image[y_chunk].append(value / count)
    return new_image


def scale_image(
    start_image_width: int,
    start_image_height: int,
    scale: float,
    image: list[list[float]],
):
    end_image_width = start_image_width * scale
    end_image_height = start_image_height * scale
    return resize_image(
        start_image_width, start_image_height, end_image_width, end_image_height, image
    )


def get_ascii(pixel: float, reverse: bool = False):
    brightness_map = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
    # "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. "
    if reverse:
        brightness_map = "".join(reversed(brightness_map))
    return f"{brightness_map[int(lerp(0, 255, 0, len(brightness_map) - 1, pixel))]} "


def main():
    INPUT_FILE_NAME = "aperature.png"
    pixels, SIZE = get_image_brightness(INPUT_FILE_NAME)
    IMG_W, IMG_H = SIZE
    OUTPUT_FILE_NAME = "output.txt"

    # pixels = resize_image(IMG_W, IMG_H, 119, 53, pixels)
    pixels = scale_image(IMG_W, IMG_H, 1, pixels)

    with open(OUTPUT_FILE_NAME, "w") as output_file:
        for row in pixels:
            line: str = ""
            for pixel in row:
                line += get_ascii(pixel, reverse=True)

            output_file.write(f"{line}\n")


main()
