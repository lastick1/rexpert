"""Рисование карт миссий и иконок целей на них"""
from PIL import Image, ImageDraw, ImageFont
from .map_splines import draw_spline
import json


class MapPainter:
    """Рисует карты миссий"""

    def __init__(self, _ioc):
        self._ioc = _ioc

    def update_map(self):
        tvd = self._ioc.campaign_controller.current_tvd
        mission = self._ioc.campaign_controller.mission
        self.draw_map(tvd.border, list(), tvd.name, list(), list(), mission.map_icons)

    def draw_map(
            self,
            neutral_line,
            influences,
            map_name,
            nodes: list,
            edges: list,
            icons=None,
            debug_data=None
    ):
        base = Image.open(self._ioc.config.draw.background[map_name]).convert('RGBA')
        kp_icons = {x: Image.open(self._ioc.config.draw.icons[x]['flames']) for x in self._ioc.config.draw.coals}
        draw = ImageDraw.Draw(base)
        x_coefficient = abs(base.size[1] / self._ioc.config.mgen.cfg[map_name]['right_top']['x'])
        z_coefficient = abs(base.size[0] / self._ioc.config.mgen.cfg[map_name]['right_top']['z'])
        if self._ioc.config.draw.draw_nodes:
            for n in nodes:
                if not n.country:
                    continue
                if not n.is_aux:
                    p = (n.z * z_coefficient, base.size[1] - n.x * x_coefficient)
                    paste = kp_icons[self._ioc.config.draw.cfg['countries'][str(n.country)]]
                    base.paste(paste, (int(p[0] - paste.size[0] / 2), int(p[1] - paste.size[1] / 2)), paste)

                    if self._ioc.config.draw.draw_nodes_text:
                        fnt = ImageFont.truetype(font="arial", size=20)
                        fill = (189, 1, 1)
                        if n.country == 201:
                            fill = (77, 75, 64)
                        draw.text((int(p[0] + paste.size[0] / 2), int(p[1] - paste.size[1])),
                                  str(n.key),
                                  fill=fill, font=fnt)
        if self._ioc.config.draw.draw_edges:
            for e in edges:
                e_points = [(a.z * z_coefficient, base.size[1] - a.x * x_coefficient) for a in e]
                draw.line(e_points[0] + e_points[1], fill=(0, 0, 0), width=7)

        if self._ioc.config.draw.draw_influences:
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
        flame = Image.open(self._ioc.config.draw.flame)
        airfield = Image.open(self._ioc.config.draw.airfield)
        airfield.thumbnail(
            (self._ioc.config.draw.cfg['icon_size'][0], self._ioc.config.draw.cfg['icon_size'][1]), Image.ANTIALIAS)
        for coal in icons.keys():  # ('1', '2'):
            for cls in icons[coal].keys():
                if cls not in self._ioc.config.draw.cfg['coal_icons']:
                    continue
                for point in icons[coal][cls]:
                    path = self._ioc.config.draw.icons[self._ioc.config.draw.cfg['coal_mapping'][coal]][cls]
                    image = Image.open(path)
                    image.thumbnail((130, 130), Image.ANTIALIAS)
                    if not point:
                        print()
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
        base.save(self._ioc.config.stat.map_full_size)
        th_width = 1140
        size = base.size
        th_aspect = size[1] / size[0]
        th_height = th_width * th_aspect
        th = base.resize((th_width, int(th_height)))
        th.save(self._ioc.config.stat.map_main_page)
