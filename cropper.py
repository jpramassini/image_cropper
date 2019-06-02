import os
from PIL import Image, ImageChops, ImageOps
from PIL import Image


def calculate_aspect(width: int, height: int):
    return width / height


def crop(im, fit_ratio):
    img_width, img_height = im.size
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()

    if bbox:
        crop_height = bbox[3] - bbox[1]
        crop_width = bbox[2] - bbox[0]

        crop_aspect = calculate_aspect(crop_width, crop_height)
        # Remove this if you don't want to add top padding to get to
        # aspect ratio of 3.
        if(fit_ratio):
            if(crop_aspect > 3):
                scale_factor = crop_aspect / 3
                print(scale_factor)
                height_pad = round(crop_height * scale_factor)
                crop_height = bbox[3] + height_pad
                bbox_vert_start = bbox[1] - height_pad
                bbox = (bbox[0] - 20, bbox_vert_start,
                        bbox[2] + 20, crop_height)
        return im.crop(bbox)


if __name__ == "__main__":
    # The image to be cropped
    images_path = os.path.join(os.getcwd(), 'images')
    os.mkdir(os.path.join(os.getcwd(), 'cropped_images'))
    for image in os.listdir(images_path):
        image_path = os.path.join(images_path, image)
        print(image_path)
        image_name, suffix = os.path.splitext(image)
        im = Image.open(image_path)
        new_im = crop(im, False)
        new_im.save('cropped_images/' + image_name + '_cropped' + suffix)
