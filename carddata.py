import GameofInequality as main
class Cards:
    go = main.Card(main.CardType.GO, "Go")
    mave = main.Card(main.CardType.PROPERTY, "Mediterranean Avenue", b=40, c=main.Set.BROWN)
    chest = main.Card(main.CardType.COMMUNITYCHEST, "Community Chest")
    bave = main.Card(main.CardType.PROPERTY, "Baltic Avenue", b=60, c=main.Set.BROWN)
    itax = main.Card(main.CardType.TAX, "Income Tax", b=200)
    rrail = main.Card(main.CardType.RAILROAD, "Reading Railroad")
    oave = main.Card(main.CardType.PROPERTY, "Oriental Avenue", b=100, c=main.Set.CYAN)
    chance = main.Card(main.CardType.CHANCE, "Chance")
    vave = main.Card(main.CardType.PROPERTY, "Vermont Avenue", b=100, c=main.Set.CYAN)
    cave = main.Card(main.CardType.PROPERTY, "Conneticut Avenue", b=120, c=main.Set.CYAN)
    jvail = main.Card(main.CardType.FREE, "Just Visiting/Jail")
    scpl = main.Card(main.CardType.PROPERTY, "St Charles Place", b=140, c=main.Set.PURPLE)
    elec = main.Card(main.CardType.UTILITY, "Electric Company")
    save =  main.Card(main.CardType.PROPERTY, "States Avenue", b=140, c=main.Set.PURPLE)
    viave = main.Card(main.CardType.PROPERTY, "Virginia Avenue", b=160, c=main.Set.PURPLE)
    
    board = [go, mave, chest, bave, itax, rrail, oave, chance, vave, cave, jvail, scpl, elec, save, viave, ]