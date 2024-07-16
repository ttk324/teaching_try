
from otree.api import *
c = cu

doc = '\nOne player decides how to divide a certain amount between himself and the other\nplayer.\nSee: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness\nand the assumptions of economics." Journal of business (1986):\nS285-S300.\n'
class C(BaseConstants):
    NAME_IN_URL = 'nodisclosure'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    ODD_ROLE = 'oddplayer'
    EVEN_ROLE = 'evenplayer'
    INSTRUCTIONS_TEMPLATE = 'nodisclosure/instructions.html'
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    import random
    for group in subsession.get_groups():
        group.random_number = random.uniform(0, 1)
class Group(BaseGroup):
    option_selected = models.StringField()
    option1or2 = models.StringField(choices=[['option1', 'option1'], ['option2', 'option2']], initial='didnotchoose', widget=widgets.RadioSelect)
    option2aor2b = models.StringField(blank=True, choices=[['option2a', 'option2a'], ['option2b', 'option2b']], initial='didnotchoose', widget=widgets.RadioSelect)
    random_number = models.FloatField()
def set_payoffs(group: Group):
    oddplayer = group.get_player_by_role(C.ODD_ROLE)
    evenplayer = group.get_player_by_role(C.EVEN_ROLE)
    
    if group.option1or2=="option1":
        oddplayer.payoff=30
        evenplayer.payoff=25
    if group.option1or2=="option2":
        if group.option2aor2b=="option2a":
            oddplayer.payoff=20
            evenplayer.payoff=50
        if group.option2aor2b=="option2b":
            # 50% chance get  "high" case
            if group.random_number>0.5:
                oddplayer.payoff=50
                evenplayer.payoff=35
            if group.random_number<=0.5:
                oddplayer.payoff=0
                evenplayer.payoff=35            
class Player(BasePlayer):
    pass
class Introduction(Page):
    form_model = 'player'
class Option1or2(Page):
    form_model = 'group'
    form_fields = ['option1or2']
    @staticmethod
    def is_displayed(player: Player):
        return player.role==C.ODD_ROLE
class Option2aor2b(Page):
    form_model = 'group'
    form_fields = ['option2aor2b']
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.role==C.ODD_ROLE and group.option1or2=="option2"
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
page_sequence = [Introduction, Option1or2, Option2aor2b, ResultsWaitPage, Results]