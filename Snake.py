import pygame
import random
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (211, 211, 211)
MAROON = (128,0,0)
YELLOW = (237,223,26)
BLUE = (26,237,213)
PINK = (245,54,194)
IJO = (180,240,103)
# Set the width and height of each snake segment
segment_width = 20
segment_height = 20
# Margin between each segment
segment_margin = 5
# Set initial speed
x_change = segment_width + segment_margin
y_change = 0
WALL_THICKNESS = 25
DEFAULT_FONT = 'freesansbold.ttf'
 
class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y, color):
        # Call the parent's constructor
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(color)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def check_collision(self, sprite1):
        return pygame.sprite.collide_rect(self, sprite1)
 
# Create an initial snake
class Snake:
    def __init__(self,length,color):
        super().__init__()
        self.allspriteslist = pygame.sprite.Group()
        self.snake_segments = []
        self.length = length
        self.color=color
        for i in range(self.length):
            x = 350 - (segment_width + segment_margin) * i
            y = 250
            segment = Segment(x, y,self.color)
            self.snake_segments.append(segment)
            self.allspriteslist.add(segment)
            
    def add_segment(self, x, y, index=None) :
        if index is None:
            index = self.length
        segment = Segment(x, y,self.color)
        self.snake_segments.insert(index, segment)
        self.length += 1
    def Head(self):
        return (self.snake_segments[0])
    def Tail(self):
        return (self.snake_segments[1:])
    def move(self,X,Y):
        #Get rid of last segment of the snake
        #pop() command removes last item in list
        old_segment = self.snake_segments.pop()
        self.last_removed = old_segment
        self.allspriteslist.remove(old_segment)
        #Figure out where new segment will be
        x = self.snake_segments[0].rect.x + X
        y = self.snake_segments[0].rect.y + Y
        if x > 800 :
            x = 0
        if x < 0 :
            x = 800
        if y > 600 :
            y = 25
        if y < 25 :
            y = 600
        segment = Segment(x, y,self.color)
        #Insert new segment into the list
        self.snake_segments.insert(0, segment)
        self.allspriteslist.add(segment)
        
    def collides(self, sprite1):
        #Only head will be colliding with other sprite
        return self.Head().check_collision(sprite1)
    def collides_any(self, group):
        for sprite in group:
            if self.collides(sprite):
                return True
        return False
    def grow(self):
        self.add_segment(self.last_removed.rect.x, self.last_removed.rect.y)

class Food(pygame.sprite.Sprite):
    def __init__(self, x_bound, y_bound):
        super().__init__()
        #Uses same size as snake segment
        self.image = pygame.Surface([20, 20])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x_bound = x_bound
        self.y_bound = y_bound
    def spawn(self):
        #Scale the bounds to segment size
        segmentx_size = segment_width + segment_margin
        segmenty_size = segment_height + segment_margin
        randx = random.randint(self.x_bound[0] // segmentx_size, self.x_bound[1] // segmentx_size - 1)
        randy = random.randint(self.y_bound[0] // segmenty_size, self.y_bound[1] // segmenty_size - 1)
        self.rect.x = (randx - 1) * segmentx_size + segment_margin + WALL_THICKNESS
        self.rect.y = (randy - 1) * segmenty_size + segment_margin + WALL_THICKNESS
        if self.rect.y >= 150 and self.rect.y <= 175 :
            self.rect.y = random.randint(175,375)
        if self.rect.y >= 400 and self.rect.y <= 425 :
            self.rect.y = random.randint(175,375)    
    def draw(self, screen):
        #print(self.rect)
        screen.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        self.wall1 = pygame.Surface([800,25])
        self.wall2= pygame.Surface([25,600])
        self.wall3= pygame.Surface([800,25])
        self.wall4= pygame.Surface([25,600])
        self.wall1.fill(MAROON)
        self.wall2.fill(MAROON)
        self.wall3.fill(MAROON)
        self.wall4.fill(MAROON)
        self.rect1=self.wall1.get_rect()
        self.rect2=self.wall2.get_rect()
        self.rect3=self.wall3.get_rect()
        self.rect4=self.wall4.get_rect()
        self.allWallslist = pygame.sprite.Group()
        
    def Wall1(self,screen):
        self.wall1 = pygame.Surface([400,25])
        self.wall2= pygame.Surface([400,25])
        self.wall1.fill(MAROON)
        self.wall2.fill(MAROON)
        self.rect1.x=200;self.rect1.y=150
        self.rect2.x=200;self.rect2.y=400
        wall = [[self.wall1,self.rect1],[self.wall2,self.rect2]]
        for i in wall:
            screen.blit(i[0],i[1])
##            self.allWallslist.add(i[0])
            
    def Wall2(self,screen) :
        self.wall1 = pygame.Surface([800,25])
        self.wall5= pygame.Surface([25,600])
        self.rect5=self.wall5.get_rect()
        self.wall1.fill(MAROON)
        self.wall5.fill(MAROON)        
        self.rect1.x=0;self.rect1.y=25
        self.rect5x=25;self.rect5.y=0
        self.rect3.x=0;self.rect3.y=575
        self.rect4.x=775;self.rect4.y=0
        wall = [[self.wall1,self.rect1],[self.wall2,self.rect2],[self.wall3,self.rect3],[self.wall4,self.rect4],[self.wall5,self.rect5]]
        for i in wall:
            screen.blit(i[0],i[1])

    def cekColl(self,x,y,level):
        wallPos = [25 , 575, 775]
        if y >= 150 and y <= 175 and level == 3 :
            if x >= 200 and x <= 600 :
                return True
        elif y >= 400 and y <= 425 and level ==3:
            if x >= 200 and x <= 600 :
                return True
        elif level<=3 and level >=2  :
            if y <= 25 or y >= 575 :
                return True
            if x <= 0 or x >= 775:
                return True
        else :
            return False
                
        
        
class APP:
    def __init__(self):
        # Call this function so the Pygame library can initialize itself
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(DEFAULT_FONT, 30)
        self.font2 = pygame.font.Font(DEFAULT_FONT, 20)
        # Create an 800x600 sized screen
        self.screen = pygame.display.set_mode([800, 600])
        # Set the title of the window
        pygame.display.set_caption('Snake')
        self.color = [WHITE,YELLOW,BLUE,PINK]
        self.DIF = [['EASY',5],['MEDIUM',10],['HARD',15]]
        self.colorIndex,self.difIndex = 0,0
        self.clock = pygame.time.Clock()
        self.done = False
        
    def game_init(self) :
        self.game_bound = {
            'min_x'  : 0,
            'max_x' : 800,
            'min_y' : 100,
            'max_y' : 600 }
        self.food = Food((self.game_bound['min_x'] + WALL_THICKNESS, self.game_bound['max_x']-WALL_THICKNESS),
                        (self.game_bound['min_y'] + WALL_THICKNESS, self.game_bound['max_y']-WALL_THICKNESS))
        self.food.spawn()
        self.score = 0
        self.level = 1
        self.wall = Wall()

    def scoreBoard(self):
        self.running = True
        BG = pygame.Surface([800,25]);BG.fill(GREY)
        BGRect=BG.get_rect()
        BGRect.x=0;BGRect.y=0
        self.screen.blit(BG,BGRect)
        self.screen.blit(self.font.render("Score : "+str(self.score), True, (255,0,0)), (50, 0))
        self.screen.blit(self.font.render("Level : "+str(self.level), True, (255,0,0)), (600, 0))
        pygame.display.update()

    def StartMenu(self):
        BG = pygame.Surface([800,400]);BG.fill(IJO)
        BGRect=BG.get_rect()
        BGRect.x=0;BGRect.y=100
        self.screen.blit(BG,BGRect)
        TittleText = self.screen.blit(self.font.render("SNAKE CLASSIC", True, (0,0,0)), (300, 130))
        ClickToStart = self.screen.blit(self.font.render("Press Y to Start Game", True, (0,0,0)), (270, 170))
        BGcolor = pygame.Surface([40,40]);BGcolor.fill(self.color[self.colorIndex])
        BGcolorRect=BG.get_rect()
        BGcolorRect.x=400;BGcolorRect.y=250
        self.screen.blit(BGcolor,BGcolorRect)
        ChangeColor = self.screen.blit(self.font.render("SNAKE Color", True, (0,0,0)), (325, 220))
        Dificult = self.screen.blit(self.font.render("Difficulty : ", True, (0,0,0)), (300,300))
        self.screen.blit(self.font.render(self.DIF[self.difIndex][0], True, (0,0,0)), (470,300))
        self.screen.blit(self.font2.render("Press KEY_LEFT and KEY_RIGHT for Change Color", True, (0,0,0)), (12, 420))
        self.screen.blit(self.font2.render("Press KEY_UP and KEY_DOWN for Change Dificult", True, (0,0,0)), (12, 450))

    def Start(self):
        start = False
        while start == False :
            #self.screen.blit(self.font.render(DIF[difIndex], True, (0,0,0)), (380,340))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_y:
                             self.Running()
                         if event.key == pygame.K_LEFT:
                             if self.colorIndex == 0 :
                                 self.colorIndex = 3
                             else:
                                 self.colorIndex -=1
                         if event.key == pygame.K_RIGHT:
                             if self.colorIndex == 3 :
                                 self.colorIndex = 0
                             else:
                                 self.colorIndex +=1
                         if event.key == pygame.K_UP:
                             if self.difIndex==2 :
                                 self.difIndex = 0
                             else:
                                 self.difIndex+=1
                         if event.key == pygame.K_DOWN:
                             if self.difIndex==0 :
                                 self.difIndex = 2
                             else:
                                 self.difIndex-=1
            self.StartMenu()
            pygame.display.flip()
            pygame.display.update()                 
            self.clock.tick(5)

    def Running(self):
         self.game_init()
         self.snake = Snake(2,self.color[self.colorIndex])
         x_change = segment_width + segment_margin
         y_change = 0
         while self.done != True :
             for event in pygame.event.get():
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_LEFT:
                         x_change = (segment_width + segment_margin) * -1
                         y_change = 0
                     if event.key == pygame.K_RIGHT:
                         x_change = (segment_width + segment_margin)
                         y_change = 0
                     if event.key == pygame.K_UP:
                         x_change = 0
                         y_change = (segment_height + segment_margin) * -1
                     if event.key == pygame.K_DOWN:
                         x_change = 0
                         y_change = (segment_height + segment_margin)
             self.snake.move(x_change, y_change)
             #Draw everything
             #Clear screen
             self.screen.fill(BLACK)
             if self.level == 2 :
                 self.wall.Wall2(self.screen)
             if self.level == 3 :
                 self.wall.Wall2(self.screen)
                 self.wall.Wall1(self.screen)
             self.scoreBoard()
             self.snake.allspriteslist.draw(self.screen)
             self.food.draw(self.screen)
             if self.score >= 2 :
                 self.level = 2
             if self.score >= 4 :
                 self.level = 3
             #Flip screen
             pygame.display.flip()
             pygame.display.update()
             #Eating food
             if self.snake.collides(self.food):
                 #self.eat_sound.play()
                 self.score += 1
                 self.snake.grow()
                 self.food.spawn()
             #Snake Hit it self
             if self.snake.collides_any(self.snake.Tail()) :
                print('lose')
                self.done = True
             xnew = self.snake.snake_segments[0].rect.x+x_change
             ynew =self.snake.snake_segments[0].rect.y+y_change 
             if self.wall.cekColl(xnew,ynew,self.level):
                print('lose')
                self.done = True
             #Pause
             self.clock.tick(self.DIF[self.difIndex][1])
         self.restart()

    def restart(self):
        BG = pygame.Surface([800,200]);BG.fill(GREY)
        BGRect=BG.get_rect()
        BGRect.x=0;BGRect.y=180
        self.screen.blit(BG,BGRect)
        ScoreText = self.screen.blit(self.font.render("Score : "+str(self.score), True, (0,0,0)), (200, 200))
        ChoiceToRestart1 = self.screen.blit(self.font.render("Want To restart? press Y", True, (0,0,0)), (200, 250))
        ChoiceToRestart1 = self.screen.blit(self.font.render("Quit? prees N : ", True, (0,0,0)), (200, 300))
        pygame.display.update()
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_y:
                             self.snake = Snake(2,self.color[self.colorIndex])
                             self.level = 1
                             self.score = 0
                             self.done = False
                             self.Running()
                         if event.key == pygame.K_n:
                             pygame.quit()
            self.clock.tick(5)
        
            
        
game = APP()
game.Start()
