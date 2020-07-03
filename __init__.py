from mycroft import intent_file_handler, intent_handler, MycroftSkill
from mycroft.skills.core import resting_screen_handler
from os.path import join, dirname
from requests_cache import CachedSession
from datetime import timedelta, datetime


class AsteroidsSkill(MycroftSkill):
    def __init__(self):
        super(AsteroidsSkill, self).__init__(
            name="AsteroidsSkill")
        if "nasa_key" not in self.settings:
            self.settings["nasa_key"] = "DEMO_KEY"
        _expire_after = timedelta(hours=1)
        self._session = CachedSession(backend='memory',
                                      expire_after=_expire_after)

    @resting_screen_handler("Asteroids")
    def idle(self, message):
        self.gui.clear()
        self.gui.show_url(join(dirname(__file__), "ui", "index.html"),
                          override_idle=200)

    @intent_file_handler("asteroids.intent")
    def handle_asteroids_intent(self, message):
        self.speak_dialog("asteroids")
        self.idle(message)

    # internal methods
    def neo_feed(self, start_date=None, end_date=None):
        '''
        NeoWs (Near Earth Object Web Service) is a RESTful web service for near earth Asteroid information. With NeoWs a user can: search_exoplanet for Asteroids based on their closest approach date to Earth, lookup a specific Asteroid with its NASA JPL small body id, as well as browse the overall data-set.

        Data-set: All the data is from the NASA JPL Asteroid team (http://neo.jpl.nasa.gov/).

        :param start_date: YYYY-MM-DD	none	Starting date for asteroid search_exoplanet
        :param end_date: YYYY-MM-DD	7 days after start_date	Ending date for asteroid search_exoplanet
        :return:
        '''
        url = "https://api.nasa.gov/neo/rest/v1/feed"

        params = {"api_key": self.settings["nasa_key"]}
        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        return self._session.get(url, params=params).json()

    def neo_feed_today(self, detailed=True):
        """
        :return:
        """
        base_url = "https://api.nasa.gov/neo/rest/v1/feed/today?"
        if not detailed:
            base_url += "detailed=false&"
        else:
            base_url += "detailed=true&"
        url = base_url + "api_key=" + self.settings["nasa_key"]
        response = self._session.get(url).json()
        return response

    def neo_lookup(self, asteroid_id):
        '''
        Lookup a specific Asteroid based on its NASA JPL small body (SPK-ID) ID

        :param: asteroid_id	int	Asteroid SPK-ID correlates to the NASA JPL small body
        :return:
        '''
        base_url = "https://api.nasa.gov/neo/rest/v1/neo/" + str(
            asteroid_id) + "?"

        url = base_url + "api_key=" + self.settings["nasa_key"]
        response = self._session.get(url).json()
        return response

    def neo_browse(self):
        '''
        Browse the overall Asteroid data-set
        :return:
        '''
        base_url = "https://api.nasa.gov/neo/rest/v1/neo/browse?"

        url = base_url + "api_key=" + self.settings["nasa_key"]
        response = self._session.get(url).json()
        return response

    def neo_sentry(self, is_active=True, page=0, size=50):
        '''
        Retrieves Near Earth Objects listed in the NASA sentry data set
        :param is_active: show current list of Sentry objects, or show removed Sentry objects
        :return:
        '''
        base_url = "https://api.nasa.gov/neo/rest/v1/feed/today?"
        if not is_active:
            base_url += "is_active=false&"
        else:
            base_url += "is_active=true&"

        base_url += "page=" + str(page) + "&"
        base_url += "size=" + str(size) + "&"

        url = base_url + "api_key=" + self.settings["nasa_key"]
        response = self._session.get(url).json()
        return response

    def sentry_lookup(self, asteroid_id):
        '''
        Retrieves Sentry Near Earth Object by ID

        :param: asteroid_id	str ID of NearEarth object. ID can be SPK_ID, Asteroid des (designation) or Sentry ID
        :return:
        '''
        base_url = "https://api.nasa.gov/neo/rest/v1/neo/sentry/" + str(
            asteroid_id) + "?"

        url = base_url + "api_key=" + self.settings["nasa_key"]
        response = self._session.get(url).json()
        return response


def create_skill():
    return AsteroidsSkill()
