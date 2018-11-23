"""Функции создания изображений карт из кусочков"""
import os
import re
from PIL import Image


def merge_map(map_dir=r'./tiles/kuban/tiles/04/', output='map.png'):
    """Склейка карты из тайлов"""
    # Выборка файлов-тайлов
    files = os.listdir(map_dir)
    tiles = [p for p in filter(lambda x: x.endswith('.dds'), files)]
    tiles.sort(key=lambda x: x[0])
    print(tiles)
    # Формирование матрицы тайлов
    tile_matrix = []
    re_tile = re.compile(r'(^\d+)_(\d+)')
    i = 0
    tile_string = []
    coords = []
    x_size = 0
    y_size = 0
    img_size = None
    for tile in tiles:
        coord = re_tile.findall(tile)
        if coord != None:
            coords.append(coord[0])
            img = Image.open(map_dir + tile)
            if img_size != None and img_size != img.size:
                print("Ошибка размера тайла")
                return None
            else:
                img_size = img.size
            if i > 0:
                if coords[i-1][0] != coords[i][0]:
                    tile_matrix.append(tile_string.copy())
                    if x_size > 0:
                        if len(tile_string) != x_size:
                            print("Ошибка в последовательности тайлов!")
                            return None
                    x_size = len(tile_string)
                    tile_string.clear()
                tile_string.append(img)
            else:
                tile_string.append(img)
            i += 1
    tile_matrix.append(tile_string)
    y_size = len(tile_matrix)

    # Склейка карты
    res_img = Image.new('RGBA', (img_size[0]*x_size, img_size[1]*y_size))
    j = 0
    for line in tile_matrix:
        i = 0
        for cimg in line:
            res_img.paste(cimg, (img_size[0]*i, img_size[1]*j))
            i += 1
        j += 1
    res_img.save(output, 'PNG')
    return None


merge_map()
