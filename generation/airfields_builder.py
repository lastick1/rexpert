"""Сборка групп аэродромов"""
import pathlib
import configs
from .mcu import Airfield
from .groups import AirfieldGroup


class AirfieldsBuilder:
    """Сборщик групп аэродромов"""
    def __init__(self, airfields_groups_folders: dict, airfield_radius: int, config: configs.Planes):
        self.planes_config = config.cfg
        self.airfield_radius = airfield_radius
        self.airfields_groups_folders = airfields_groups_folders

    def make_airfield_group(self, name: str, country: int, x: float, z: float, planes: list) -> AirfieldGroup:
        """Создать координатную группу аэродрома"""
        airfield = Airfield(name=name, country=country, radius=self.airfield_radius, planes=planes)
        folder = pathlib.Path(self.airfields_groups_folders[country])
        file = '!x{0:.0f}z{1:.0f}.Group'.format(x, z)
        result = AirfieldGroup(airfield.format(), folder.joinpath(file))
        result.make()
        return result
