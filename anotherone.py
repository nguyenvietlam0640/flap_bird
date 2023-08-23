# basic physics in a pygame game!!
from random import randint
from pygame.locals import *
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode((0,0),pygame.RESIZABLE | pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
taking_shot = False
game_running =True
force = 0
max_force = 10000
force_direction = 1
powering_up = False

TUBE_WIDTH = 50
TUBE_VELOCITY = 5
TUBE_GAP = 150

tube1_x = 1500
tube2_x = 2500
tube3_x = 3500

tube1_height = randint(100,600)
tube2_height = randint(100,600)
tube3_height = randint(100,600)

fps = 60
timer = pygame.time.Clock()

# game variables
slides = 1
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3
# track positions of mouse to get movement vector
mouse_trajectory = []
score = 0
font = pygame.font.SysFont('sans', 20)
pausing = False
tube1_pass = False
tube2_pass = False
tube3_pass = False
bird_image = pygame.image.load("flap/bird.png").convert_alpha()
bg = pygame.image.load("flap/background.png").convert_alpha()
bgscale = pygame.transform.scale(bg,(WIDTH,HEIGHT))
# bird_image = pygame.transform.scale(bird_image, (, BIRD_HEIGHT))
tube_list =[]

class Ball:
	def __init__(self,image, x_pos, y_pos, width, height, color, mass, retention, y_speed, x_speed, id, friction, pausing):
		self.image = bird_image
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.width = width
		self.height = height
		self.color = color
		self.mass = mass
		self.retention = retention
		self.y_speed = y_speed
		self.x_speed = x_speed
		self.id = id
		self.rect = ''
		self.selected = False
		self.pausing = pausing
		self.friction = friction

	def draw(self,surface):
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.rect = surface.blit(self.image,(self.x_pos,self.y_pos))

	def draw_pic(self, surface):
		surface.blit(self.image,(self.x_pos,self.y_pos))
		
	def check_gravity(self):
		if not self.selected:
			if self.y_speed > 0:
				self.y_speed -=  self.friction
			elif self.y_speed < 0:
				self.y_speed += self.friction
		else:
			self.x_speed = x_push
			self.y_speed = y_push
		return self.y_speed

	def update_pos(self, mouse):
		if not self.selected:
			self.y_pos += self.y_speed
			self.x_pos += self.x_speed
		else:
			self.x_pos = mouse[0]
			self.y_pos = mouse[1]

	def check_select(self, pos):
		self.selected = False
		if self.rect.collidepoint(pos):
			self.selected = True
		if slides == 0:
			self.selected = False
		return self.selected	

	def check_col(self,danger):
		if self.rect.colliderect(danger):
			self.pausing = True
		else:
			self.pausing = False
		return self.pausing
			

def draw_walls():
	left = pygame.draw.line(screen, 'white', (0, 0), (0, HEIGHT), wall_thickness)
	right = pygame.draw.line(screen, 'white', (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
	top = pygame.draw.line(screen, 'white', (0, 0), (WIDTH, 0), wall_thickness)
	bottom = pygame.draw.line(screen, 'white', (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness)
	wall_list = [left, right, top, bottom]
	return wall_list


def calc_motion_vector():
	x_speed = 0
	y_speed = 0
	if len(mouse_trajectory) > 10:
		# x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
		y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
	return x_speed, y_speed


# ball1 = Ball(50, 50, 30, 'blue', 100, .75, 0, 0, 1, 0.3)
# ball2 = Ball(500, 50, 50, 'green', 300, .9, 0, 0, 2, 0.3)
ball3 = Ball(bird_image,50, 400, 50,50, 'purple', 200, .8, 0, 0, 3, .3, False)
# ball4 = Ball(700, 50, 60, 'red', 500, .7, 0, 0, 4, .3)
# balls = [ball1, ball2, ball3, ball4]
print(mouse_trajectory)
# main game loop
run = True
bird_image1 = pygame.transform.scale(ball3.image, (ball3.width, ball3.height))


while run:
	timer.tick(fps)
	screen.fill('green')
	# screen.blit(bgscale,(0,0))
	mouse_coords = pygame.mouse.get_pos()
	mouse_trajectory.append(mouse_coords)
	if len(mouse_trajectory) > 20:
		mouse_trajectory.pop(0)
	x_push, y_push = calc_motion_vector()

	#draw tube
	tube1_rect = pygame.draw.rect(screen,'blue', (tube1_x, 0, TUBE_WIDTH, tube1_height))
	tube2_rect = pygame.draw.rect(screen,'blue', (tube2_x, 0, TUBE_WIDTH, tube2_height))	
	tube3_rect = pygame.draw.rect(screen,'blue', (tube3_x, 0, TUBE_WIDTH, tube3_height))
	tube_list.append(tube1_rect)
	tube_list.append(tube2_rect)
	tube_list.append(tube3_rect)

	# Draw tube inverse
	tube1_rect_inv = pygame.draw.rect(screen, 'blue', (tube1_x, tube1_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube1_height - TUBE_GAP))
	tube2_rect_inv = pygame.draw.rect(screen, 'blue', (tube2_x, tube2_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube2_height - TUBE_GAP))
	tube3_rect_inv = pygame.draw.rect(screen, 'blue', (tube3_x, tube3_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube3_height - TUBE_GAP))
	tube_list.append(tube1_rect_inv)
	tube_list.append(tube2_rect_inv)
	tube_list.append(tube3_rect_inv)

	# Draw cond
	# tube1_cond = pygame.draw.rect(screen, 'red',(tube1_x,tube1_height,50,150))
	# tube2_cond = pygame.draw.rect(screen, 'red',(tube2_x,tube2_height,50,150))
	# tube3_cond = pygame.draw.rect(screen, 'red',(tube3_x,tube3_height,50,150))
	# cond_list = [tube1_cond,tube2_cond,tube3_cond]


	# move tube to the left
	tube1_x = tube1_x - TUBE_VELOCITY
	tube2_x = tube2_x - TUBE_VELOCITY
	tube3_x = tube3_x - TUBE_VELOCITY

	# generate new tubes
	if tube1_x < -TUBE_WIDTH:
		tube1_x = 3000
		tube1_height = randint(100,600)
		tube1_pass = False	
	if tube2_x < -TUBE_WIDTH:
		tube2_x = 3000	
		tube2_height = randint(100,600)	
		tube2_pass = False	
	if tube3_x < -TUBE_WIDTH:
		tube3_x = 3000
		tube3_height = randint(100,600)	
		tube3_pass = False	

	sand_rect = pygame.draw.rect(screen, 'YELLOW', (0,799,1001,1))
	sand_rect1 =pygame.draw.rect(screen,'yellow', (0,1,1001,1))



	# for i in cond_list:
	# 	if bird_rect.colliderect(sand_rect):
	# 		tube1_cond = pygame.draw.rect(screen,'blue',(0,0,0,0))


	# walls = draw_walls()
	# ball1.draw()
	# ball2.draw()
	ball3.draw(screen)
	# ball4.draw()
	# ball1.update_pos(mouse_coords)
	# ball2.update_pos(mouse_coords)
	ball3.update_pos(mouse_coords)
	# ball4.update_pos(mouse_coords)
	# ball1.y_speed = ball1.check_gravity()
	# ball2.y_speed = ball2.check_gravity()
	ball3.y_speed = ball3.check_gravity()
	# ball4.y_speed = ball4.check_gravity()
	# ball3.check_col()


	# if ball1.y_pos > 805:
		# ball1.y_pos = -10
	# if ball1.y_pos < -5:
		# ball1.y_pos = 810
	# if ball2.y_pos > 805:
		# ball2.y_pos = -10
	# if ball2.y_pos < -10:
		# ball2.y_pos = 810
	if ball3.y_pos > 801:
		ball3.y_pos = 0
	if ball3.y_pos < -1:
		ball3.y_pos = 800
	# if ball4.y_pos > 805:
	# 	ball4.y_pos = -10
	# if ball4.y_pos < -5:
	# 	ball4.y_pos = 810

	score_txt = font.render("Score: " + str(score), True, 'white')
	screen.blit(score_txt,(5,5))

	
	# delete = pygame.sprite.spritecollide(bird_rect, cond_list,True)	


	if tube1_x + TUBE_WIDTH <= ball3.x_pos and tube1_pass == False:
		score += 1
		slides +=1		 
		tube1_pass = True
	if tube2_x + TUBE_WIDTH <= ball3.x_pos and tube2_pass == False:
		score += 1 
		slides +=1		 
		tube2_pass = True
	if tube3_x + TUBE_WIDTH <= ball3.x_pos and tube3_pass == False:
		score += 1 
		slides +=1		 
		tube3_pass = True
	
	for tube in [tube1_rect, tube2_rect, tube3_rect, tube1_rect_inv, tube2_rect_inv, tube3_rect_inv]:
		if ball3.check_col(tube) or ball3.x_pos < -1 or ball3.x_pos > 1001:
			pausing = True
			ball3.y_speed = 0
			ball3.x_speed = 0
			TUBE_VELOCITY = 0
			game_over_txt = font.render("Game over, score: " + str(score), True, 'white')
			screen.blit(game_over_txt, (200,300))
			press_space_txt = font.render("Press Space to Continue", True, 'white')
			screen.blit(press_space_txt, (200,400))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if ball3.check_select(event.pos): 
					active_select = True
					slides -= 1 
					
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				active_select = False
				ball3.check_select((-300, -300))
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.type == pygame.MOUSEBUTTONDOWN:		
				if pausing == True:
					ball3.y_pos = 400
					ball3.x_pos = 50
					TUBE_VELOCITY = 5
					tube1_x = 1500
					tube2_x = 2500
					tube3_x = 3500
					score = 0
					slides = 1
					pausing = False
	pygame.display.flip()
pygame.quit()

# ball1.check_select(event.pos) or ball2.check_select(event.pos) \
# or ball4.check_select(event.pos):

