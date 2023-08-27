from PIL import Image, ImageSequence
from copy import deepcopy

BASE_PATH = './data/'
PHOTO_SRC1_PATH = BASE_PATH + 'pic1.jpg'
PHOTO_SRC2_PATH = BASE_PATH + 'pic2.jpg'
PHOTO_TMP_PATH = BASE_PATH + 'tmp'
PHOTO_OUT_PATH = BASE_PATH + 'out.gif'

RATIO = 20
CROP_SIZE = 10 // RATIO
ROTATE_OFFSET = 0


def combine_gifs(gif_paths, output_path, matrix=[]):
    # Load gifs
    gifs = [Image.open(gif_path) for gif_path in gif_paths]
    
    # Get gif iterator
    # frames_list = [list(ImageSequence.Iterator(gif)) for gif in gifs]
    frames_list = [[frame.copy() for frame in ImageSequence.Iterator(gif)] for gif in gifs]

    # get frame count
    frame_count = min([len(frames) for frames in frames_list])
    combined_frames = []
    for frame_idx in range(frame_count):
        # Calc new width and height frame
        combined_width = gifs[0].width * matrix[0]
        combined_height = gifs[0].height * matrix[1]
        combined_frame = Image.new('RGBA', (combined_width, combined_height))

        # Combine frames in to bigger one
        cnt = matrix[0] * matrix[1]
        for i in range(cnt):
            for w in range(matrix[0]):
                for h in range(matrix[1]):
                    combined_frame.paste(frames_list[i][frame_idx], 
                                            (gifs[0].width*w, gifs[0].height*h))
        combined_frames.append(combined_frame)

    # Save
    combined_frames[0].save(output_path, 
                            save_all=True, 
                            append_images=combined_frames[1:], 
                            optimize=False,
                            duration=gifs[0].info['duration'], 
                            loop=gifs[0].info['loop'])


def convert_gif(src, tar, range_list, flip=False):
    with Image.open(src) as img_org:
        img = deepcopy(img_org)
        w, h = img.size

        # Resize
        img_size = min([w, h])
        img = img.crop((0, 0, img_size, img_size))
        img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
        if flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        w, h = img.size

        frames = []
        for i in range(*range_list):
            rotated_image = img.rotate(i)
            frames.append(rotated_image)

        # Save to GIF
        frames[0].save(tar, 
                        save_all=True, 
                        append_images=frames[1:], 
                        duration=100,
                        loop=0)

def crop_gif(src, tar):
    with Image.open(src) as img:
        w, h = img.size
        frames = []
        for frame in ImageSequence.Iterator(img):
            cropped_frame = frame.crop((CROP_SIZE, CROP_SIZE, w-CROP_SIZE, h-CROP_SIZE))
            frames.append(cropped_frame)

        frames[0].save(tar, 
                        save_all=True, 
                        append_images=frames[1:], 
                        duration=img.info['duration'], 
                        loop=img.info['loop'])


def main():
    # tmp_file = f'{PHOTO_TMP_PATH}/tmp.gif'
    # tmp_crop_file = f'{PHOTO_TMP_PATH}/tmp_crop.gif'
    # convert_gif(PHOTO_SRC1_PATH, tmp_file, (0, 360, 10))
    # crop_gif(tmp_file, tmp_crop_file)

    gif_paths = []
    for i in range(9):
        tmp_file = f'{PHOTO_TMP_PATH}/{i}_tmp.gif'
        tmp_crop_file = f'{PHOTO_TMP_PATH}/{i}_tmp_crop.gif'
        convert_gif(PHOTO_SRC1_PATH, tmp_file, (0, 360, 10))
        crop_gif(tmp_file, tmp_crop_file)
        gif_paths.append(tmp_crop_file)

    combine_gifs(gif_paths, PHOTO_OUT_PATH, matrix=[3, 3])

if __name__ == '__main__':
    main()