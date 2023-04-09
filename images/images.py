import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

def get_size(font: ImageFont, text: str):
    lines = text.replace("\n\n", "\na\n").split("\n")
    w = max([font.getsize(l)[0] + 5 for l in lines])
    h = sum([font.getsize(l)[1] + 5 for l in lines])
    return w, h

def get_text_image(text, font_file, size):
    MAX_W, MAX_H = 12800,7200

    im = Image.new('RGBA', (MAX_W, MAX_H))
    font = ImageFont.truetype(font_file, size)

    relative_w, relative_h = get_size(font, text)

    mid_w, mid_h = MAX_W / 2, MAX_H / 2
    epsilon = 5
    im = im.crop((mid_w - relative_w / 2 - epsilon, mid_h - relative_h / 2 - epsilon, mid_w + relative_w / 2 + epsilon, mid_h + relative_h / 2 + epsilon))

    draw = ImageDraw.Draw(im)

    draw.text((epsilon, epsilon), text, align='center', font=font)

    return im

def generate_characters(characters, font_file, size):
    chars = {}
    for chrs in characters:
        f_name = str(ord(chrs))
        chars[f_name] = get_text_image(chrs, font_file, size)

def get_color(RGB: tuple):
    color = Image.new('RGB', (1280, 720), RGB)
    return color

def gradient(RGB):
    # Define width and height of image
    W, H = 720, 720

    # Create solid red image
    im = Image.new(mode='RGB', size=(W,H), color=RGB)

    # Create radial alpha/transparency layer. 255 in centre, 0 at edge
    Y = np.linspace(-1, 1, H)[None, :]*255
    X = np.linspace(-1, 1, W)[:, None]*255
    alpha = (X**2 + Y**2) ** 0.5
    alpha = np.clip(0,255,alpha)

    # Push that radial gradient transparency onto red image and save
    im.putalpha(Image.fromarray(alpha.astype(np.uint8)))
    return im

def rectangle(width, height):
    im = Image.new(mode='RGB', size=(width, height), color=(255,255,255))
    return im

def randomglitcheffect(width, height, RGB, chance):
    im = Image.new(mode='RGB', size=(width, height), color=RGB)
    alp = np.random.choice([0,1], p=[1 - chance, chance], size=(width, height)) * 255

    im.putalpha(Image.fromarray(alp.astype(np.uint8)))
    return im

def white_ball():
    W, H = 500, 500
    im = Image.new(mode='RGB', size=(W,H), color=(255,255,255))
    
    Y = np.linspace(-1, 1, H)[None, :]*255
    X = np.linspace(-1, 1, W)[:, None]*255
    al = (X ** 2 + Y ** 2) ** 0.5
    al[al<=255] = 255
    al[al > 255] = 0
    
    
    im.putalpha(Image.fromarray(al.astype(np.uint8)))
    return im

def glitch_crop(im: Image, n_portions: int):
    visible = np.random.randint(0, n_portions, size=im.size).T
    for i in range(n_portions):
        alpha = np.ones(im.size) * 255
        alpha = alpha.T
        alpha[visible != i] = 0
        alpha[np.array(im)[:, :, 0] == 0] = 0 
        copy_image = im.copy()
        alpha = Image.fromarray(alpha.astype(np.uint8))
        copy_image.putalpha(alpha)
        yield copy_image

def crop_edge(im: Image):
    alp = np.array(im)[:, :, 1].T
    horiz_edge = np.sort(np.where(np.sum(alp, axis=1) != 0)[0])
    vert_edge = np.sort(np.where(np.sum(alp.T, axis=1) != 0)[0])
    
    im = im.crop((horiz_edge[0], vert_edge[0], horiz_edge[-1], vert_edge[-1]))
    return im
