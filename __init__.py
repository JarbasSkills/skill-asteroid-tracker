from mycroft import intent_file_handler, intent_handler, MycroftSkill
from mycroft.skills.core import resting_screen_handler
from os.path import join, dirname


class AsteroidsSkill(MycroftSkill):


    @resting_screen_handler("Asteroids")
    def idle(self, message):
        self.gui.clear()
        self.gui.show_url(join(dirname(__file__), "index.html"),
                          override_idle=True)

    @intent_file_handler("asteroids.intent")
    def handle_asteroids_intent(self, message):
        self.speak_dialog("asteroids")
        self.idle(message)


def create_skill():
    return AsteroidsSkill()
