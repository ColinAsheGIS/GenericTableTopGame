from util import calculate_modifier

def test_calculate_modifier():

    test_data = [
        {
            "stat": 1,
            "modifier": -5
        },
        {
            "stat": 8,
            "modifier": -1
        },
        {
            "stat": 15,
            "modifier": 2
        },
        {
            "stat": 25,
            "modifier": 7
        }
    ]

    for stat in test_data:
        assert stat['modifier'] == calculate_modifier(stat['stat'])