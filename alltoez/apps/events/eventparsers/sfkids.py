import urllib, urllib2
import json
import re
from datetime import date, timedelta

from bs4 import BeautifulSoup


def get_events(days_from_today=0):
    """
    Get a list of events from sfkids.org/events at a certain number of days after today
    """
    find_date = date.today() + timedelta(days = days_from_today)
    find_date_str = find_date.strftime('%m/%d/%Y')
    print 'Getting events from sfkids for date ' + find_date_str

    host = 'http://sfkids.org'
    url = host + '/views/ajax'
    values = {'date_filter[value][date]' : find_date_str,
              'view_name' : 'events',
              'view_display_id' : 'page',
              'view_path' : 'events',
              'view_base_path' : 'events',
              }
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent,
                'X-Requested-With' : 'XMLHttpRequest',
    #             'Host' : host,
                'Referer' : host + '/events',
                'Content-Type' : 'application/x-www-form-urlencoded',
                }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    content = response.read()
    jcontent = json.loads(content, encoding='utf-8')

    soup = BeautifulSoup(json.dumps(jcontent))

    events = []
    for link in soup.find_all('a'):
        href = link.get('href')[2:-2] #it starts and ends with \"
        try:
            event = extract_info_from_sfkids_event(host + href)
        except:
            pass
        events.append(event)

    return events


def extract_info_from_sfkids_event(url):
    """
    Extract the event information for the particular event from sfkids.org/events
    """
    print 'Extracting info from url ' + url

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()
    soup = BeautifulSoup(content)
    article = soup.article
    event_info = article.find("div", class_="content")

    event = dict()
    event[u'title'] = soup.title.contents[0]
    event[u'orig_link'] = url

    for info in event_info.contents:
        if info.name != u'div':
            continue

        '''
        The event info is always in divs with top level structure which looks like:
        <div class="field field-name-field-start-date field-type-datetime field-label-above"><div cnt="2014-08-
        <div class="field field-name-field-start-time field-type-datetime field-label-above"><div cm</sp
        <div class="field field-name-field-get-location field-type-getlocations-fields field-label-above"><div
        <div class="field field-name-field-description field-type-text-long field-label-above"><div class="fie
        '''

        # Sanity check
        assert len(list(info.children)) <= 2

        for idx, child in enumerate(info.children):
            if 'field-label' in child.attrs.get('class', None):
                info_label = unicode(repr(list(child.strings)[0])[2:-6])
                continue
            elif idx == 0:
                #This is a field where the label is not available. Deduce it from the class of the info.
                # Make sure this is really just free text
                assert len(list(info.children)) == 1

                attrs = info.attrs.get('class', None)
                regex = re.compile("(field-name-field-).*")
                info_label = [m.group(0) for l in attrs for m in [regex.search(l)] if m][0]
            else:
                pass
            if 'field-type-link-field' in info.attrs.get('class', None):
                # Links need to be handed specially as they don't show up in child.strings
                info_des = child.a["href"]
            else:
                if len(list(child.strings)) > 1:
                    info_des = unicode(list(child.strings))
                else:
                    info_des = unicode(child.string)
            event[info_label] = info_des

    return event
