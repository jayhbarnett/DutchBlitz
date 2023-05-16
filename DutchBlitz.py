import random
import pygame
#hello


class Card:
    def __init__(self, colour, value):
        self.colour = colour
        self.value = value
    
    def to_list(self):
        return [self.colour, self.value]

class Player:
    def __init__(self):
        self.hand = createCards()
        self.blitz = createBlitz(self.hand)
        self.front3 = createFront3(self.hand)
        self.flipped = []  
        self.score = 0

    def getHand(self):
        return self.hand

    def getBlitz(self):
        return self.blitz

    def getFront3(self):
        return self.front3
    
    def getFlipped(self):
        return self.flipped

    def printCards(self):
        hand = self.getHand()
        blitz = self.getBlitz()
        front3 = self.getFront3()
        print("hand")
        print(len(hand))

        for card in hand:
            print(card.to_list())

        print("blitz")
        print(len(blitz))

        for card in blitz:
            print(card.to_list())

        print("front 3")
        print(len(front3))

        for card in front3:
            print(card.to_list())

    def flip(self):
        if len(self.hand) >= 3:
            for i in range(3):
                self.flipped.append(self.hand.pop())
        else:
            for i in range(len(self.hand)):
                self.flipped.append(self.hand.pop())
        print(len(self.hand))


        for card in self.flipped:
            print(card.to_list())

    def mergeDecks(self):
        self.hand = self.flipped[::-1]
        self.flipped = []
        print("merged")

    def useFront3(self,pos):
        used = self.front3[pos]
        self.front3[pos] = self.blitz.pop()
        print("blitz")
        print(len(self.blitz))

        for card in self.blitz:
            print(card.to_list())

        print("front 3")
        print(len(self.front3))

        for card in self.front3:
            print(card.to_list())
        
        return used
        

    def addToScore(self):
        self.score += (40-len(self.hand)-len(self.flipped)-len(self.front3)-len(self.blitz))-2*len(self.blitz)
        return self.score
    
    def addToPile(self):
        return self.flipped.pop()


        
        
def createCards():
    colours =["red", "yellow", "green", "blue"]
    hand =[]
    for colour in colours:
        for i in range(1,11):
            card = Card(colour, i)
            hand.append(card)
    
    random.shuffle(hand)
    return hand


def createBlitz(hand):
    blitz = hand[:10]
    del hand[:10]
    return blitz

def createFront3(hand):
    front3 = hand[:3]
    del hand[:3]
    return front3

jay = Player()
jay.printCards()
print("flipped")
#jay.flip()
print("flipped")
#jay.flip()
jay.useFront3(0)
#jay.addToPile()
print("flipped")
#jay.flip()
print(jay.addToScore())
#jay.mergeDecks()

pygame.init()
piles = []
for i in range(16):
    piles.append([])
    i+=1

screen_width = 750
screen_height = 750
screen = pygame.display.set_mode((screen_width,screen_height))

rect_width = 100
rect_height = 150
blitz_rect_x = 10
blitz_rect_y = screen_height - rect_height-10
flipped_rect_x = screen_width - rect_width -10
flipped_rect_y = screen_height - rect_height-10
front3_rect_x = blitz_rect_x+ rect_width +20
hand_rect_x = flipped_rect_x - rect_width- 20
pile_rect_x = 20
pile_rect_y = 10

# Define the label text and font
def playCard():
    pileLen = 0
    if len(piles[pileIndex])>0:
        pileLen = len(piles[pileIndex])-1
    if fromFlipped:
        if cardToPlace.value == 1:
            if len(piles[pileIndex]) == 0:
                piles[pileIndex].append(jay.addToPile())
                print("lol")
        else:
            
            print(pileLen)
            
            if(piles[pileIndex][pileLen].colour == cardToPlace.colour and piles[pileIndex][pileLen].value == cardToPlace.value-1):
                piles[pileIndex].append(jay.addToPile())
                print("hi")
    else:
        if cardToPlace.value == 1:
            if len(piles[pileIndex]) == 0:
                piles[pileIndex].append(jay.useFront3(index))
                print("loll")
        else:
           print(pileLen)
           if(piles[pileIndex][pileLen].colour == cardToPlace.colour and piles[pileIndex][pileLen].value == cardToPlace.value-1):
                piles[pileIndex].append(jay.useFront3(index))
                print("hii")


font_size = 50
font = pygame.font.Font(None, font_size)

running = True
cardToPlace = None
fromFlipped = None
index = None
pileIndex = None
while running:
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click falls within the rectangle
            if hand_rect_x < event.pos[0] < hand_rect_x + rect_width and flipped_rect_y < event.pos[1] < flipped_rect_y + rect_height:
                if len(jay.getHand()) > 0:
                    jay.flip()
                else:
                    jay.mergeDecks()
            if flipped_rect_x < event.pos[0] < flipped_rect_x + rect_width and flipped_rect_y < event.pos[1] < flipped_rect_y + rect_height:
                cardToPlace = jay.getFlipped()[len(jay.getFlipped())-1]
                fromFlipped = True
                print (cardToPlace.colour + " "+ str(cardToPlace.value))
            if front3_rect_x < event.pos[0] < front3_rect_x + rect_width and flipped_rect_y < event.pos[1] < flipped_rect_y + rect_height:
                cardToPlace = jay.getFront3()[0]
                fromFlipped= False
                index = 0
                print (cardToPlace.colour + " "+ str(cardToPlace.value))
            if front3_rect_x + 20 + rect_width < event.pos[0] < front3_rect_x + rect_width + 20 + rect_width and flipped_rect_y < event.pos[1] < flipped_rect_y + rect_height:
                cardToPlace = jay.getFront3()[1]
                index = 1
                fromFlipped= False
                print (cardToPlace.colour + " "+ str(cardToPlace.value))
            if front3_rect_x + 20 + rect_width + 20 + rect_width < event.pos[0] < front3_rect_x + rect_width + 20 + rect_width + 20 + rect_width and flipped_rect_y < event.pos[1] < flipped_rect_y + rect_height:
                cardToPlace = jay.getFront3()[2]
                fromFlipped= False
                index = 2
                print (cardToPlace.colour + " "+ str(cardToPlace.value))

            if pile_rect_x < event.pos[0] < pile_rect_x + rect_width and pile_rect_y < event.pos[1] < pile_rect_y + rect_height:
                pileIndex = 0
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
                

            if pile_rect_x + 20 + rect_width< event.pos[0] < pile_rect_x + rect_width+ 20 + rect_width and pile_rect_y < event.pos[1] < pile_rect_y + rect_height:
                pileIndex = 1
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 2*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 2*(20 + rect_width) and pile_rect_y < event.pos[1] < pile_rect_y + rect_height:
                pileIndex = 2
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 3*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 3*(20 + rect_width) and pile_rect_y < event.pos[1] < pile_rect_y + rect_height:
                pileIndex = 3
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 4*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 4*(20 + rect_width) and pile_rect_y < event.pos[1] < pile_rect_y + rect_height:
                pileIndex = 4
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 5*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 5*(20 + rect_width) and pile_rect_y < event.pos[1] < pile_rect_y + rect_height:
                pileIndex = 5
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None

            if pile_rect_x < event.pos[0] < pile_rect_x + rect_width and pile_rect_y +20 + rect_height < event.pos[1] < pile_rect_y + rect_height+20 + rect_height:
                pileIndex = 6
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None

            if pile_rect_x + 20 + rect_width< event.pos[0] < pile_rect_x + rect_width+ 20 + rect_width and pile_rect_y +20 + rect_height < event.pos[1] < pile_rect_y + rect_height + 20 + rect_height:
                pileIndex = 7
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 2*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 2*(20 + rect_width) and pile_rect_y +20 + rect_height< event.pos[1] < pile_rect_y + rect_height+20 + rect_height:
                pileIndex = 8
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 3*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 3*(20 + rect_width) and pile_rect_y +20 + rect_height< event.pos[1] < pile_rect_y + rect_height+20 + rect_height:
                pileIndex = 9
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 4*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 4*(20 + rect_width) and pile_rect_y +20 + rect_height< event.pos[1] < pile_rect_y + rect_height+20 + rect_height:
                pileIndex = 10
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 5*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 5*(20 + rect_width) and pile_rect_y +20 + rect_height< event.pos[1] < pile_rect_y + rect_height+20 + rect_height:
                pileIndex = 11
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None

            if pile_rect_x + 20 + rect_width< event.pos[0] < pile_rect_x + rect_width+ 20 + rect_width and pile_rect_y +2*(20 + rect_height) < event.pos[1] < pile_rect_y + rect_height + 2*(20 + rect_height):
                pileIndex = 12
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 2*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 2*(20 + rect_width) and pile_rect_y +2*(20 + rect_height)< event.pos[1] < pile_rect_y + rect_height+2*(20 + rect_height):
                pileIndex = 13
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 3*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 3*(20 + rect_width) and pile_rect_y +2*(20 + rect_height)< event.pos[1] < pile_rect_y + rect_height+2*(20 + rect_height):
                pileIndex = 14
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None
            if pile_rect_x + 4*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ 4*(20 + rect_width) and pile_rect_y +2*(20 + rect_height)< event.pos[1] < pile_rect_y + rect_height+2*(20 + rect_height):
                pileIndex = 15
                print(pileIndex)
                if cardToPlace != None:
                    if cardToPlace.value == 1:
                        playCard()
                    elif len(piles[pileIndex]) > 0:
                        playCard()
                cardToPlace = None
                fromFlipped = None
                index = None


    screen.fill((255, 255, 255))

    for card in jay.getBlitz():

        pygame.draw.rect(screen, card.colour, (blitz_rect_x, blitz_rect_y, rect_width, rect_height))

        # Render the label text
        label = font.render(str(card.value), True, 'black')
        label_rect = label.get_rect(centerx=blitz_rect_x + rect_width // 2, centery=blitz_rect_y + rect_height // 2)
        
        screen.blit(label, label_rect)
        blitz_rect_x += 1

    if len(jay.getFlipped()) > 0:
        for card in jay.getFlipped():

            pygame.draw.rect(screen, card.colour, (flipped_rect_x, flipped_rect_y, rect_width, rect_height))

            # Render the label text
            label = font.render(str(card.value), True, 'black')
            label_rect = label.get_rect(centerx=flipped_rect_x + rect_width // 2, centery=flipped_rect_y + rect_height // 2)
            screen.blit(label, label_rect)

    for card in jay.getFront3():

        pygame.draw.rect(screen, card.colour, (front3_rect_x, flipped_rect_y, rect_width, rect_height))

        # Render the label text
        label = font.render(str(card.value), True, 'black')
        label_rect = label.get_rect(centerx=front3_rect_x + rect_width // 2, centery=flipped_rect_y + rect_height // 2)
        screen.blit(label, label_rect)
        front3_rect_x += rect_width+20

    for card in jay.getHand():
        if len(jay.getHand())>0:

            pygame.draw.rect(screen, 'grey', (hand_rect_x, flipped_rect_y, rect_width, rect_height))

    count = 0
    for pile in piles:
        if len(pile)> 0:
             
            pygame.draw.rect(screen, pile[len(pile)-1].colour, (pile_rect_x, pile_rect_y, rect_width, rect_height))

            # Render the label text
            label = font.render(str(pile[len(pile)-1].value), True, 'black')
            label_rect = label.get_rect(centerx=pile_rect_x + rect_width // 2, centery=pile_rect_y + rect_height // 2)
            screen.blit(label, label_rect)
        else:
            pygame.draw.rect(screen, 'grey', (pile_rect_x, pile_rect_y, rect_width, rect_height))
        count += 1
        if count%6 == 0 and count%12 != 0:
            pile_rect_y += rect_height + 20
            pile_rect_x = 20
        elif count%12 ==0:
            pile_rect_y += rect_height+20
            pile_rect_x = 20 + rect_width+20
        else:
            pile_rect_x += rect_width+20

        

        
        
        
    front3_rect_x = 140
    blitz_rect_x = 10
    pile_rect_x = 20
    pile_rect_y = 10

    
    pygame.display.update()

pygame.quit()


