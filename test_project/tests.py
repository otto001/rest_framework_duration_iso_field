import datetime

from django.test import TestCase

from rest_framework_duration_iso_field import DurationIsoField


class TestDurationIsoField(TestCase):

    def test_to_representation_basic(self):
        self.assertEqual("PT10H00M00S",
                         DurationIsoField().to_representation(datetime.timedelta(hours=10)))
        self.assertEqual("PT10H10M10S",
                         DurationIsoField().to_representation(datetime.timedelta(hours=10, minutes=10, seconds=10)))

        # days
        self.assertEqual("P02DT10H10M10S",
                         DurationIsoField().to_representation(
                             datetime.timedelta(days=2, hours=10, minutes=10, seconds=10)))
        self.assertEqual("P09DT10H10M10S",
                         DurationIsoField().to_representation(
                             datetime.timedelta(days=9, hours=10, minutes=10, seconds=10)))

    def test_to_representation_overflow(self):
        self.assertEqual("PT11H05M10S",
                         DurationIsoField().to_representation(datetime.timedelta(hours=10, minutes=65, seconds=10)))

        self.assertEqual("P01W93DT11H05M10S",
                         DurationIsoField().to_representation(
                             datetime.timedelta(days=100, hours=10, minutes=65, seconds=10)))
        self.assertEqual("P01W99DT11H05M10S",
                         DurationIsoField().to_representation(
                             datetime.timedelta(days=106, hours=10, minutes=65, seconds=10)))
        self.assertEqual("P02W93DT11H05M10S",
                         DurationIsoField().to_representation(
                             datetime.timedelta(days=107, hours=10, minutes=65, seconds=10)))

        self.assertEqual("P01W93D",
                         DurationIsoField().to_representation(
                             datetime.timedelta(days=99, hours=23, minutes=59, seconds=60)))

        self.assertEqual("P01W94DT01H01M00S",
                         DurationIsoField().to_representation(
                             datetime.timedelta(days=100, hours=24, minutes=60, seconds=60)))

        self.assertEqual("P200W93D",
                         DurationIsoField().to_representation(
                             datetime.timedelta(weeks=200, days=93)))

    def test_parse(self):
        self.assertEqual(datetime.timedelta(hours=10), DurationIsoField().to_internal_value("PT10H00M00S"))

        self.assertEqual(datetime.timedelta(hours=10), DurationIsoField().to_internal_value("PT10H"))
        self.assertEqual(datetime.timedelta(hours=10, minutes=3), DurationIsoField().to_internal_value("PT10H3M"))
        self.assertEqual(datetime.timedelta(weeks=2), DurationIsoField().to_internal_value("P14D"))
        self.assertEqual(datetime.timedelta(days=100, hours=24, minutes=60, seconds=60),
                         DurationIsoField().to_internal_value("P01W94DT01H01M00S"))

        # overflows
        self.assertEqual(datetime.timedelta(days=10), DurationIsoField().to_internal_value("PT240H"))
        self.assertEqual(datetime.timedelta(hours=10), DurationIsoField().to_internal_value("PT600M"))
        self.assertEqual(datetime.timedelta(minutes=10), DurationIsoField().to_internal_value("PT600S"))
