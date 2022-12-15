from app.basic import top_drivers


class TestBasic:
    def test_top_drivers(self, top_drivers_dataFrame):
        assert top_drivers == top_drivers_dataFrame
