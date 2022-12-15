import pytest

from app.tests.test_f1_transforms import TestF1Transforms


class TestSuperF1Transforms:
    def testBestTimePerLap(self, lap_times_for_race_989_dataFrame, best_lap_times_for_race_989_dataFrame):
        assert (
            TestF1Transforms().testget_best_time_per_lap(lap_times_for_race_989_dataFrame, best_lap_times_for_race_989_dataFrame)
            == best_lap_times_for_race_989_dataFrame
        )

    def testFastestLap(self, best_lap_times_for_race_989_dataFrame, fastest_lap_for_race_989):
        assert TestF1Transforms().testget_fastest_lap(best_lap_times_for_race_989_dataFrame, fastest_lap_for_race_989) == fastest_lap_for_race_989

    def testBestTimePerLap(self, races_dataFrame, race_id, race_name_for_id_1009):
        assert TestF1Transforms(races_dataFrame, race_id, race_name_for_id_1009).testget_race_name() == race_name_for_id_1009
