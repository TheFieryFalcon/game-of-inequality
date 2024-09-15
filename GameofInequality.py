# Game of Inequality
# Abhijith Madhavan & Uno Wong
# September 2024

# import libraries
import os
import random
import time
from enum import Enum
import carddata
import scll
# define types
class Race(Enum):
    PLACEHOLDER = 0
    WHITE = 1
    ASIAN = 2
    INDIAN = 3
    LATINO = 4
    INDIGENOUS = 5
    BLACK = 6
class CardType(Enum):
    PLACEHOLDER = 0
    PROPERTY = 1
    UTILITY = 2
    RAILROAD = 3
    TAX = 4
    FREE = 5
    GOTOJAIL = 6
    CHANCE = 7
    COMMUNITYCHEST = 8
    GO = 9
class Set(Enum):
    BROWN = 5
    CYAN = 10
    PURPLE = 15
    ORANGE = 20
    RED = 25
    YELLOW = 30
    GREEN = 35
    BLUE = 40

class Player:
    money = 2000
    properties = []
    race = Race.PLACEHOLDER
    name = 'Placeholder'
    injail = False
    bankrupt = False
    position = 0
    rolleddoubles = 0
    timesmoved = 0
    builthousethisturn = False
    turnssincecenterlink = 0
    sortedproperties = {
        "Brown": [],
        "Cyan": [],
        "Purple": [],
        "Orange": [],
        "Red": [],
        "Yellow": [],
        "Green": [],
        "Blue": [],
        "Railroads": [],
        "Utilities": []
    }
    def __init__(this, name, race):
        this.name = name
        this.race = race
    def __str__(this):
        return this.name
    def rolldice(this):
        random.seed()
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        print("Rolling dice...")
        time.sleep(1)
        print ("Dice 1: " + dice1)
        print ("Dice 2: " + dice2)
        if dice1 == dice2:
            print ("Doubles!")
            this.rolleddoubles = this.rolleddoubles + 1
        this.move(this, dice1+dice2)
    def move (this, spaces):
        this.position += spaces
        if (this.position > 39):
            this.money += 200
            this.turnssincecenterlink += 1
            this.position = this.position % 40
        this.timesmoved = this.timesmoved + 1
        if this.rolleddoubles==3:
            this.gotojail()
        elif this.rolleddoubles == this.timesmoved:
            this.rolldice()
        else:
            this.playerturn(False)
    def playerturn (this):
        this.builthousethisturn = False
        this.rolleddoubles = 0
        this.timesmoved = 0
        cardon = carddata.Cards.board[this.position]
        action = input(f"What would you like to do, {this.name}? \n 1 to buy this card (if applicable) \n 2 to put houses on this card (if applicable) \n 3 to sell this card (if applicable) \n 4 to view stats of this card \n 5 to view your own stats \n 6 to collect centerlink benefits (if applicable) \n 9 to end your turn")
        match action:
            case[1]:
                if (cardon.cardtype < 4):
                    cardon.buy(this)
                else:
                    print("You cannot buy this type of card!")
            case[2]:
                if (cardon.cardtype == 1):
                    cardon.construct_house(this)
                else:
                    print("You cannot construct houses on that type of card!")
            case[3]:
                if (cardon.cardtype < 4):
                    cardon.sell(this)
                else:
                    print("You cannot sell that type of card!")
            case[4]:
                print(f" Name: {cardon.name} \nType: {cardon.cardtype.name}")
                match cardon.cardtype:
                    case[1]:
                        if (cardon.owner == emptyplayer):
                            print(f" Set: {cardon.set.name} \n Price: {cardon.price} \n Base rent: {cardon.set.value} \n Rent with 1 house: {cardon.set.value * cardon.rentbase[1]} \n Rent with 2 houses: {cardon.set.value * cardon.rentbase[2]} \n Rent with 3 houses: {cardon.set.value * cardon.rentbase[3]} \n Rent with 4 houses: {cardon.set.value * cardon.rentbase[4]} \n Rent with a hotel: {cardon.set.value * cardon.rentbase[5]}")
                        else:
                            print(f" Set: {cardon.set.name} \n Owner: {cardon.owner.name} \n Owner's race: {cardon.owner.race} \n Rent: {cardon.rent}")
                    case[2]:
                        if (cardon.owner == emptyplayer):
                            print(" Rent with 1 railroad: 25 \n Rent with 2 railroads: 50 \n Rent with 3 railroads: 100 \n Rent with 4 railroads: 200")
                        else:
                            print(f" Owner: {cardon.owner.name} \n Owner's race: {cardon.owner.race} \n Rent: {cardon.rent}")
                    case[3]:
                        if (cardon.owner == emptyplayer):
                            print(" Rent with 1 utility: 4x rolled total \n Rent with 2 utilities: 10x rolled total")
                        else:
                            print(f" Owner: {cardon.owner.name} \n Owner's race: {cardon.owner.race} \n Rent: {cardon.multi}x rolled total")
                    case[4]:
                        print(f" Payment: {cardon.tax}")
                    case[9]:
                        print("Get 200 for passing and 400 for landing here")
            case[5]:
                print(f" Name: {this.name} \n Race: {this.race} \n Properties Owned: ")
                for key in this.sortedproperties.keys():
                    if(this.sortedproperties[key].len > 0):
                        print (f"{key} Set:")
                        for property in this.sortedproperties[key]:
                            print(property.name)
                print (f" Balance: {this.money} ")


            case[9]:
                shouldbreak = True
        if (shouldbreak == False):
            this.playerturn(this)
        else:
            this.postplayerturn()
    def postplayerturn(this):
        pass
    def gotojail(this):
        pass
        # abhijith implement these
    def chance(this):
        pass
    def chest(this):
        pass
    def modifybalance(this, amount):
        if (this.race != Race.INDIAN):
            this.money == this.money + amount
            return(this.money)
        elif (amount > 0):
            this.money = this.money + amount
    def refreshrent(this, property):
            trainstations = []
            utilities = []
            trainstationrents = [25, 50, 100, 200]
            utilitymultis = [4, 10]
            if (property in this.properties):
                match property.cardtype:
                    case[1]:
                        match property.set:
                            case[Set.BROWN]:
                                this.sortedproperties["Brown"].remove(property)
                            case[Set.CYAN]:
                                this.sortedproperties["Cyan"].remove(property)
                            case[Set.PURPLE]:
                                this.sortedproperties["Purple"].remove(property)
                            case[Set.ORANGE]:
                                this.sortedproperties["Orange"].remove(property)
                            case[Set.RED]:
                                this.sortedproperties["Red"].remove(property)
                            case[Set.YELLOW]:
                                this.sortedproperties["Yellow"].remove(property)
                            case[Set.GREEN]:
                                this.sortedproperties["Green"].remove(property)
                            case[Set.BLUE]:
                                this.sortedproperties["Blue"].remove(property)
                    case[2]:
                        trainstations.remove(property)
                        this.sortedproperties["Railroads"].remove(property)
                    case[3]:
                        utilities.remove(property)
                        this.sortedproperties["Utilities"].remove(property)
            else:
                match property.cardtype:
                    case[1]:
                        match property.set:
                            case[Set.BROWN]:
                                this.sortedproperties["Brown"].append(property)
                            case[Set.CYAN]:
                                this.sortedproperties["Cyan"].append(property)
                            case[Set.PURPLE]:
                                this.sortedproperties["Purple"].append(property)
                            case[Set.ORANGE]:
                                this.sortedproperties["Orange"].append(property)
                            case[Set.RED]:
                                this.sortedproperties["Red"].append(property)
                            case[Set.YELLOW]:
                                this.sortedproperties["Yellow"].append(property)
                            case[Set.GREEN]:
                                this.sortedproperties["Green"].append(property)
                            case[Set.BLUE]:
                                this.sortedproperties["Blue"].append(property)
                    case[2]:
                        trainstations.append(property)
                        this.sortedproperties["Railroads"].append(property)
                    case[3]:
                        utilities.append(property)
                        this.sortedproperties["Utilities"].append(property)
            for trainstation in trainstations:
                trainstation.rent == trainstationrents[trainstations.len]
            for utility in utilities:
                utility.multi == utilitymultis[utilities.len]
                
#too much effort to implement
'''            for key in this.sortedproperties.keys():
                this.fullsetbonus(key, sp2[key].pop(0), sp2)
    def fullsetbonus(this, color, number, sp):
        if (sp[color].len >= number):
            for property in sp[color]:
                property.rent = property.rent*2
                property.remove
        else
        
'''             
emptyplayer = Player("Empty", Race.PLACEHOLDER)
class Card:
    cardtype = CardType.PLACEHOLDER
    owner = emptyplayer
    housesbuilt = 0
    rentbase = [1, 4, 12, 28, 34, 40]
    def __init__(this, cardtype, name, space, **kwargs):
        b = kwargs.get('b', None)
        c = kwargs.get('c', None)
        this.cardtype = cardtype
        this.name = name
        match cardtype:
            case [1]:
                this.price = b
                this.set = c
                this.rent = this.set.value
                match this.set:
                    case [Set.BROWN] | [Set.CYAN]:
                        this.houseprice = 50
                    case [Set.PURPLE] | [Set.ORANGE]:
                        this.houseprice = 100
                    case [Set.RED] | [Set.YELLOW]:
                        this.houseprice = 150
                    case [Set.GREEN] | [Set.BLUE]:
                        this.houseprice = 200
            case [2]:
                this.multiplier = 4
                this.price = 150
            case[3]:
                this.rent = 25
                this.price = 200
            case[4]:
                this.tax = b
            case[6]:
                #5 is empty
                this.effect=Player.gotojail
            case[7]:
                this.effect=Player.chance
            case[8]:
                this.effect=Player.chest
                #logic of 9 is determined in turn code
    def gettype(this):
        return(this.cardtype)
    def sell(this, player):
        if (player == this.owner):
            this.owner = emptyplayer
            sellprice = (this.price + (this.houseprice * this.housesbuilt))/2
            player.modifybalance(sellprice)
            player.properties.remove(this)
            player.refreshrent(this)
            this.housesbuilt = 0
            if (this.cardtype == CardType.PROPERTY):
                this.rent = this.set.value
        else:
            print("You don't own that property!")
        
    def construct_house (this, player):
            if (player.money >= this.houseprice & player == this.owner & this.housesbuilt < 5 & player.builthousethisturn == False):
                player.modifybalance(this.houseprice * -1)
                this.housesbuilt += 1
                this.rent = this.set.value * this.rentbase[this.housesbuilt]
            else:
                print("Building not successful. Balance has not been deducted.")
    def buy(this, player):
        if (this.owner == emptyplayer):
            if (player.money > this.price):
                player.modifybalance(this.price * -1)
                player.properties.append(this)
                player.refreshrent(this)
            else:
                print("Not enough money!")
        else:
            print("Someone else already owns this card!")
        
        
                
        
# define modules
def clearconsole():
    os.system("cls" if os.name == "nt" else "clear")

def tokenselect(player_list):
    # List of available tokens (races)
    tokens = [Race.ASIAN, Race.BLACK, Race.INDIAN, Race.INDIGENOUS, Race.WHITE, Race.LATINO]
    print("\nToken assignments:")
    for player in player_list.traverse():
        if tokens:
            player.race = random.choice(tokens)
            print(f"Player {player} got the token {player.race}!")
    currentplayer = player_list.getnodeat(0)
            #Allow duplicates
def playerturns(player):
    print(f"\n{player}'s turn")
    i = input("Press N to roll dice")
    if i != "n":
        print ("Please press N to roll dice")
    else:
        player.rolldice()

def gamestart():
    print("Welcome everyone, it is time for the grand token selection. Each player is given a token with which they (\n) are either given perks or unhappiness.")
    print("This is the part that will determine your fate in the Game of Inequality.")
    tokenselect()
    



# mainline
print("************************************************************")
time.sleep(5)
print("---------- Abhijith Madhavan and Uno Wong present: ---------")
time.sleep(3)
print("------------------- Game of Inequality ---------------")
print("-------- The prejudice of institutional racism -------")
print("************************************************************")

while True:
    time.sleep(3)
    clearconsole()
    print("Welcome to the Game of Inequality, a modified version of Monopoly! This game will teach you why a world with institutional racism will never go well.")
    nameno = int(input("How many players are here today? More than two players can play! \n"))
    if nameno < 2:
        print("Not enough players!")
        continue
    elif nameno > 5:
        print("Too many players!")
        continue
    player_list = scll.SingularCircularLinkedList()
    for i in range(nameno):
        name = input(f"Select a name for the player {i + 1} \n")
        player_list.append(name)
    
    for i, name in enumerate(player_list.traverse()):
        print(f"Player {i + 1}: {name}")
    print("Starting game...")
    gamestart()
