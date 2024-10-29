#!/usr/bin/python

PASSWORD_CARD = [
'SQUIRELL*JUDGE*NEWS*LESSON',
'WORRY*UPDATE*SEAFOOD*CROSS',
'CHAPTER*SPEEDBUMP*CHECKERS',
'PHONE*HOPE*NOTEBOOK*ORANGE',
'CARTOONS*CLEAN*TODAY*ENTER',
'ZEBRA*PATH*VALUABLE*MARINE',
'VOLUME*REDUCE*LETTUCE*GOAL',
'BUFFALOS*THE*CATCH*SUPREME',
'LONG*OCTOPUS*SEASON*SCHEME',
'CARAVAN*TOBACCO*WORM*XENON',
'PUPPYLIKE*WHATEVER*POPULAR',
'SALAD*UNKNOWN*SQUATS*AUDIT',
'HOUR*NEWBORN*TURN*WORKSHOP',
'USEFUL*OFFSHORE*TOAST*BOOK',
'COMPANY*FREQUENCY*NINETEEN',
'AMOUNT*CREATE*HOUSE*FOREST',
'BATTERY*GOLDEN*ROOT*WHEELS',
'SHEEP*HOLIDAY*APPLE*LAWYER',
'SUMMER*HORSE*WATER*SULPHUR'
]

PW_LIMIT = 18

with open('dict_list.txt', 'w') as f:
    for i in PASSWORD_CARD:
        for j in range(len(i)-PW_LIMIT+1):
            f.write(i[j:j+PW_LIMIT] + '\n')
            f.write(i[::-1][j:j+PW_LIMIT] + '\n')

    for i in range(len(PASSWORD_CARD) - PW_LIMIT+1):
        for j in range(len(PASSWORD_CARD[0])):
            pw = ''
            for k in range(PW_LIMIT):
                pw += PASSWORD_CARD[i+k][j]
            f.write(pw + '\n')
            f.write(pw[::-1] + '\n')

    for i in range(len(PASSWORD_CARD) - PW_LIMIT+1):
        for j in range(len(PASSWORD_CARD[0]) - PW_LIMIT+1):
            pw = ''
            y = i
            x = j
            while len(pw) != PW_LIMIT:
                pw += PASSWORD_CARD[y][x]
                y += 1
                x += 1
            f.write(pw + '\n')
            f.write(pw[::-1] + '\n')

    for i in range(len(PASSWORD_CARD) - (len(PASSWORD_CARD)-PW_LIMIT)-1, len(PASSWORD_CARD)):
        for j in range(len(PASSWORD_CARD[0]) - PW_LIMIT+1):
            pw = ''
            y = i
            x = j
            while len(pw) != PW_LIMIT:
                pw += PASSWORD_CARD[y][x]
                y -= 1
                x += 1
            f.write(pw + '\n')
            f.write(pw[::-1] + '\n')
