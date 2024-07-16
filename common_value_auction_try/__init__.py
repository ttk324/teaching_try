
from otree.api import *
c = cu

doc = '\nIn a common value auction game, players simultaneously bid on the item being\nauctioned.<br/>\nPrior to bidding, they are given an estimate of the actual value of the item.\nThis actual value is revealed after the bidding.<br/>\nBids are private. The player with the highest bid wins the auction, but\npayoff depends on the bid amount and the actual value.<br/>\n'
class C(BaseConstants):
    NAME_IN_URL = 'common_value_auction_try'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 3
    BID_MIN = cu(0)
    BID_MAX = cu(10)
    BID_NOISE = cu(1)
    BUYER_ROLE = 'buyer'
    SELLER_ROLE = 'seller'
    INSTRUCTIONS_TEMPLATE = 'common_value_auction_try/instructions.html'
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    if subsession.round_number==1:
        for p in subsession.get_players():
            if p.id_in_group==1:
                p.role_type="seller"
            if p.id_in_group==2:
                p.role_type="buyer"
            if p.id_in_group==3:
                p.role_type="buyer"
    
    # set the same role type in each match 
    if subsession.round_number > 1:
        for p in subsession.get_players():
            p.role_type=p.in_round(subsession.round_number-1).role_type
    
    
    
    for g in subsession.get_groups():
        import random
    
        item_value = random.uniform(C.BID_MIN, C.BID_MAX)
        g.item_value = round(item_value, 1)
class Group(BaseGroup):
    item_value = models.CurrencyField(doc='Common value of the item to be auctioned random for treatment')
    highest_bid = models.CurrencyField()
def generate_value_estimate(group: Group):
    import random
    
    estimate = group.item_value + random.uniform(
        -C.BID_NOISE, C.BID_NOISE
    )
    estimate = round(estimate, 1)
    if estimate < C.BID_MIN:
        estimate = C.BID_MIN
    if estimate > C.BID_MAX:
        estimate = C.BID_MAX
    return estimate
def set_winner(group: Group):
    import random
    
    players = group.get_players()
    group.highest_bid = max([p.bid_amount for p in players])
    players_with_highest_bid = [p for p in players if p.bid_amount == group.highest_bid]
    winner = random.choice(
        players_with_highest_bid
    )  # if tie, winner is chosen at random
    winner.is_winner = True
    for p in players:
        set_payoff(p)
class Player(BasePlayer):
    item_value_estimate = models.CurrencyField(doc='Estimate of the common value may be different for each player')
    bid_amount = models.CurrencyField(doc='Amount bidded by the player', label='Bid amount', max=C.BID_MAX, min=C.BID_MIN)
    is_winner = models.BooleanField(doc='Indicates whether the player is the winner', initial=False)
    role_type = models.StringField()
def set_payoff(player: Player):
    group = player.group
    if player.is_winner:
        player.payoff = group.item_value - player.bid_amount
        if player.payoff < 0:
            player.payoff = 0
    else:
        player.payoff = 0
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        player.item_value_estimate = generate_value_estimate(group)
class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_winner
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(is_greedy=group.item_value - player.bid_amount < 0)
page_sequence = [Introduction, Bid, ResultsWaitPage, Results]