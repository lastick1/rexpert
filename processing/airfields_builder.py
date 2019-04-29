"""Сборка групп аэродромов"""
from __future__ import annotations
import pathlib
import configs
from .mcu import Airfield
from .groups import AirfieldGroup, Group


CONVERT_KEY = {
    101: 'red',
    201: 'blue',
    'red': 'red',
    'blue': 'blue'
}


def _format_name(x: float, z: float) -> str:
    return '!x{0:.0f}z{1:.0f}'.format(x, z)


def _get_group_file_name(x: float, z: float, folder: pathlib.Path) -> pathlib.Path:
    return folder.joinpath((_format_name(x=x, z=z) + '.Group').format(x, z)).absolute()


class AirfieldsBuilder:
    """Сборщик групп аэродромов"""
    def __init__(self, airfields_groups_folders: dict, subtitle_groups_folder: pathlib.Path, config: configs.Planes):
        self.planes_config = config.cfg
        self.airfields_groups_folders = airfields_groups_folders
        self.subtitle_groups_folder = subtitle_groups_folder.absolute()

    def make_airfield_group(self, airfield: Airfield, x: float, z: float) -> AirfieldGroup:
        """Создать координатную группу аэродрома"""
        group_file = _get_group_file_name(x=x, z=z, folder=self.airfields_groups_folders[CONVERT_KEY[airfield.country]])
        result = AirfieldGroup(airfield.format(), group_file)
        result.make()
        return result

    def make_subtitle_group(self, airfield: Airfield, x: float, z: float, template_group: pathlib.Path) -> Group:
        """Создать координатную группу субтитров"""
        result = Group(group_file=template_group)
        result.clone_to(self.subtitle_groups_folder)
        result.rename(_format_name(x=x, z=z))
        result.replace_content('!AFNAME!', airfield.name)
        return result
