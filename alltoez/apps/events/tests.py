from datetime import date

from django.test import TestCase

from eventparsers import get_sfkids_events, extract_info_from_sfkids_event
from eventparsers import get_redtri_events, extract_info_from_redtri_event


class EventParserTestCase(TestCase):
    """
    Testcase to see if parsing individual events from the different event sources is still working
    """
    def setUp(self):
        pass

    def test_sfkids_parser(self):
        # Confirm we are able to get events
        num_events = get_sfkids_events(0)
        self.assertGreater(num_events, 0, 'zero sfkids.org events on {}'.format(date.today()))

        # Check our parsing of events is OK
        key_set = set([u'field-name-field-accessibility', u'Location', u'Organization Tag', u'Parent Event?', u'Ages Served', u'Email', u'Financial Assistance', u'Website', u'Getting There', u'Description', u'Special Needs Support', u'title', u'Season', u'Languages Spoken', u'Free', u'Date', u'Categories', u'orig_link', u'Phone Number', u'field-name-field-registration-deadline-memo', u'Time', u'Neighborhood', u'Tags', u'Cost'])
        event = extract_info_from_sfkids_event("http://sfkids.org/events/emergency-and-disaster-preparedness-families")
        self.assertTrue(set(event.keys()).issubset(key_set), "Error parsing http://sfkids.org/events/emergency-and-disaster-preparedness-families")

        key_set = set([u'Website', u'Neighborhood', u'Description', u'title', u'Phone Number', u'Free', u'field-name-field-accessibility', u'Location', u'Time', u'Date', u'Parent Event?', u'Ages Served', u'Email', u'Categories', u'orig_link'])
        event = extract_info_from_sfkids_event("http://sfkids.org/events/drop-play-randall-museum-toddler-tree-house-159")
        self.assertTrue(set(event.keys()).issubset(key_set), "Error parsing http://sfkids.org/events/drop-play-randall-museum-toddler-tree-house-159")

    def test_redtri_parser(self):
        # Confirm we are able to get events
        num_events = get_redtri_events(0)
        self.assertGreater(num_events, 0, 'zero redtri.com events on {}'.format(date.today()))

        # Check our parsing of events is OK
        key_set = set([u'description', u'title', u'url', u'when', u'ages', u'cost', u'where', u'orig_link'])
        event = extract_info_from_redtri_event("http://redtri.com/san-francisco/get-the-real-story-at-toddler-tales/")
        self.assertTrue(set(event.keys()).issubset(key_set), "Error parsing http://redtri.com/san-francisco/get-the-real-story-at-toddler-tales/")

        key_set = set([u'description', u'title', u'url', u'when', u'ages', u'cost', u'where', u'orig_link'])
        event = extract_info_from_redtri_event("http://redtri.com/san-francisco/mommy-me-spanish-immersion-class-2/")
        self.assertTrue(set(event.keys()).issubset(key_set), "Error parsing http://redtri.com/san-francisco/mommy-me-spanish-immersion-class-2/")