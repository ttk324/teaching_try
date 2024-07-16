
from otree.api import *
c = cu

doc = '\nIn a common value auction game, players simultaneously bid on the item being\nauctioned.<br/>\nPrior to bidding, they are given an estimate of the actual value of the item.\nThis actual value is revealed after the bidding.<br/>\nBids are private. The player with the highest bid wins the auction, but\npayoff depends on the bid amount and the actual value.<br/>\n'
class C(BaseConstants):
    NAME_IN_URL = 'Secondpriceauction'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    EVALUATE_MIN = cu(0)
    EVALUATE_MAX = cu(100)
    INSTRUCTIONS_TEMPLATE = 'Secondpriceauction/instructions.html'
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    import random 
    subsession.group_randomly()
    for player in subsession.get_players():
        value=random.uniform(C.EVALUATE_MIN,C.EVALUATE_MAX)
        player.item_value=round(value, 2)
    
class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    second_highest_bid = models.CurrencyField()
def set_winner(group: Group):
    import random
    
    players = group.get_players()
    group.highest_bid = max([p.bid_amount for p in players])
    players_with_highest_bid = [p for p in players if p.bid_amount == group.highest_bid]
    
    not_winners = [p for p in players if p.bid_amount < group.highest_bid]
    if len(not_winners) > 0:
        group.second_highest_bid = max([p.bid_amount for p in not_winners])
    else:
        group.second_highest_bid = group.highest_bid
    
    winner = random.choice(players_with_highest_bid)  
    # if tie, winner is chosen at random
    winner.is_winner = True
    
    for p in players:
        set_payoff(p)
class Player(BasePlayer):
    item_value = models.CurrencyField(doc='Estimate of the common value may be different for each player')
    bid_amount = models.CurrencyField(doc='Amount bidded by the player', label='Bid amount')
    is_winner = models.BooleanField(doc='Indicates whether the player is the winner', initial=False)
def set_payoff(player: Player):
    group = player.group
    if player.is_winner:
        player.payoff = player.item_value - group.second_highest_bid
        #if player.payoff < 0:
         #   player.payoff = 0
    else:
        player.payoff = 0
class Introduction(Page):
    form_model = 'player'
class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_winner
class Results(Page):
    form_model = 'player'
page_sequence = [Introduction, Bid, ResultsWaitPage, Results]