from aggregatorbroker import utils
from datetime import datetime

import unittest


class TestDateTime(unittest.TestCase):

    def test_time_zone(self):
        str_datetime = "2019-11-15T23:08:14.945616+10:00"
        parse_datetime = utils.parse_datetime(str_datetime)
        isoformat = datetime.isoformat(parse_datetime)
        reparse_datetime = utils.parse_datetime(isoformat)
        assert (reparse_datetime - parse_datetime).total_seconds() == 0


if __name__ == '__main__':
    unittest.main()
