from PIL import Image, ImageSequence
from copy import deepcopy

BASE_PATH = './data/'
PHOTO_SRC_PATH = BASE_PATH + 'pic.jpg'
PHOTO_TARGET_1_PATH = BASE_PATH + 'pic_1.gif'
PHOTO_TARGET_2_PATH = BASE_PATH + 'pic_2.gif'
PHOTO_TARGET_3_PATH = BASE_PATH + 'pic_3.gif'
PHOTO_TARGET_4_PATH = BASE_PATH + 'pic_4.gif'

PHOTO_CROP_1_TARGET_PATH = BASE_PATH + 'pic_crop1.gif'
PHOTO_CROP_2_TARGET_PATH = BASE_PATH + 'pic_crop2.gif'
PHOTO_CROP_3_TARGET_PATH = BASE_PATH + 'pic_crop3.gif'
PHOTO_CROP_4_TARGET_PATH = BASE_PATH + 'pic_crop4.gif'

PHOTO_MATRIX_PATH = BASE_PATH + 'pic_matrix.gif'

PHOTO_OTHER_PATH = BASE_PATH + 'other'

RATIO = 3
CROP_SIZE = 170 // RATIO
# ROTATE_OFFSET = 110
ROTATE_OFFSET = 0


def combine_gifs(gif_paths, output_path):
    # 載入所有 GIFs
    gifs = [Image.open(gif_path) for gif_path in gif_paths]
    
    # 取得每個 GIF 的幀列表
    # frames_list = [list(ImageSequence.Iterator(gif)) for gif in gifs]
    frames_list = [[frame.copy() for frame in ImageSequence.Iterator(gif)] for gif in gifs]

    # 確保所有 GIF 的幀數是一樣的（簡化示例，真實情況可能需要更多的處理）
    frame_count = min([len(frames) for frames in frames_list])
    combined_frames = []


    for frame_idx in range(frame_count):
        # 創建一個新的幀來放置 2x2 矩陣中的幀
        combined_width = gifs[0].width + gifs[1].width
        combined_height = gifs[0].height + gifs[2].height
        combined_frame = Image.new('RGBA', (combined_width, combined_height))

        # 將每個 GIF 的當前幀放到正確的位置
        combined_frame.paste(frames_list[0][frame_idx], (0, 0))
        combined_frame.paste(frames_list[1][frame_idx], (gifs[0].width, 0))
        combined_frame.paste(frames_list[2][frame_idx], (0, gifs[0].height))
        combined_frame.paste(frames_list[3][frame_idx], (gifs[1].width, gifs[2].height))

        combined_frames.append(combined_frame)

        # combined_frame.save(f"{PHOTO_OTHER_PATH}/frame_{frame_idx}.png")

    # 儲存組合後的 GIF
    combined_frames[0].save(output_path, 
                            save_all=True, 
                            append_images=combined_frames[1:], 
                            optimize=False,
                            duration=gifs[0].info['duration'], 
                            loop=gifs[0].info['loop'])



# def flip(src, tar, mode):
#     # Mode: Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM
#     with Image.open(src) as im:
#         frames = []
#         for frame in ImageSequence.Iterator(im):
#             flipped_frame = frame.transpose(mode)
#             frames.append(flipped_frame)

#         frames[0].save(tar, 
#                         save_all=True, 
#                         append_images=frames[1:], 
#                         duration=im.info['duration'], 
#                         loop=im.info['loop'])

# def rotate(src, tar, degree):
#     # Mode: Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM
#     with Image.open(src) as im:
#         frames = []
#         for frame in ImageSequence.Iterator(im):
#             flipped_frame = frame.rotate(degree)
#             frames.append(flipped_frame)

#         frames[0].save(tar, 
#                         save_all=True, 
#                         append_images=frames[1:], 
#                         duration=im.info['duration'], 
#                         loop=im.info['loop'])


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

    
    convert_gif(PHOTO_SRC_PATH, PHOTO_TARGET_4_PATH, (0, 360, 10))
    crop_gif(PHOTO_TARGET_4_PATH, PHOTO_CROP_4_TARGET_PATH)

    convert_gif(PHOTO_SRC_PATH, PHOTO_TARGET_3_PATH, (360, 0, -10), True)
    crop_gif(PHOTO_TARGET_3_PATH, PHOTO_CROP_3_TARGET_PATH)

    convert_gif(PHOTO_SRC_PATH, PHOTO_TARGET_1_PATH, (360, 0, -10), True)
    crop_gif(PHOTO_TARGET_1_PATH, PHOTO_CROP_1_TARGET_PATH)

    convert_gif(PHOTO_SRC_PATH, PHOTO_TARGET_2_PATH, (0, 360, 10))
    crop_gif(PHOTO_TARGET_2_PATH, PHOTO_CROP_2_TARGET_PATH)

    # Convert GIF 4
    # with Image.open(PHOTO_SRC_PATH) as img_org:
    #     img = deepcopy(img_org)
    #     w, h = img.size

    #     # Resize
    #     img_size = min([w, h])
    #     img = img.crop((0, 0, img_size, img_size))
    #     img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
    #     w, h = img.size

    #     frames = []
    #     for i in range(0, 360, 10):
    #         rotated_image = img.rotate(i)
    #         frames.append(rotated_image)

    #     # Save to GIF
    #     frames[0].save(PHOTO_TARGET_4_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=100,
    #                     loop=0)

    # # Crop 4
    # with Image.open(PHOTO_TARGET_4_PATH) as img:
    #     w, h = img.size
    #     frames = []
    #     for frame in ImageSequence.Iterator(img):
    #         cropped_frame = frame.crop((CROP_SIZE, CROP_SIZE, w-CROP_SIZE, h-CROP_SIZE))
    #         frames.append(cropped_frame)

    #     frames[0].save(PHOTO_CROP_4_TARGET_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=img.info['duration'], 
    #                     loop=img.info['loop'])


    # # Convert GIF 3
    # with Image.open(PHOTO_SRC_PATH) as img_org:
    #     img = deepcopy(img_org)
    #     w, h = img.size

    #     # Resize
    #     img_size = min([w, h])
    #     img = img.crop((0, 0, img_size, img_size))
    #     img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
    #     img = img.transpose(Image.FLIP_LEFT_RIGHT)
    #     w, h = img.size

    #     frames = []
    #     for i in range(360, 0, -10):
    #         rotated_image = img.rotate(i)
    #         frames.append(rotated_image)

    #     # Save to GIF
    #     frames[0].save(PHOTO_TARGET_3_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=100,
    #                     loop=0)

    # # Crop 3
    # with Image.open(PHOTO_TARGET_3_PATH) as img:
    #     w, h = img.size
    #     frames = []
    #     for frame in ImageSequence.Iterator(img):
    #         cropped_frame = frame.crop((CROP_SIZE, CROP_SIZE, w-CROP_SIZE, h-CROP_SIZE))
    #         frames.append(cropped_frame)

    #     frames[0].save(PHOTO_CROP_3_TARGET_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=img.info['duration'], 
    #                     loop=img.info['loop'])


    # # Convert GIF 1
    # with Image.open(PHOTO_SRC_PATH) as img_org:
    #     img = deepcopy(img_org)
    #     w, h = img.size

    #     # Resize
    #     img_size = min([w, h])
    #     img = img.crop((0, 0, img_size, img_size))
    #     img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
    #     img = img.transpose(Image.FLIP_LEFT_RIGHT)
    #     w, h = img.size

    #     frames = []
    #     for i in range(360, 0, -10):
    #         rotated_image = img.rotate(i-ROTATE_OFFSET)
    #         frames.append(rotated_image)

    #     # Save to GIF
    #     frames[0].save(PHOTO_TARGET_1_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=100,
    #                     loop=0)

    # # Crop 1
    # with Image.open(PHOTO_TARGET_1_PATH) as img:
    #     w, h = img.size
    #     frames = []
    #     for frame in ImageSequence.Iterator(img):
    #         cropped_frame = frame.crop((CROP_SIZE, CROP_SIZE, w-CROP_SIZE, h-CROP_SIZE))
    #         frames.append(cropped_frame)

    #     frames[0].save(PHOTO_CROP_1_TARGET_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=img.info['duration'], 
    #                     loop=img.info['loop'])


    # # Convert GIF 2
    # with Image.open(PHOTO_SRC_PATH) as img_org:
    #     img = deepcopy(img_org)
    #     w, h = img.size

    #     # Resize
    #     img_size = min([w, h])
    #     img = img.crop((0, 0, img_size, img_size))
    #     img = img.resize((w//RATIO, h//RATIO), Image.LANCZOS)
    #     w, h = img.size

    #     frames = []
    #     for i in range(0, 360, 10):
    #         rotated_image = img.rotate(i+ROTATE_OFFSET)
    #         frames.append(rotated_image)

    #     # Save to GIF
    #     frames[0].save(PHOTO_TARGET_2_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=100,
    #                     loop=0)

    # # Crop 2
    # with Image.open(PHOTO_TARGET_2_PATH) as img:
    #     w, h = img.size
    #     frames = []
    #     for frame in ImageSequence.Iterator(img):
    #         cropped_frame = frame.crop((CROP_SIZE, CROP_SIZE, w-CROP_SIZE, h-CROP_SIZE))
    #         frames.append(cropped_frame)

    #     frames[0].save(PHOTO_CROP_2_TARGET_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=img.info['duration'], 
    #                     loop=img.info['loop'])




    # flip(PHOTO_CROP_4_TARGET_PATH, PHOTO_CROP_3_TARGET_PATH, Image.FLIP_LEFT_RIGHT)
    # rotate(PHOTO_CROP_4_TARGET_PATH, PHOTO_CROP_2_TARGET_PATH, 45)
    # rotate(PHOTO_CROP_3_TARGET_PATH, PHOTO_CROP_1_TARGET_PATH, 45)

    # flip(PHOTO_CROP_4_TARGET_PATH, PHOTO_CROP_2_TARGET_PATH, Image.FLIP_TOP_BOTTOM)
    # flip(PHOTO_CROP_2_TARGET_PATH, PHOTO_CROP_1_TARGET_PATH, Image.FLIP_LEFT_RIGHT)


    # Create Matrix
    gif_paths = [PHOTO_CROP_1_TARGET_PATH, PHOTO_CROP_2_TARGET_PATH,
                    PHOTO_CROP_3_TARGET_PATH, PHOTO_CROP_4_TARGET_PATH]

    # gif_paths = [PHOTO_TARGET_1_PATH, PHOTO_TARGET_2_PATH,
    #                 PHOTO_TARGET_3_PATH, PHOTO_TARGET_4_PATH]
    combine_gifs(gif_paths, PHOTO_MATRIX_PATH)


    # # Horizontal Flip
    # with Image.open(PHOTO_CROP_4_TARGET_PATH) as im:
    #     frames = []
    #     for frame in ImageSequence.Iterator(im):
    #         flipped_frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
    #         frames.append(flipped_frame)

    #     frames[0].save(PHOTO_CROP_3_TARGET_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=im.info['duration'], 
    #                     loop=im.info['loop'])

    # # Vertical Flip
    # with Image.open(PHOTO_CROP_4_TARGET_PATH) as im:
    #     frames = []
    #     for frame in ImageSequence.Iterator(im):
    #         flipped_frame = frame.transpose(Image.FLIP_TOP_BOTTOM)
    #         frames.append(flipped_frame)

    #     frames[0].save(PHOTO_CROP_2_TARGET_PATH, 
    #                     save_all=True, 
    #                     append_images=frames[1:], 
    #                     duration=im.info['duration'], 
    #                     loop=im.info['loop'])


if __name__ == '__main__':
    main()