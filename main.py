from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageSequence
from copy import deepcopy
import time

BASE_PATH = './data/'
PHOTO_SRC1_PATH = BASE_PATH + 'pic1.jpg'
PHOTO_SRC2_PATH = BASE_PATH + 'pic2.jpg'
PHOTO_TMP_PATH = BASE_PATH + 'tmp'
PHOTO_OUT_PATH = BASE_PATH + 'out.gif'

RATIO = 20
CROP_SIZE = 10 // RATIO
ROTATE_OFFSET = 0


def process_frame(args):
    frame_idx, gifs, matrix, src_frames = args

    # Calc new width and height for frame
    combined_width = gifs[0].width * matrix[0]
    combined_height = gifs[0].height * matrix[1]
    combined_frame = Image.new('RGBA', (combined_width, combined_height))

    # Combine frames into a bigger one
    cnt = matrix[0] * matrix[1]
    # for i in range(cnt):
    i = 0
    for w in range(matrix[0]):
        for h in range(matrix[1]):
            if (w==1 and (h==0 or h==2)):     # Vertical
                frame = src_frames[2][frame_idx].copy()
            elif (h==1 and (w==0 or w==2)):  # Horizontal
                frame = src_frames[1][frame_idx].copy()
            else:
                frame = src_frames[0][frame_idx].copy()

            combined_frame.paste(frame, (gifs[0].width * w, gifs[0].height * h))
                
    return combined_frame

def combine_gifs_parallel(gif_paths, output_path, matrix=[]):
    # Load gifs
    gifs = [Image.open(gif_path) for gif_path in gif_paths]
    src_frames = [[frame.copy() for frame in ImageSequence.Iterator(gif)] for gif in gifs]
    frame_count = len(src_frames[0])


    # Load gifs
    # gifs = [Image.open(gif_path) for gif_path in gif_paths]
    
    # Get gif iterator
    # frames_list = [list(ImageSequence.Iterator(gif)) for gif in gifs]
    # frames_list = [[frame.copy() for frame in ImageSequence.Iterator(gif)] for gif in gifs]
    # get frame count
    # frame_count = min([len(frames) for frames in frames_list])


    # Create matrix 
    args_list = [(idx, gifs, matrix, src_frames) for idx in range(frame_count)]
    with ProcessPoolExecutor() as executor:
        combined_frames = list(executor.map(process_frame, args_list))

    # Save
    combined_frames[0].save(output_path, 
                            save_all=True, 
                            append_images=combined_frames[1:], 
                            duration=gifs[0].info['duration'], 
                            loop=gifs[0].info['loop'])



def combine_gifs(gif_path, output_path, matrix=[]):
    # Load gifs
    gif = Image.open(gif_path)
    src_frame = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    frame_count = len(src_frame)

    # Create matrix 
    combined_frames = []
    for frame_idx in range(frame_count):
        # Calc new width and height frame
        combined_width = gif.width * matrix[0]
        combined_height = gif.height * matrix[1]
        combined_frame = Image.new('RGBA', (combined_width, combined_height))

        # Combine frames in to bigger one
        cnt = matrix[0] * matrix[1]
        for i in range(cnt):
            for w in range(matrix[0]):
                for h in range(matrix[1]):
                    combined_frame.paste(src_frame[frame_idx], 
                                            (gif.width*w, gif.height*h))
        combined_frames.append(combined_frame)

    # Save
    combined_frames[0].save(output_path, 
                            save_all=True, 
                            append_images=combined_frames[1:], 
                            duration=gif.info['duration'], 
                            loop=gif.info['loop'])

# Rotate
def convert_gif(src, tar, range_list):
    with Image.open(src) as img_org:
        img = deepcopy(img_org)
        w, h = img.size

        # Resize
        img_size = min([w, h])
        img = img.crop((0, 0, img_size, img_size))
        img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
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

# Horizontal Flip
def convert_gif2(src, tar, range_list):
    with Image.open(src) as img_org:
        img = deepcopy(img_org)
        w, h = img.size

        # Resize
        img_size = min([w, h])
        img = img.crop((0, 0, img_size, img_size))
        img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
        w, h = img.size

        frames = []
        for i in range(*range_list):
            # if i % 12 == 0:
            #     img = img.transpose(Image.FLIP_LEFT_RIGHT)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            frames.append(img)

        # Save to GIF
        frames[0].save(tar, 
                        save_all=True, 
                        append_images=frames[1:], 
                        optimize=False,
                        duration=100,
                        loop=0)

# Vertical Flip
def convert_gif3(src, tar, range_list, flip=False):
    with Image.open(src) as img_org:
        img = deepcopy(img_org)
        w, h = img.size

        # Resize
        img_size = min([w, h])
        img = img.crop((0, 0, img_size, img_size))
        img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
        w, h = img.size

        frames = []
        img = img.rotate(90)
        for i in range(*range_list):
            # if i % 12 == 0:
            #     img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            frames.append(img)

        # Save to GIF
        frames[0].save(tar, 
                        save_all=True, 
                        append_images=frames[1:], 
                        optimize=False,
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
    t0 = time.perf_counter()
    
    matrix = [3, 3]
    tmp_file1 = f'{PHOTO_TMP_PATH}/tmp1.gif'
    tmp_file2 = f'{PHOTO_TMP_PATH}/tmp2.gif'
    tmp_file3 = f'{PHOTO_TMP_PATH}/tmp3.gif'
    tmp_crop_file1 = f'{PHOTO_TMP_PATH}/tmp_crop1.gif'
    tmp_crop_file2 = f'{PHOTO_TMP_PATH}/tmp_crop2.gif'
    tmp_crop_file3 = f'{PHOTO_TMP_PATH}/tmp_crop3.gif'

    # Rotate
    convert_gif(PHOTO_SRC1_PATH, tmp_file1, (0, 360, 10))
    crop_gif(tmp_file1, tmp_crop_file1)

    # Horizontal Flip
    convert_gif2(PHOTO_SRC2_PATH, tmp_file2, (0, 360, 10))
    crop_gif(tmp_file2, tmp_crop_file2)

    # Vertical Flip
    convert_gif3(PHOTO_SRC2_PATH, tmp_file3, (0, 360, 10))
    crop_gif(tmp_file3, tmp_crop_file3)

    # combine_gifs(tmp_crop_file, PHOTO_OUT_PATH, matrix=matrix)
    
    gifs = [tmp_crop_file1, tmp_crop_file2, tmp_crop_file3]
    combine_gifs_parallel(gifs, PHOTO_OUT_PATH, matrix=matrix)

    t1 = time.perf_counter()
    print(f'Execute Time: {t1-t0:.2f} sec')

if __name__ == '__main__':
    main()