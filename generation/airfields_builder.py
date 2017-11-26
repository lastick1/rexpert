"""Сборка групп аэродромов"""
import pathlib
import configs
from .mcu import Airfield
from .groups import AirfieldGroup, Group


def _format_name(x: float, z: float) -> str:
    return '!x{0:.0f}z{1:.0f}'.format(x, z)


def _get_group_file_name(x: float, z: float, folder: pathlib.Path) -> pathlib.Path:
    return folder.joinpath(_format_name(x=x, z=z) + '.Group'.format(x, z))


class AirfieldsBuilder:
    """Сборщик групп аэродромов"""
    def __init__(self, airfields_groups_folders: dict, subtitle_groups_folder: pathlib.Path, airfield_radius: int, config: configs.Planes):
        self.planes_config = config.cfg
        self.airfield_radius = airfield_radius
        self.airfields_groups_folders = airfields_groups_folders
        self.subtitle_groups_folder = subtitle_groups_folder.absolute()

    def make_airfield_group(self, name: str, country: int, x: float, z: float, planes: list) -> AirfieldGroup:
        """Создать координатную группу аэродрома"""
        airfield = Airfield(name=name, country=country, radius=self.airfield_radius, planes=planes)
        group_file = _get_group_file_name(x=x, z=z, folder=self.airfields_groups_folders[country])
        result = AirfieldGroup(airfield.format(), group_file)
        result.make()
        return result

    def make_subtitle_group(self, name: str, x: float, z: float, template_group: pathlib.Path) -> Group:
        """Создать координатную группу субтитров"""
        result = Group(group_file=template_group)
        result.clone_to(self.subtitle_groups_folder)
        result.rename(_format_name(x=x, z=z))
        result.replace_content('!AFNAME!', name)
        return result
