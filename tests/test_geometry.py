#pylint: disable=missing-docstring,invalid-name
import unittest
import geometry

TEST_LOG1 = './testdata/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'

class TestSegment(unittest.TestCase):
    def test_length_must_equal_5_for_345_triangle(self):
        hypotenuse = geometry.Segment(3, 4, 6, 8)
        self.assertEqual(hypotenuse.length, 5)

    def test_center_must_be_3_4_for_0_0_6_8(self):
        hypotenuse = geometry.Segment(0, 0, 6, 8)
        self.assertEqual(hypotenuse.center, (3, 4))

    def test_angle_must_be_0_for_1_1_1_3(self):
        segment = geometry.Segment(1, 1, 1, 3)
        self.assertEqual(segment.angle, 0)

    def test_angle_must_be_90_for_1_1_3_1(self):
        segment = geometry.Segment(1, 1, 3, 1)
        self.assertEqual(segment.angle, 90)

    def test_parallel_segments_must_be_1_5_4_5_and_1_1_4_1_for_1_3_4_3_at_2_distance(self):
        segment = geometry.Segment(1, 3, 4, 3)

        s1, s2 = segment.parallel_segments(2)

        self.assertEqual((s1._x1, s1._y1, s1._x2, s1._y2), (1, 5, 4, 5))
        self.assertEqual((s2._x1, s2._y1, s2._x2, s2._y2), (1, 1, 4, 1))


class TestPoint(unittest.TestCase):
    def test_is_in_area_must_be_true_for_1_1_and_square_size_of_2(self):
        point = geometry.Point(1, 1)
        area = [
            geometry.Point(0, 0), geometry.Point(0, 2), geometry.Point(2, 2), geometry.Point(2, 2)
        ]
        self.assertEqual(True, point.is_in_area(area))
        area.reverse()
        self.assertEqual(True, point.is_in_area(area))

    def test_distance_to_must_be_5_for_1_1_and_4_5(self):
        point = geometry.Point(1, 1)

        self.assertEqual(point.distance_to(4, 5), 5)
