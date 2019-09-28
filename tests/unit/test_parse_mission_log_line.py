"""Тесты чтения ATYPE из логов"""
import unittest

from core import parse_mission_log_line

ATYPE_10_LINE = 'T:42979 AType:10 PLID:1153026 PID:1154050 BUL:360 SH:0 BOMB:0 RCT:0 ' + \
                '(215023.0156,66.8702,239581.0156) IDS:fd0660bd-665d-4368-a954-5bf80f6e991d ' + \
                'LOGIN:fd0660bd-665d-4368-a954-5bf80f6e991d NAME:72AG_Crusader TYPE:LaGG-3 ser.29 ' + \
                'COUNTRY:101 FORM:0 FIELD:2029568 INAIR:2 PARENT:-1 ISPL:1 ISTSTART:1 PAYLOAD:0 FUEL:0.5353 SKIN: WM:1'


class TestPlayersController(unittest.TestCase):
    """Тесты чтения ATYPE из логов"""

    def test_atype_10(self):
        """Читается AType:10"""
        # Act
        atype = parse_mission_log_line(ATYPE_10_LINE)
        # Assert
        self.assertTrue(atype)
