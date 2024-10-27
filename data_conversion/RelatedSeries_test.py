import RelatedSeries
import unittest

test_seriesName = "New Series"
test_seriesURL = "https://gramophoneturtle.neocities.org"

class Test_TestRelatedSeries(unittest.TestCase):

    def NoRelatedEntries(self):
        relSeries = RelatedSeries(test_seriesName, test_seriesURL)
        self.assertEqual(relSeries.SeriesName, "SHOULD FAIL")
        self.assertEqual(relSeries.SeriesURL, test_seriesURL)

if __name__ == '__main__':
    unittest.main()