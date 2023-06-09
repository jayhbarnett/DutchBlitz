import random
import pygame



class Card:
    def __init__(self, colour, value):
        self.colour = colour
        self.value = value
    
    def to_list(self):
        return [self.colour, self.value]

class Player:
    def __init__(self):
        self.hand = self.createCards()
        self.blitz = self.createBlitz()
        self.front3 = self.createFront3()
        self.flipped = []  
        self.score = 0
        self.piles = []
        for i in range(16):
            self.piles.append([])
            i+=1

    def getHand(self):
        return self.hand

    def getBlitz(self):
        return self.blitz

    def getFront3(self):
        return self.front3
    
    def getFlipped(self):
        return self.flipped
    
    def getPiles(self):
        return self.piles

    def flip(self):
        if len(self.hand) >= 3:
            for i in range(3):
                self.flipped.append(self.hand.pop())
        else:
            for i in range(len(self.hand)):
                self.flipped.append(self.hand.pop())
        print(len(self.hand))


    def mergeDecks(self):
        self.hand = self.flipped[::-1]
        self.flipped = []
        print("merged")

    def useFront3(self,pos):
        used = self.front3[pos]
        self.front3[pos] = self.blitz.pop()
        
        return used
        

    def addToScore(self):
        self.score += (40-len(self.hand)-len(self.flipped)-len(self.front3)-len(self.blitz))-2*len(self.blitz)
        return self.score
    
    def addToPile(self):
        return self.flipped.pop()
    
    def playCard(self,pileIndex,index,fromFlipped):
        pileLen = 0
        if len(self.piles[pileIndex])>0:
            pileLen = len(self.piles[pileIndex])-1
        # if fromFlipped:
        if cardToPlace.value == 1:
            if len(self.piles[pileIndex]) == 0:
                if fromFlipped:
                    self.piles[pileIndex].append(self.addToPile())
                else:
                    self.piles[pileIndex].append(self.useFront3(index))
                print("lol")
        else:
            
            print(pileLen)
            
            if(self.piles[pileIndex][pileLen].colour == cardToPlace.colour and self.piles[pileIndex][pileLen].value == cardToPlace.value-1):
                if fromFlipped:
                    self.piles[pileIndex].append(self.addToPile())
                else:
                    self.piles[pileIndex].append(self.useFront3(index))
                print("hi")


        
        
    def createCards(self):
        colours =["red", "yellow", "green", "blue"]
        hand =[]
        for colour in colours:
            for i in range(1,11):
                card = Card(colour, i)
                hand.append(card)
        
        random.shuffle(hand)
        return hand


    def createBlitz(self):
        blitz = self.hand[:10]
        del self.hand[:10]
        return blitz

    def createFront3(self):
        front3 = self.hand[:3]
        del self.hand[:3]
        return front3

player1 = Player()


pygame.init()


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
                if len(player1.getHand()) > 0:
                    player1.flip()
                else:
                    player1.mergeDecks()

            #If a card from the flipped pile is chosen
            if flipped_rect_x < event.pos[0] < flipped_rect_x + rect_width and flipped_rect_y < event.pos[1] < flipped_rect_y + rect_height:
                cardToPlace = player1.getFlipped()[len(player1.getFlipped())-1]
                fromFlipped = True
                print (cardToPlace.colour + " "+ str(cardToPlace.value))

            #If a card from front 3 is chosen
            for i in range(3):
                if front3_rect_x +i*(20+rect_width)< event.pos[0] < front3_rect_x + rect_width +i*(20+rect_width)and flipped_rect_y < event.pos[1] < flipped_rect_y + rect_height:
                    cardToPlace = player1.getFront3()[i]
                    fromFlipped= False
                    index = i
                    print (cardToPlace.colour + " "+ str(cardToPlace.value))
           

            #When a playing pile is chosen
            for i in range(16):
                x = i%6
                if i > 11:
                    x+=1

                if i<6:
                    y = 0
                elif i>6 and i<12:
                    y = 1
                else:
                    y = 2

                if pile_rect_x + x*(20 + rect_width)< event.pos[0] < pile_rect_x + rect_width+ x*(20 + rect_width) and pile_rect_y +y*(20 + rect_height)< event.pos[1] < pile_rect_y + rect_height+y*(20 + rect_height):
                    pileIndex = i
                    print(pileIndex)
                    if cardToPlace != None:
                        if cardToPlace.value == 1:
                            player1.playCard(pileIndex,index,fromFlipped)
                        elif len(player1.getPiles()[pileIndex]) > 0:
                            player1.playCard(pileIndex,index,fromFlipped)
                    cardToPlace = None
                    fromFlipped = None
                    index = None    

           


    screen.fill((255, 255, 255))

    for card in player1.getBlitz():

        pygame.draw.rect(screen, card.colour, (blitz_rect_x, blitz_rect_y, rect_width, rect_height))

        # Render the label text
        label = font.render(str(card.value), True, 'black')
        label_rect = label.get_rect(centerx=blitz_rect_x + rect_width // 2, centery=blitz_rect_y + rect_height // 2)
        
        screen.blit(label, label_rect)
        blitz_rect_x += 1

    if len(player1.getFlipped()) > 0:
        for card in player1.getFlipped():

            pygame.draw.rect(screen, card.colour, (flipped_rect_x, flipped_rect_y, rect_width, rect_height))

            # Render the label text
            label = font.render(str(card.value), True, 'black')
            label_rect = label.get_rect(centerx=flipped_rect_x + rect_width // 2, centery=flipped_rect_y + rect_height // 2)
            screen.blit(label, label_rect)

    for card in player1.getFront3():

        pygame.draw.rect(screen, card.colour, (front3_rect_x, flipped_rect_y, rect_width, rect_height))

        # Render the label text
        label = font.render(str(card.value), True, 'black')
        label_rect = label.get_rect(centerx=front3_rect_x + rect_width // 2, centery=flipped_rect_y + rect_height // 2)
        screen.blit(label, label_rect)
        front3_rect_x += rect_width+20

    for card in player1.getHand():
        if len(player1.getHand())>0:

            pygame.draw.rect(screen, 'grey', (hand_rect_x, flipped_rect_y, rect_width, rect_height))

    count = 0
    for pile in player1.getPiles():
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


