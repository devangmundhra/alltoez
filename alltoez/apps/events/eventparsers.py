import urllib, urllib2
import json
import re
from datetime import date, timedelta, datetime

from bs4 import BeautifulSoup


def get_sfkids_events(days_from_today = 0):
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


def get_redtri_events(days_from_today = 0):
    """
    Get a list of events from redtri.com/events/san-francisco at a certain number of days after today
    """
    find_date = date.today() + timedelta(days=days_from_today)
    find_date_str = find_date.strftime('%Y/%m/%d')
    print 'Getting events from redtri for date ' + find_date_str

    url = "{}/{}/".format("http://redtri.com/events/san-francisco", find_date_str)

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()

    soup = BeautifulSoup(content)
    pager_soup = soup.find("div", class_="pager")

    events = []
    if pager_soup:
        next_link_soup = pager_soup.find_all("a", class_="page-numbers")

        # Get the events for the current page
        events += (get_redtri_events_at_url(url, find_date))

        # Get the events for the next pages
        for next_link in next_link_soup:
            url = next_link["href"]
            events += get_redtri_events_at_url(url, find_date)
    else:
        # This is probably the end of the month
        events += get_redtri_events_at_url(url, find_date)

    return events


def get_redtri_events_at_url(url, find_date):
    """
    Get a list of events from redtri.com/events/san-francisco on a particular pagination page at a certain date
    """
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()

    soup = BeautifulSoup(content)

    events_soup = soup.find("div", class_="selected-day-events")
    events_soup = events_soup.find("div", class_="events-2-cols-grid")

    events = []

    process_events = False

    for child in events_soup.children:
        if child.name == "h1":
            this_date_str = unicode(child.string)
            this_date = datetime.strptime(this_date_str, "%A, %B %d")
            # this_date is only good for day and month
            this_date = this_date.replace(year=find_date.year)
            if find_date == this_date.date():
                process_events = True
            else:
                process_events = False
            continue
        # So we have reached the section where the events are for the date that we are looking for
        if process_events and child.name == "div" and "event" in child.attrs.get("class", []):
            event_url = child.find("div", class_="event-body").h2.a["href"]
            event = extract_info_from_redtri_event(event_url)
            events.append(event)

    return events


def extract_info_from_redtri_event(url):
    """
    Extract the event information for the particular event from redtri.com
    """
    print 'Extracting info from url ' + url

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()
    soup = BeautifulSoup(content)

    event_info = soup.find("div", class_="event-single")
    event_info = event_info.find("div", class_="column-2")

    event = dict()
    event[u'title'] = soup.title.contents[0]
    event[u'orig_link'] = url
    for info in event_info.contents:
        if info.name != "div" and info.name != "p":
            continue
        if "add-cal" in info.attrs.get("class", []):
            continue
        if "pl-link" in info.attrs.get("class", []):
            continue

        if "the scoop:" in repr(list(info.strings)):
            event_des_soup = info.find("div", class_="prose")
            event_des = repr(list(event_des_soup.strings))
            event[u"description"] = event_des
        elif "more info:" in repr(list(info.strings)):
            event_url = info.a["href"]
            event[u"url"] = event_url
        else:
            event_label_soup = info.find("span", class_="event-label")
            if not event_label_soup:
                continue
            event_content_soup = info.find("span", class_="event-content")
            if not event_content_soup:
                continue
            event_label = unicode(event_label_soup.string)[:-1]
            if len(list(event_content_soup.strings)) > 1:
                event_content = unicode(list(event_content_soup.strings))
            else:
                event_content = unicode(event_content_soup.string)
            event[event_label] = event_content

    return event