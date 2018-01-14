"Модуль рисования"
import math
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
from configs import Mgen, Draw

class SplineTuple:
    """Вспомогательный класс - описание сплайна через коэффициенты"""
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0
    x = 0.0

    def __init__(self):
        a = 0.0
        b = 0.0
        c = 0.0
        d = 0.0
        x = 0.0


def get_parallel_multiline(pts, dist):
    """Расчёт ломанной линии, параллельной заданной"""
    n = len(pts)
    i = 0
    tmppts = [[0.0, 0.0] for p in range(n)]
    while i < n - 1:
        tmpline = get_parallel_line([pts[i], pts[i + 1]], dist)
        tmppts[i] = tmpline[0]
        tmppts[i + 1] = tmpline[1]
        i += 1
    return [(p[0], p[1]) for p in tmppts]


def get_parallel_line(line_x_y, dist):
    """Расчёт параллельного заданному (line_x_y) отрезка"""
    x1 = line_x_y[0][0]
    y1 = line_x_y[0][1]
    x2 = line_x_y[1][0]
    y2 = line_x_y[1][1]
    """Нахождение вектора нормали к исходной прямой"""
    norm = [y2 - y1, x1 - x2]
    """Длина вектора"""
    lenn = math.sqrt(math.pow(norm[0], 2) + math.pow(norm[1], 2))
    """Коэффициент перевода длины вектора нормали к заданному расстоянию"""
    kl = dist / lenn
    """Нахождение вектора нужной длины, коллинеарного нормали"""
    vect = [norm[0] * kl, norm[1] * kl]
    """Нахождение первой точки отрезка"""
    resbeg = (vect[0] + x1, vect[1] + y1)
    """Нахождение второй точки отрезка"""
    resend = (vect[0] + x2, vect[1] + y2)
    return [resbeg, resend]


def polydim_spline(pts, skip=False):
    """Интерполяция производной двухмерной функции двухмерным же сплайном"""
    """Подготовка вспомогательных массивов"""
    n = len(pts)
    x = [p[0] for p in pts]
    y = [p[1] for p in pts]
    t = [0.0 for p in range(n)]
    xt = [[0.0, 0.0] for p in range(n)]
    yt = [[0.0, 0.0] for p in range(n)]
    xt[0] = [t[0], x[0]]
    yt[0] = [t[0], y[0]]
    i = 1
    while i < n:
        """подготовка ряда ti"""
        t[i] = t[i - 1] + math.sqrt(math.pow(x[i] - x[i - 1], 2) + math.pow(y[i] - y[i - 1], 2))
        """Подготовка функций x(t), y(t)"""
        xt[i] = [t[i], x[i]]
        yt[i] = [t[i], y[i]]
        i += 1
    """Интерполяция кубическим сплайном x(t), y(t)"""
    s_xt = make_cube_spline(xt)
    s_yt = make_cube_spline(yt)
    """Подготовка результирующих координат"""
    result = []
    i = 0
    for pt in s_xt:
        # берём только каждую 25-ю вершину (отсекаем избыточные данные)
        if skip and i % 25:
            i += 1
            continue
        result.append((pt[1], s_yt[i][1]))
        i += 1
    return result


def make_cube_spline(pts):
    """Расчёт промежуточных точек функции при помощи кубического сплайна"""
    n = len(pts)
    splines = []
    """Инициализация массива сплайнов"""
    for pt in pts:
        spline = SplineTuple()
        spline.x = pt[0]
        spline.a = pt[1]
        splines.append(spline)
    splines[0].c = 0.0
    splines[n - 1].c = 0.0
    """Вспомогательные массивы"""
    x = [p[0] for p in pts]
    y = [p[1] for p in pts]
    """Решение СЛАУ относительно коэффициентов сплайнов c[i] методом прогонки для трехдиагональных матриц"""

    """Вычисление прогоночных коэффициентов - прямой ход метода прогонки"""
    alpha = [0.0 for k in range(n)]
    beta = [0.0 for k in range(n)]
    i = 1
    while i < n - 1:
        hi = x[i] - x[i - 1]
        hi1 = x[i + 1] - x[i]
        A = hi
        C = 2.0 * (hi + hi1)
        B = hi1
        F = 6.0 * ((y[i + 1] - y[i]) / hi1 - (y[i] - y[i - 1]) / hi)
        z = A * alpha[i - 1] + C
        alpha[i] = -1.0 * B / z
        beta[i] = (F - A * beta[i - 1]) / z
        i += 1

    """Нахождение решения - обратный ход метода прогонки"""
    i = n - 2
    while i > 0:
        splines[i].c = alpha[i] * splines[i + 1].c + beta[i]
        i -= 1

    """По известным коэффициентам c[i] находим значения b[i] и d[i]"""
    i = n - 1
    while i > 0:
        hi = x[i] - x[i - 1]
        splines[i].d = (splines[i].c - splines[i - 1].c) / hi
        splines[i].b = hi * (2.0 * splines[i].c + splines[i - 1].c) / 6.0 + (y[i] - y[i - 1]) / hi
        i -= 1

    """Вычисление точек интерполированной функции"""
    sx = x[0]
    result = []
    while sx < x[n - 1]:
        s = SplineTuple()
        if sx <= splines[0].x:
            s = splines[0]
        elif sx >= splines[n - 1].x:
            s = splines[n - 1]
        else:
            i = 0
            j = n - 1
            while i + 1 < j:
                k = int(i + (j - i) / 2)
                if sx <= splines[k].x:
                    j = k
                else:
                    i = k
            s = splines[j]
        dx = sx - s.x
        sy = s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx
        if sy < 0:
            sy = 0
        result.append((sx, sy))
        sx += 10
    return result


def draw_spline(
        cut,  # набор из линий фронта
        draw,
        linewidth=6,  # толщина линии фронта
        dist=10,  # расстояние между составными кривыми линии фронта
        color=((189, 1, 1), (77, 75, 64))  # цвета линии фронта
):
    lines = []
    """Функция отрисовки линии фронта, сглаженной двухмерным кубическим сплайном
        Линия фронта состоит из 2 параллельных линий"""
    for line in cut:
        pts = [(float(p[0]), float(p[1])) for p in line]
        respts = polydim_spline(pts)
        parpts1 = get_parallel_multiline(respts, int(dist / 2))
        parpts2 = get_parallel_multiline(respts, int(dist / (-2)))

        lines.append(list(tuple(int(z) for z in x) for x in respts))

        draw.line(xy=parpts1, fill=color[1], width=linewidth)
        draw.line(xy=parpts2, fill=color[0], width=linewidth)

        """Костыль:
        если "котёл" - принудительно замыкаем линии"""
        if pts[0] == pts[len(pts) - 1]:
            draw.line([parpts1[0], parpts1[len(parpts1) - 1]], fill=color[1], width=linewidth)
            draw.line([parpts2[0], parpts2[len(parpts2) - 1]], fill=color[0], width=linewidth)


def get_splines(
        cut,  # набор из линий фронта
        dist=2000  # расстояние между составными кривыми линии фронта
):
    """Функция отрисовки линии фронта, сглаженной двухмерным кубическим сплайном
        Линия фронта состоит из 2 параллельных линий"""
    lines = []

    for line in cut:
        pts = [(float(p[0]), float(p[1])) for p in line]
        respts = polydim_spline(pts, skip=True)
        parpts1 = get_parallel_multiline(respts, int(dist / 2))
        parpts2 = get_parallel_multiline(respts, int(dist / (-2)))
        lines.append([parpts1, parpts2])
    return lines


def draw_graph(neutral_line, influences, map_name, nodes: list, edges: list, mgen: Mgen, draw: Draw, icons=None, debug_data=None):
    base = Image.open(draw.background[map_name]).convert('RGBA')
    kp_icons = {x: Image.open(draw.icons[x]['flames']) for x in draw.coals}
    draw = ImageDraw.Draw(base)
    x_coefficient = abs(base.size[1] / mgen.cfg[map_name]['right_top']['x'])
    z_coefficient = abs(base.size[0] / mgen.cfg[map_name]['right_top']['z'])
    if draw.draw_nodes:
        for n in nodes:
            if not n.country:
                continue
            if not n.is_aux:
                p = (n.z * z_coefficient, base.size[1] - n.x * x_coefficient)
                paste = kp_icons[draw.cfg['countries'][str(n.country)]]
                base.paste(paste, (int(p[0] - paste.size[0] / 2), int(p[1] - paste.size[1] / 2)), paste)

                if draw.draw_nodes_text:
                    fnt = ImageFont.truetype(font="arial", size=20)
                    fill = (189, 1, 1)
                    if n.country == 201:
                        fill = (77, 75, 64)
                    draw.text((int(p[0] + paste.size[0] / 2), int(p[1] - paste.size[1])),
                              str(n.key),
                              fill=fill, font=fnt)
    if draw.draw_edges:
        for e in edges:
            e_points = [(a.z * z_coefficient, base.size[1] - a.x * x_coefficient) for a in e]
            draw.line(e_points[0] + e_points[1], fill=(0, 0, 0), width=7)

    if draw.draw_influences:
        for country in influences:
            fill = (189, 1, 1)
            if country == 201:
                fill = (77, 75, 64)
            for line in influences[country]:
                dots = []
                for p in line:
                    x = base.size[1] - int(p.z * z_coefficient)
                    x = 0 if x < 0 else x if x < base.size[1] else base.size[1]
                    z = int(p.x * x_coefficient)
                    z = 0 if z < 0 else z if z < base.size[0] else base.size[0]
                    dots.append((x, z))
                draw.line(dots, fill=fill, width=7)

    points = [list((int(x.z * z_coefficient), int(base.size[1] - x.x * x_coefficient)) for x in neutral_line)]
    with open('lines.json', mode='w') as f:
        f.write(json.dumps(points))
    draw_spline(points, draw)
    if debug_data:
        for n in debug_data:
            p = (n.z * z_coefficient, base.size[1] - n.x * x_coefficient)
            color = (255, 255, 255)  # if n.country == 101 else (0, 0, 255)
            draw.ellipse(
                (p[0] - base.size[0] / 100, p[1] - base.size[1] / 100) +
                (p[0] + base.size[0] / 100, p[1] + base.size[1] / 100),
                fill=color,
                outline=(0, 0, 0))
    flame = Image.open(draw.flame)
    airfield = Image.open(draw.airfield)
    airfield.thumbnail((draw.cfg['icon_size'][0], draw.cfg['icon_size'][1]), Image.ANTIALIAS)
    for coal in icons.keys():  # ('1', '2'):
        for cls in icons[coal].keys():
            if cls not in draw.cfg['coal_icons']:
                continue
            for point in icons[coal][cls]:
                image = Image.open(draw.icons[draw.cfg['coal_mapping'][coal]][cls])
                image.thumbnail((130, 130), Image.ANTIALIAS)
                coordinates = (
                        int(point['x'] * x_coefficient - image.size[0] / 2),
                        base.size[1] - int(point['z'] * z_coefficient) - int(image.size[1])
                    )
                base.paste(image, coordinates, image)
                if cls == 'flames':
                    coordinates = (
                        int(point['x'] * x_coefficient - flame.size[0] / 2),
                        base.size[1] - int(point['z'] * z_coefficient) - int(flame.size[1])
                    )
                    base.paste(flame, coordinates, flame)
    base.save(StatsCustomCfg.map_full_size)
    th_width = 1140
    size = base.size
    th_aspect = size[1] / size[0]
    th_height = th_width * th_aspect
    th = base.resize((th_width, int(th_height)))
    th.save(StatsCustomCfg.map_main_page)
