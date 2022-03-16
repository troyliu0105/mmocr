import argparse
import glob
import os.path

import exrex
import numpy as np
import tqdm
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class WordsGenerator(object):
    def __init__(self, dict_file):
        with open(dict_file, encoding="UTF-8") as fp:
            dicts = [l.replace("\n", "").replace("\r", "").strip() for l in fp.readlines()]
            dicts.insert(0, " ")
        self.dicts = dicts
        p = np.zeros((len(dicts),))
        p[:70] = 0.6 / len(p[:70])
        p[70:] = 0.4 / len(p[70:])
        self.p = p

    def generate(self, size, with_replace=True):
        # 生成时间
        if np.random.rand() > 0.85:
            words = exrex.getone(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        else:
            words = "".join(np.random.choice(self.dicts, size=size, replace=with_replace, p=self.p))
        return words


def generate_on_image(image: Image,
                      font_files,
                      words_generator: WordsGenerator,
                      min_lines=2, max_lines=6,
                      min_font_size=10, max_font_size=35,
                      min_len=5, max_len=50,
                      min_space=0, max_space=10,
                      draw_bbox=False):
    drawer = ImageDraw.Draw(image)
    img_w, img_h = image.size
    lines = np.random.randint(min_lines, max_lines)
    top_margin = 0
    bottom_margin = 0
    results = []
    for i in range(lines):
        font = ImageFont.truetype(np.random.choice(font_files),
                                  np.random.randint(min_font_size, max_font_size),
                                  index=0)
        # 字符串长度
        words_size = np.random.randint(min_len, max_len)
        # 字边
        stroke_width = np.random.randint(0, 3)
        stroke_fill = np.random.randint(0, 25)
        stroke_fill = (stroke_fill, stroke_fill, stroke_fill)
        # 字体颜色
        fill = np.random.randint(200, 240)
        fill = (fill, fill, fill)
        # 生成字符串
        while text := words_generator.generate(words_size):
            valid = True
            for c in text:
                if len(np.array(font.getmask(c))) == 0 and c != ' ':
                    valid = False
                    # print(f"invalid: {c}")
                    break
            if valid:
                break
        # 获得字符串的实际大小
        w, h = drawer.textsize(text, font=font, stroke_width=stroke_width)
        if w >= img_w or h >= img_h:
            continue
        # 行间距
        space = np.random.randint(min_space, max_space)
        # 在图像上半部分生成。xy 为单行的左上角起点
        if i % 2 == 0:
            y = top_margin + space
            x = np.random.randint(0, img_w - w)
            top_margin += y + h
        else:
            y = img_h - bottom_margin - space - h
            x = np.random.randint(0, img_w - w)
            bottom_margin = img_h - y
        # 每一行对空白切分
        for j, seg in enumerate(filter(lambda it: len(it.strip()) > 0, text.split(" "))):
            if len(seg) < 5:
                continue
            seg_w, seg_h = drawer.textsize(seg, font=font, stroke_width=stroke_width)
            if x + seg_w >= img_w or y + seg_h >= img_h:
                break
            drawer.text((x, y), seg, fill=fill, font=font, stroke_width=stroke_width, stroke_fill=stroke_fill,
                        spacing=0)
            if draw_bbox:
                drawer.rectangle((x, y, x + seg_w, y + seg_h), outline=(255, 0, 0), width=2)
            results.append([x, y, x + seg_w, y, x + seg_w, y + seg_h, x, y + seg_h, seg])

            space_w, _ = drawer.textsize(" " * np.random.randint(1, 4), font=font, stroke_width=stroke_width)
            x += space_w + seg_w
    return image, results


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--background-dir", required=True, type=str, help="Background images...")
    parser.add_argument("--out-dir", required=True, type=str, help="output images...")
    parser.add_argument("--anno-dir", required=True, type=str, help="Annotation folder...")
    parser.add_argument("--word-dir", required=True, type=str, help="Annotation folder...")
    parser.add_argument("--word-label", required=True, type=str, help="Annotation folder...")
    parser.add_argument("--font-dir", required=True, type=str, help="Font folder...")
    parser.add_argument("--dict-file", required=True, type=str, help="dict file")
    args = parser.parse_args()
    return args


def main(background_dir, out_dir, anno_dir, word_dir, word_label, font_dir, dict_file):
    image_files = glob.glob(f"{background_dir}/**/*.jpg", recursive=True)
    fonts = glob.glob(f"{font_dir}/**/*.ttf", recursive=True)
    words_generator = WordsGenerator(dict_file)
    words_results = []
    word_idx = 0
    for image_file in tqdm.tqdm(image_files, desc="Generating..."):
        image = Image.open(image_file)
        out_image, results = generate_on_image(image, fonts, words_generator,
                                               min_lines=2, max_lines=6,
                                               min_font_size=20, max_font_size=35,
                                               min_len=5, max_len=35,
                                               min_space=0, max_space=5,
                                               draw_bbox=False)
        out_image_file = os.path.join(out_dir, os.path.split(image_file)[1])
        out_image.save(out_image_file)
        with open(os.path.join(anno_dir, os.path.splitext(os.path.split(image_file)[1])[0] + ".txt"),
                  mode="w",
                  encoding="utf-8") as fp:
            lines = [",".join([str(i) for i in l[:8]] + ["Chinese", l[8]]) + "\n" for l in results]
            fp.writelines(lines)
            for result in results:
                roi = (result[0], result[1], result[2], result[5])
                word = out_image.crop(roi)
                word_file = f"{word_dir}/word_{word_idx:08d}.jpg"
                word.save(word_file)
                word_idx += 1
                words_results.append(f"{word_file} {result[-1]}\n")
        if len(words_results) > 1000:
            with open(word_label, "a+", encoding="utf-8") as fp:
                fp.writelines(words_results)
            words_results.clear()


if __name__ == '__main__':
    args = parse_args()
    main(args.background_dir, args.out_dir, args.anno_dir, args.word_dir, args.word_label, args.font_dir,
         args.dict_file)
