import pygame,sys,random,time
import tkinter as tk
from tkinter import messagebox
pygame.init()
width = 600
row = 30
cellw = width//row
display = pygame.display.set_mode((width,width))
pygame.display.set_caption('Snake')
crash = pygame.mixer.Sound('data/crash.wav')
pygame.mixer.music.load('data/Game_Plan.mp3')

eat1 = pygame.mixer.Sound('data/food1.wav')
eat2 = pygame.mixer.Sound('data/food2.wav')
def eat(i):
	if i==0:
		return eat1
	else:
		return eat2


white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)


class snake(object):
	body = []
	turns ={}
	def __init__(self,color,pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirx = 0
		self.diry = 1
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					self.dirx=-1
					self.diry=0
					self.turns[self.head.pos[:]]= [self.dirx,self.diry]
				elif event.key==pygame.K_RIGHT:
					self.dirx=1
					self.diry=0
					self.turns[self.head.pos[:]]= [self.dirx,self.diry]
				elif event.key==pygame.K_UP:
					self.dirx=0
					self.diry=-1
					self.turns[self.head.pos[:]]= [self.dirx,self.diry]
				elif event.key==pygame.K_DOWN:
					self.dirx=0
					self.diry=1
					self.turns[self.head.pos[:]]= [self.dirx,self.diry]
			elif event.type == pygame.KEYUP:
				pass
		for i,c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn =self.turns[p]
				c.move(turn[0],turn[1])
				if i==len(self.body)-1:
					self.turns.pop(p)
			else:
				if c.dirx==-1 and c.pos[0]<=0: c.pos=(c.rows-1,c.pos[1])
				elif c.dirx==1 and c.pos[0]>=c.rows-1: c.pos=(0,c.pos[1])
				elif c.diry==-1 and c.pos[1]<=0: c.pos=(c.pos[0],c.rows-1)
				elif c.diry==1 and c.pos[1]>=c.rows-1: c.pos=(c.pos[0],0)
				else: c.move(c.dirx,c.diry)
	def draw(self):
		for i,c in enumerate(self.body):
			if i==0:
				c.draw(1)
			else:
				c.draw(0)
	def addCube(self):
		tail = self.body[-1]
		dx,dy = tail.dirx, tail.diry
		if dx==1 and dy==0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx==-1 and dy==0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx==0 and dy==1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx==0 and dy==-1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
		self.body[-1].dirx=dx
		self.body[-1].diry=dy
	def reset(self,pos):
		self.head = cube(pos)
		self.body=[]
		self.body.append(self.head)
		self.turns={}
		self.dirx=0
		self.diry=1
		pygame.mixer.music.unpause()


class cube(object):
	rows=row
	def __init__(self,start,dirx=1,diry=0,color = green):
		self.pos =start
		self.dirx=1
		self.diry=0
		self.color=color
	def move(self,dirx,diry):
		self.dirx=dirx
		self.diry=diry
		self.pos = (self.pos[0]+self.dirx,self.pos[1]+self.diry)
	def draw(self,eyes):
		i = self.pos[0]
		j = self.pos[1]


		pygame.draw.rect(display,self.color,(i*cellw+1,j*cellw+1,cellw-1 ,cellw-1))
		if eyes==1:
			centre = cellw//2
			radius = 3
			mid1 = (i*cellw +centre - radius,j*cellw+8)
			mid2 = (i*cellw +centre + radius,j*cellw+8)
			pygame.draw.circle(display,black,mid1,3)
			pygame.draw.circle(display,black,mid2,3 )

def food(item):
	positions = item.body

	while True:
		x = random.randrange(row)
		y = random.randrange(row)
		if len(list(filter(lambda z :z.pos ==(x,y),positions)))>0:
			continue
		else:
			break

	return(x,y)


def drawGrid():
	x=0
	y=0
	for j in range(row+1):

		pygame.draw.line(display,white,(x,0),(x,width))
		pygame.draw.line(display,white,(0,y),(width,y))
		y+= cellw
		x+= cellw


def message_box(subject,content):
	root=tk.Tk()
	root.attributes("-topmost",True)
	root.withdraw()
	messagebox.showinfo(subject,content)
	try:
		root.destroy()
	except :
		pass

			

def redraw_window():
	global s,snack
	global score
	display.fill((0,0,0))
	
	drawGrid()
	s.draw()
	snack.draw(0)
	pygame.display.flip()

def main():
	global s,snack,score
	pygame.mixer.music.play(-1)

	s = snake(green,(10,10))

	flag =True
	clock = pygame.time.Clock()
	snack = cube(food(s),color = red)

	while flag:
		clock.tick(10)
		
		s.move()
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(food(s),color = red)

			pygame.mixer.Sound.play(eat(len(s.body)%2))
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z: z.pos,s.body[x+1:])):
				score = len(s.body)
				pygame.mixer.Sound.play(crash)
				time.sleep(1)
				pygame.mixer.music.pause()

				message_box('You lost',"Play again \n Score: {}".format(score))
				s.reset((10,10))
				break


		redraw_window()



main()