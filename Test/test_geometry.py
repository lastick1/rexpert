from unittest import TestCase
import geometry


class TestSegment(TestCase):
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
