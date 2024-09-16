# Game of Inequality
# Abhijith Madhavan and Uno Wong
# September 2024

# import libraries
import os
import random
import time
from enum import Enum
import scll
# declare globals
currentplayer = None
player_list = None
#init types
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
    UTILITY = 3
    RAILROAD = 2
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
    turnsinjail = 0
    gojfc = 0
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
    clbenefits = [0, 0, 300, 600, 1000, 1500, 2000]
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
        print (f"Dice 1: {dice1}")
        print (f"Dice 2: {dice2}")
        if dice1 == dice2:
            print ("Doubles!")
            this.rolleddoubles = this.rolleddoubles + 1
        this.move((dice1+dice2))
    def move (this, spaces):
        this.builthousethisturn = False
        print(f"Moving {spaces} spaces...")
        time.sleep(2)
        this.position += spaces
        if (this.position > 39):
            if(this.race == Race.INDIAN):
                this.modifybalance(140, "pass go while not looking like you're good at managing finance so they pay you less")
            elif (this.race == Race.ASIAN):
                this.modifybalance(300, "pass go while looking trustworthy and smart")
            else:
                this.modifybalance(200, "pass go")
            this.turnssincecenterlink += 1
            this.position = this.position % 40
        print(f"You landed on {Cards.board[this.position].name}")
        this.timesmoved = this.timesmoved + 1
        if this.rolleddoubles==3:
            this.gotojail()
        elif this.rolleddoubles == this.timesmoved:
            this.rolldice()
        else:
            this.playerturn(spaces)
    def playerturn (this, dicesum):
        this.rolleddoubles = 0
        this.timesmoved = 0
        cardon = Cards.board[this.position]
        action = input(f"What would you like to do, {this.name}? \n 1 to buy this card (if applicable) \n 2 to put houses on this card (if applicable) \n 3 to sell this card (if applicable) \n 4 to view stats of this card \n 5 to view your own stats \n 6 to collect centerlink benefits (if applicable) \n 9 to end your turn\n")
        shouldbreak = False
        match action:
            case '1':
                if (this.race != Race.INDIGENOUS):
                    if (cardon.cardtype.value < 4):
                        cardon.buy(this)
                    else:
                        print("You cannot buy this type of card!")
                else:
                    if (cardon.cardtype.value == 1):
                        cardon.buy (this)
                    elif (cardon.cardtype.value < 4):
                        print("You cannot buy this type of card due to local laws not recognizing you as a full human being.")
                    else:
                        print("You cannot buy this type of card!")
            case '2':
                if (cardon.cardtype.value == 1):
                    cardon.construct_house(this)
                else:
                    print("You cannot construct houses on that type of card!")
            case '3':
                if (cardon.cardtype.value < 4):
                    cardon.sell(this)
                else:
                    print("You cannot sell that type of card!")
            case '4':
                print(f" Name: {cardon.name} \n Type: {cardon.cardtype.name}")
                match cardon.cardtype.value:
                    case 1:
                        if (cardon.owner == emptyplayer):
                            print(f" Set: {cardon.set.name} \n Price: {cardon.price} \n Base rent: {cardon.set.value} \n Rent with 1 house: {cardon.set.value * cardon.rentbase[1]} \n Rent with 2 houses: {cardon.set.value * cardon.rentbase[2]} \n Rent with 3 houses: {cardon.set.value * cardon.rentbase[3]} \n Rent with 4 houses: {cardon.set.value * cardon.rentbase[4]} \n Rent with a hotel: {cardon.set.value * cardon.rentbase[5]}")
                        else:
                            print(f" Set: {cardon.set.name} \n Owner: {cardon.owner.name} \n Owner's race: {cardon.owner.race.name} \n Houses: {cardon.housesbuilt} \n Rent: {cardon.rent}")
                    case 2:
                        if (cardon.owner == emptyplayer):
                            print(" Rent with 1 railroad: 25 \n Rent with 2 railroads: 50 \n Rent with 3 railroads: 100 \n Rent with 4 railroads: 200")
                        else:
                            print(f" Owner: {cardon.owner.name} \n Owner's race: {cardon.owner.race.name} \n Rent: {cardon.rent}")
                    case 3:
                        if (cardon.owner == emptyplayer):
                            print(" Rent with 1 utility: 4x rolled total \n Rent with 2 utilities: 10x rolled total")
                        else:
                            print(f" Owner: {cardon.owner.name} \n Owner's race: {cardon.owner.race.name} \n Rent: {cardon.multi}x rolled total")
                    case 4:
                        print(f" Payment: {cardon.tax}")
                    case 9:
                        print("Get 200 for passing and 400 for landing here")
            case '5':
                print(f" Name: {this.name} \n Race: {this.race.name} \n Properties Owned: ")
                for key in this.sortedproperties.keys():
                    if(len(this.sortedproperties[key]) > 0):
                        print (f" {key} Set:")
                        for property in this.sortedproperties[key]:
                            print(f" {property.name}")
                print (f" Balance: {this.money} ")
                if (this.turnssincecenterlink >= this.race.value and this.race != Race.WHITE):
                    print(" Centerlink Status: READY")
                elif (this.race != Race.WHITE):
                    print(f" Centerlink Status: IN {this.race.value - this.turnssincecenterlink} GO PASSES")
                else:
                    print(" Centerlink Status: INELIGIBLE")
                print(f" Position: {Cards.board[this.position].name}")
            case '6':
                if (this.turnssincecenterlink >= this.race.value and this.race != Race.WHITE):
                    print(f"Collected {this.clbenefits[this.race.value]} in Centerlink benefits!")
                    this.money += this.clbenefits[this.race.value]
                elif (this.race != Race.WHITE):
                    print(f"Too soon since last benefit collection. You will be eligible in {this.race.value - this.turnssincecenterlink} go passes.")
                else:
                    print("You are not eligible for any Centerlink benefits, sorry!")
            case '9':
                shouldbreak = True
            case _:
                print("Invalid input. Please try again")
        if (shouldbreak == False):
            this.playerturn(dicesum)
        else:
            this.postplayerturn(cardon, dicesum)
    def postplayerturn(this, cardon, dicesum):
        match cardon.cardtype.value:
            case 1 | 2:
                if (cardon.owner != emptyplayer and cardon.owner != this and cardon.owner.injail == False):
                    this.modifybalance(cardon.rent * -1, "pay rent to owner")
                    this.bankruptcheck()
                elif (cardon.owner.injail == True):
                    print("Rent was not collected because owner is in jail")
            case 3:
                if (cardon.owner != emptyplayer and cardon.owner != this and cardon.owner.injail == False):
                    this.modifybalance(cardon.multi * -1 * dicesum, "pay usage fees to owner")
                    this.bankruptcheck()
                elif (cardon.owner.injail == True):
                    print("Usage fees was not collected because owner is in jail")
            case 4:
                if (this.race == Race.ASIAN):
                    this.modifybalance(cardon.tax * -2, "pay tax and pay extra because you look good at math")
                    this.bankruptcheck()
                elif (this.race == Race.INDIAN and cardon.name == "Luxury Tax"):
                    this.modifybalance(cardon.tax * -3, "pay tax and pay extra extra because the clerk doesn't like Indians")
                    this.bankruptcheck()
                else:
                    this.modifybalance(cardon.tax * -1, "pay tax")
                    this.bankruptcheck()
            case 5:
                if (this.race == Race.ASIAN & cardon.name == "Free Parking"):
                    this.modifybalance(-100, "preemptive bad driving fine")
            case 6:
                if (this.race != Race.LATINO):
                    cardon.effect(this)
                else:
                    this.gameover("illegally deported back to Venezuela")
            case 7 | 8:
                cardon.effect(this)
                this.bankruptcheck()
            case 9:
                this.modifybalance(200, "landed on go")
        currentplayer = currentplayer.next
        preplayerturn(currentplayer.data)
    def gotojail(this):
        this.position = 99
        this.injail = True
        if(this.race == Race.BLACK):
            print("Police brutality has caused you to lose one of your properties.")
            lost = random.choice(this.properties)
            print(f"You have lost {lost.name}!")
            this.properties.remove(lost)
    def chance(this):
        print("Drawing Chance card...")
        time.sleep(2)
        cardid = random.randint(1, 16)
        match cardid:
            case 1:
                print("Advance to Mayfair")
                this.position = 39
                this.playerturn(0)
            case 2:
                print("Advance to Go")
                this.position = 0
                this.playerturn(0)
            case 3:
                print("Advance to Trafalgar Square")
                this.position = 24
                this.playerturn(0)
            case 4:
                print("Advance to Pall Mall")
                this.position = 11
                this.playerturn(0)
            case 5 | 6:
                print("Advance to the nearest station")
                this.position = int(this.position/10) + 5
                this.playerturn(0)
            case 7:
                print("Advance to the nearest utility")
                this.position = min(abs(28 - this.position), abs(12 - this.position))
                this.playerturn(0)
            case 8:
                print("Bank pays you dividend of $50")
                this.modifybalance(50, "chance")
            case 9:
                print("Get Out of Jail Free")
                this.gojfc += 1
            case 10:
                print("Go Back 3 Spaces")
                this.position -= 3
                this.playerturn(7)
            case 11:
                print("Go to jail. Go directly to jail.")
                this.gotojail()
            case 12:
                print("General repairs on all property. Pay $30 for each house.")
                i = 0
                for property in this.properties:
                    i += property.housesbuilt * 30
                this.modifybalance(i * -1, "chance")
            case 13:
                print("Speeding fine, $15")
                this.modifybalance(-15, "chance")
                this.bankruptcheck()
            case 14:
                print("Take a trip to King's Cross Station")
                this.position = 5
                this.playerturn(0)
            case 15:
                print("You have been elected Chairman of the Board. Pay each player $50")
                for player in player_list.traverse(1000):
                    if (player != this):
                        player.modifybalance(50, f"Dividends paid generously by {this.name}")
                this.modifybalance((len(player_list.traverse(1000)) - 1) * -50, "chance")
                this.bankruptcheck()
            case 16:
                print("Your building loan matures. Gain $150")
                this.modifybalance(150, "chance")
    def chest(this):
        print("Drawing Community Chest card...")
        time.sleep(2)
        cardid = random.randint(1, 16)
        match cardid:
            case 1:
                print("Advance to Go")
                this.position = 0
                this.playerturn(0)
            case 2:
                print("Bank error in your favor. Collect $200")
                this.modifybalance(200, "community chest")
            case 3:
                print("Doctor's fee. Pay $50")
                this.modifybalance(-50, "community chest")
                this.bankruptcheck()
            case 4:
                print("From sale of stock you get $50")
                this.modifybalance(50, "community chest")
            case 5:
                print("Get Out of Jail Free")
                this.gojfc += 1
            case 6:
                print("Go to jail. Go directly to jail.")
                this.gotojail()
            case 7:
                print("Holiday fund matures. Collect $100")
                this.modifybalance(100, "community chest")
            case 8:
                print("Income tax refund, collect $20")
                this.modifybalance(20, "community chest")
            case 9:
                print("It's your birthday. Collect $10 from every player")
                for player in player_list.traverse(1000):
                    if (player != this):
                        player.modifybalance(-10, f"Birthday gift for {this.name}")
                this.modifybalance((len(player_list.traverse(1000)) - 1) * 10, "community chest")
            case 10:
                print("Life insurance matures. Collect $100")
                this.modifybalance(100, "community chest")
            case 11:
                print("Pay hospital fees of $100")
                this.modifybalance(-100, "community chest")
                this.bankruptcheck()
            case 12:
                print("Pay school fees of $50")
                this.modifybalance(-50, "community chest")
                this.bankruptcheck()
            case 13:
                print("Recieve $25 consultancy fee")
                this.modifybalance(25, "community chest")
            case 14:
                print("Assessed for street repairs. Pay $60 for each house.")
                i = 0
                for property in this.properties:
                    i += property.housesbuilt * 60
                this.modifybalance(i * -1, "chance")
            case 15:
                print("You have won second prize in a beauty contest. Collect $10")
                this.modifybalance(10, "community chest")
            case 16:
                print("Inherit $100")
                this.modifybalance(100, "community chest")

    def modifybalance(this, amount, reason):
        if (this.race != Race.INDIAN):
            this.money = this.money + amount
            print(f"Modified balance of {this.name} by {amount}. Reason: {reason}")
            return(this.money)
        elif (amount > 0):
            this.money = this.money + 0.8 * amount
            print(f"Modified balance of {this.name} by {amount}. Reason: {reason} \nAs you are Indian, the banker took a look at you and waved his nose as if to dispell a curry smell. \n20% of your transaction has been voided due to racism.")
        else:
            this.money = this.money + 1.2 * amount
            print(f"Modified balance of {this.name} by {amount}. Reason: {reason} \nAs you are Indian, the banker thought you were reckless with your spending and decided to teach you a lesson by charging 20% more for your transaction.")
    def refreshrent(this, property):
            trainstations = []
            utilities = []
            trainstationrents = [25, 50, 100, 200]
            utilitymultis = [4, 10]
            if (property in this.properties):
                match property.cardtype.value:
                    case 1:
                        match property.set:
                            case Set.BROWN:
                                this.sortedproperties["Brown"].remove(property)
                            case Set.CYAN:
                                this.sortedproperties["Cyan"].remove(property)
                            case Set.PURPLE:
                                this.sortedproperties["Purple"].remove(property)
                            case Set.ORANGE:
                                this.sortedproperties["Orange"].remove(property)
                            case Set.RED:
                                this.sortedproperties["Red"].remove(property)
                            case Set.YELLOW:
                                this.sortedproperties["Yellow"].remove(property)
                            case Set.GREEN:
                                this.sortedproperties["Green"].remove(property)
                            case Set.BLUE:
                                this.sortedproperties["Blue"].remove(property)
                    case 2:
                        trainstations.remove(property)
                        this.sortedproperties["Railroads"].remove(property)
                    case 3:
                        utilities.remove(property)
                        this.sortedproperties["Utilities"].remove(property)
            else:
                match property.cardtype.value:
                    case 1:
                        match property.set:
                            case Set.BROWN:
                                this.sortedproperties["Brown"].append(property)
                            case Set.CYAN:
                                this.sortedproperties["Cyan"].append(property)
                            case Set.PURPLE:
                                this.sortedproperties["Purple"].append(property)
                            case Set.ORANGE:
                                this.sortedproperties["Orange"].append(property)
                            case Set.RED:
                                this.sortedproperties["Red"].append(property)
                            case Set.YELLOW:
                                this.sortedproperties["Yellow"].append(property)
                            case Set.GREEN:
                                this.sortedproperties["Green"].append(property)
                            case Set.BLUE:
                                this.sortedproperties["Blue"].append(property)
                    case 2:
                        trainstations.append(property)
                        this.sortedproperties["Railroads"].append(property)
                    case 3:
                        utilities.append(property)
                        this.sortedproperties["Utilities"].append(property)
            for trainstation in trainstations:
                trainstation.rent == trainstationrents[len(trainstations)]
            for utility in utilities:
                utility.multi == utilitymultis[len(utilities)]
    def bankruptcheck(this):
        if this.money >= 0:
            pass
        else:
            valuesum = 0
            for property in this.properties:
                valuesum += (property.value / 2)
            if (valuesum - this.money >= 0):
                while this.money < 0:
                    print("Your balance is below zero! Sell properties to get money.")
                    print("Type property name to sell the property. Type 'declarebankruptcy' to declare bankruptcy prematurely.")
                    for key in this.sortedproperties.keys():
                        if(len(this.sortedproperties[key]) > 0):
                            print (f" {key} Set:")
                            for property in this.sortedproperties[key]:
                                print(f" {property.name} - {property.value}")
                    a = input("\n")
                    match a:
                        case 'declarebankruptcy':
                            this.gameover("declared bankruptcy")
                        case propertyname:
                            matched = False
                            for property in this.properties:
                                if (property.name == propertyname):
                                    property.sell()
                                    matched = True
                                    break
                            if (matched == False):
                                print("No match found, please try again")
            else:
                this.gameover("went bankrupt")
    def gameover(this, reason):
        print(f"Player {this.name} has lost the game. Reason: {reason}")
        player_list.deleteat(player_list.findnode(this))
    def jailedplayerturn(this):
        this.turnsinjail += 1
        if(this.turnsinjail >= 3 and this.race != Race.BLACK):
            this.injailseq()
        elif(this.turnsinjail >= 15):
            this.injailseq
        else:
            print("You have served your sentence and may go free.")
            this.injail = False
            this.turnsinjail = 0
            this.rolldice()
    def injailseq(this):
            a = input(f"YOU ARE IN JAIL. You have served {this.turnsinjail} turns of your sentence so far. \n1 to roll doubles to try to escape (if applicable) \n2 to bribe your way out ($50) \n3 to use your Get Out of Jail Free card (if applicable) \n9 to end turn\n")
            match(a):
                case '1':
                        if (this.race != Race.BLACK):
                            random.seed()
                            dice1 = random.randint(1, 6)
                            dice2 = random.randint(1, 6)
                            print("Rolling dice...")
                            time.sleep(1)
                            print (f"Dice 1: {dice1}")
                            print (f"Dice 2: {dice2}")
                            if dice1 == dice2:
                                print ("You rolled doubles. You are now free.")
                                this.injail = False
                                this.turnsinjail = 0
                                this.rolldice()
                            else:
                                print ("You failed to roll doubles. You have been caught and your turn has been automatically ended.")
                                currentplayer = currentplayer.next
                                preplayerturn(currentplayer.data)
                        if (this.race != Race.BLACK):
                            print("You cannot attempt to escape as one of the officers has an eye on you at all times.")
                case '2':
                    if (this.race != Race.BLACK):
                        if(this.money > 50):
                            this.modifybalance(-50, "bribe prison officials")
                            print("You will be released next turn.")
                            this.injail = False
                            this.turnsinjail = 0
                        else:
                            print("You do not have enough money!")
                    else:
                        if(this.money > 500):
                            this.modifybalance(-500, "bribe racist prison officials")
                            print("You will be released next turn. You paid 10x more before they would finally let you go.")
                            this.injail = False
                            this.turnsinjail = 0
                        else:
                            print("You do not have enough money! As a black person, you need 500 dollars to bribe officials as they are far more averse to taking bribes from blacks.")
                case '3':
                    if(this.gojfc >= 1):
                        this.gojfc -= 1
                        print("You have used your Get Out of Jail Free card. You are now free.")
                        this.injail = False
                        this.turnsinjail = 0
                        this.rolldice()
                    else:
                        print("You have no such card.")
                        this.injailseq()
                case '9':
                    currentplayer = currentplayer.next
                    preplayerturn(currentplayer.data)
#too much effort to implement
'''            for key in this.sortedproperties.keys():3
                this.fullsetbonus(key, sp2[key].pop(0), sp2)
    def fullsetbonus(this, color, number, sp):
        if (sp[color].len() >= number):
            for property in sp[color:
                property.rent = property.rent*2
                property.remove
        else
        
'''             
#define statics
emptyplayer = Player("Empty", Race.PLACEHOLDER)
class Card:
    cardtype = CardType.PLACEHOLDER
    owner = emptyplayer
    housesbuilt = 0
    rentbase = [1, 4, 12, 28, 34, 40]
    value = 0
    def __init__(this, cardtype, name, space, **kwargs):
        b = kwargs.get('b', None)
        c = kwargs.get('c', None)
        this.cardtype = cardtype
        this.name = name
        match cardtype.value:
            case 1:
                this.price = b
                this.set = c
                this.rent = this.set.value
                this.value = this.price
                match this.set:
                    case Set.BROWN | Set.CYAN:
                        this.houseprice = 50
                    case Set.PURPLE | Set.ORANGE:
                        this.houseprice = 100
                    case Set.RED | Set.YELLOW:
                        this.houseprice = 150
                    case Set.GREEN | Set.BLUE:
                        this.houseprice = 200
            case 3:
                this.multi = 4
                this.price = 150
                this.value = this.price
            case 2:
                this.rent = 25
                this.price = 200
                this.value = this.price
            case 4:
                this.tax = b
            case 6:
                #5 is empty
                this.effect=Player.gotojail
            case 7:
                this.effect=Player.chance
            case 8:
                this.effect=Player.chest
                #logic of 9 is determined in turn code
    def gettype(this):
        return(this.cardtype)
    def sell(this, player):
        if (player == this.owner):
            this.owner = emptyplayer
            sellprice = int((this.price + (this.houseprice * this.housesbuilt))/2)
            player.modifybalance(sellprice, "sold property")
            player.refreshrent(this)
            player.properties.remove(this)
            this.value = this.price
            this.housesbuilt = 0
            if (this.cardtype == CardType.PROPERTY):
                this.rent = this.set.value
        else:
            print("You don't own that property!")
        
    def construct_house (this, player):
            if (player.race != Race.INDIGENOUS):
                if (player.money >= this.houseprice and player == this.owner and this.housesbuilt < 5 and player.builthousethisturn == False):
                    player.modifybalance(this.houseprice * -1, "built house")
                    this.housesbuilt += 1
                    this.rent = this.set.value * this.rentbase[this.housesbuilt]
                    this.value += this.houseprice
                else:
                    print("Building not successful. Balance has not been deducted.")
            else:
                if (player.money >= this.houseprice and player == this.owner and this.housesbuilt < 3 and player.builthousethisturn == False):
                    player.modifybalance(this.houseprice * -1, "built house")
                    this.housesbuilt += 1
                    this.rent = this.set.value * this.rentbase[this.housesbuilt]
                    this.value += this.houseprice
                elif (this.housesbuilt == 3):
                    print("The council won't approve any denser building plans because they don't trust indigenous people to be able to build competently.")
                else:
                    print("Building not successful. Balance has not been deducted.")

    def buy(this, player):
        if (this.owner == emptyplayer):
            if (player.race != Race.BLACK):
                if (player.money > this.price):
                    player.modifybalance(this.price * -1, "bought property")
                    player.refreshrent(this)
                    player.properties.append(this)
                    player.builthousethisturn = True
                    this.owner = player
                else:
                    print("Not enough money!")
            else:
                if (player.money > this.price * 2):
                    player.modifybalance(this.price * -2, "bought property at double the cost due to archaic racist laws")
                    player.refreshrent(this)
                    player.properties.append(this)
                    player.builthousethisturn = True
                    this.owner = player
                else:
                    print("Not enough money!")
        else:
            print("Someone else already owns this card!")
# card data
class Cards:
    go = Card(CardType.GO, "GO", 1)
    okr = Card(CardType.PROPERTY, "Old Kent Road", 2, b=60, c=Set.BROWN)
    chest1 = Card(CardType.COMMUNITYCHEST, "Community Chest Card", 3)
    wchr = Card(CardType.PROPERTY, "Whitechapel Road", 4, b=60, c=Set.BROWN)
    itax = Card(CardType.TAX, "Income Tax", 5, b=200)
    kcs = Card(CardType.RAILROAD, "King's Cross Station", 6)
    tai = Card(CardType.PROPERTY, "The Angel, Islington", 7, b=100, c=Set.CYAN)
    chance1 = Card(CardType.CHANCE, "Chance Card", 8)
    er = Card(CardType.PROPERTY, "Euston Road", 9, b=100, c=Set.CYAN)
    pvr = Card(CardType.PROPERTY, "Pentonville Road", 10, b=120, c=Set.CYAN)
    jail = Card(CardType.FREE, "Just Visiting/Jail", 11)
    pm = Card(CardType.PROPERTY, "Pall Mall", 12, b=140, c=Set.PURPLE)
    ecomp = Card(CardType.UTILITY, "Electric Company", 13)
    wh = Card(CardType.PROPERTY, "Whitehall", 14, b=140, c=Set.PURPLE)
    nta = Card(CardType.PROPERTY, "Northumb'nd Avenue", 15, b=160, c=Set.PURPLE)
    mbs = Card(CardType.RAILROAD, "Marylebone Station", 16)
    bs = Card(CardType.PROPERTY, "Bow Street", 17, b=180, c=Set.ORANGE)
    chest2 = Card(CardType.COMMUNITYCHEST, "Community Chest Card", 18)
    gms = Card(CardType.PROPERTY, "Great Marlborough Street", 19, b=180, c=Set.ORANGE)
    vs = Card(CardType.PROPERTY, "Vine Street", 20, b=200, c=Set.ORANGE)
    fp = Card(CardType.FREE, "Free Parking", 21)
    str = Card(CardType.PROPERTY, "Strand", 22, b=220, c=Set.RED)
    chance2 = Card(CardType.CHANCE, "Chance Card", 23)
    fs = Card(CardType.PROPERTY, "Fleet Street", 24, b=220, c=Set.RED)
    ts = Card(CardType.PROPERTY, "Trafalgar Square", 25, b=240, c=Set.RED)
    fss = Card(CardType.RAILROAD, "Fenchurch St. Station", 26)
    ls = Card(CardType.PROPERTY, "Leicester Square", 27, b=260, c=Set.YELLOW)
    cos = Card(CardType.PROPERTY, "Coventry Street", 28, b=260, c=Set.YELLOW)
    water = Card(CardType.UTILITY, "Water Works", 29)
    picady = Card(CardType.PROPERTY, "Piccadilly", 30, b=280, c=Set.YELLOW)
    gotojail = Card(CardType.GOTOJAIL, "GO TO JAIL", 31)
    rgs = Card(CardType.PROPERTY, "Regent Street", 32, b=300, c=Set.GREEN)
    oxst = Card(CardType.PROPERTY, "Oxford Street", 33, b=300, c=Set.GREEN)
    community3 = Card(CardType.COMMUNITYCHEST, "Community Chest Card", 34)
    bos = Card(CardType.PROPERTY, "Bond Street", 35, b=320, c=Set.GREEN)
    lsst = Card(CardType.RAILROAD, "Liverpool St. Station", 36)
    chance3 = Card(CardType.CHANCE, "Chance Card", 37)
    pkln = Card(CardType.PROPERTY, "Park Lane", 38, b=350, c=Set.BLUE)
    suptx = Card(CardType.TAX, "Luxury Tax", 39, b=100)
    mayfr = Card(CardType.PROPERTY, "Mayfair", 40, b=400, c=Set.BLUE)

    board = [go, okr, chest1, wchr, itax, kcs, tai, chance1, er, pvr, jail, pm, ecomp, wh, nta, mbs, bs, chest2, gms, vs, fp, str, chance2, fs, ts, fss, ls, cos, water, picady, gotojail, rgs, oxst, community3, bos, lsst, chance3, pkln, suptx, mayfr]


        
# define modules
def clearconsole():
    os.system("cls" if os.name == "nt" else "clear")

def tokenselect(player_name_list):
    tokens = [Race.ASIAN, Race.BLACK, Race.INDIAN, Race.INDIGENOUS, Race.WHITE, Race.LATINO]
    print("\nToken assignments:")
    player_list = scll.SingularCircularLinkedList()
    for player in player_name_list:
        if tokens:
            race = random.choice(tokens)
            print(f"Player {player} got the token {race.name}!")
            player_list.append(Player(player, race))
    currentplayer = player_list.getnodeat(0)
    preplayerturn(currentplayer.data)
            #Allow duplicates
def preplayerturn(player):
    #ORDER OF TURN
    #preplayerturn -> rolldice -> move -> playerturn -> postplayerturn
    if (player.injail == False):
        if (len(player_list.traverse(1000)) != 1):
            print(f"\n{player}'s turn")
            i = input("Press N to roll dice \n")
            if i != "n":
                print ("Please press N to roll dice")
                preplayerturn(player)
            else:
                player.rolldice()
        else:
            print(f"{player_list.getnodeat(0)} has won with {len(player.properties)} properties and {player.money} dollars.")
    else:
        player.jailedplayerturn()

def gamestart():
    print("Welcome everyone, it is time for the grand token selection. Each player is given a token with which they \nare either given perks or unhappiness.")
    print("This is the part that will determine your fate in the Game of Inequality.")
    tokenselect(player_name_list)

# mainline
print("************************************************************")
print("---------- Abhijith Madhavan and Uno Wong present: ---------")
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
    elif nameno > 6:
        print("Too many players!")
        continue
    player_name_list = []
    for i in range(nameno):
        name = input(f"Select a name for the player {i + 1} \n")
        player_name_list.append(name)
    
    for i, name in enumerate(player_name_list):
        print(f"Player {i + 1}: {name}")
    print("Starting game...")
    gamestart()