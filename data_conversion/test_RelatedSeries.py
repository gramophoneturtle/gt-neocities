import RelatedSeries

test_seriesName = "New Series"
test_seriesURL = "https://gramophoneturtle.neocities.org"

def NoRelatedEntries():
    relSeries = RelatedSeries(test_seriesName, test_seriesURL)
    assert relSeries.SeriesName == "SHOULD FAIL"
    assert relSeries.SeriesURL == test_seriesURL
