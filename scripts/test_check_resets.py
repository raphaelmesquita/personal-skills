import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_resets


class CheckResetsTimezoneTests(unittest.TestCase):
    def test_formats_email_expiry_in_local_time_without_timezone_suffix(self):
        self.assertEqual(
            check_resets.fmt_local_expiry(
                "2026-06-27T15:30:00Z",
                timezone_name="America/Sao_Paulo",
            ),
            "27/06/2026 às 12:30:00",
        )

    def test_treats_offsetless_api_timestamp_as_utc(self):
        self.assertEqual(
            check_resets.fmt_local_expiry(
                "2026-06-27T15:30:00",
                timezone_name="America/Sao_Paulo",
            ),
            "27/06/2026 às 12:30:00",
        )


if __name__ == "__main__":
    unittest.main()
