import pygame, random, sys
from pygame.locals import *

windowWidth = 700
windowHeight = 650
textColor = (0, 255, 26)
backgroundColor = (0, 0, 0)
fps = 30
enemiesMinSize = 10
enemiesMaxSize = 40
enemiesMinSpeed = 1
enemiesMaxSpeed = 8
newEnemyRate = 6
p1Movement = 5

def terminate():
  pygame.quit()
  sys.exit()

def waitForPlayerKeyDown():
  while True:
    for event in pygame.event.get():
       if event.type == QUIT:
          terminate()
       if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            terminate()
          return

def PlayerCollision(playerRect, enemies):
  for e in enemies:
    if playerRect.colliderect(e['rect']):
      return True
  return False

def drawText(text, font, surface, x, y):
  textObj = font.render(text, 1, textColor)
  textRect = textObj.get_rect()
  textRect.topleft = (x,y)
  surface.blit(textObj, textRect)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font = pygame.font.Font('Dodger/slkscr.ttf', 40)

gameOverSound = pygame.mixer.Sound('Dodger/bala.wav')
pygame.mixer.music.load('Dodger/megalovania.mid')

playerImage = pygame.image.load('Dodger/player.png')
playerRect = playerImage.get_rect()
enemyImage = pygame.image.load('Dodger/com.png')

drawText('Dodger', font, windowSurface, (windowWidth / 3) + 20, (windowHeight / 3))
drawText('Press a key to start', font, windowSurface, (windowWidth / 3) - 150, (windowHeight / 3) + 50)
pygame.display.update()
waitForPlayerKeyDown()

topScore = 0
while True:
  enemies = []
  score = 0
  playerRect.topleft = (windowWidth / 2, windowHeight - 50)
  moveLeft = moveRight = moveUp = moveDown = False
  reverseCheat = slowCheat = False
  enemyAddCounter = 0
  pygame.mixer.music.play(-1, 0.0)

  while True:
    score += 1

    for event in pygame.event.get():
      if event.type == QUIT:
        terminate()

      if event.type == KEYDOWN:
        if event.key == ord('z'):
          reverseCheat = True
        if event.key == ord('x'):
          slowCheat = True
        if event.key == K_LEFT or event.key == ord('a'):
          moveRight = False
          moveLeft = True
        if event.key == K_RIGHT or event.key == ord('d'):
          moveLeft = False
          moveRight = True
        if event.key == K_UP or event.key == ord('w'):
          moveDown = False
          moveUp = True
        if event.key == K_DOWN or event.key == ord('s'):
          moveUp = False
          moveDown = True

      if event.type == KEYUP:
        if event.key == ord('z'):
          reverseCheat = False
          score = 0
        if event.key == ord('x'):
          slowCheat = False
          score = 0
        if event.key == K_ESCAPE:
          terminate()

        if event.key == K_LEFT or event.key == ord('a'):
          moveLeft = False
        if event.key == K_RIGHT or event.key == ord('d'):
          moveRight = False
        if event.key == K_UP or event.key == ord('w'):
          moveUp = False
        if event.key == K_DOWN or event.key == ord('s'):
          moveDown = False

      if event.type == MOUSEMOTION:
        playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

    if not reverseCheat and not slowCheat:
      enemyAddCounter += 1 
    if enemyAddCounter == newEnemyRate:
      enemyAddCounter = 0
      enemySize = random.randint(enemiesMinSize, enemiesMaxSize)
      newEnemy = {'rect':pygame.Rect(random.randint(0, windowWidth-enemySize), 0 - enemySize, enemySize, enemySize ),
          'speed': random.randint(enemiesMinSpeed, enemiesMaxSize),
          'surface': pygame.transform.scale(enemyImage, (enemySize, enemySize)),
          }
        
      enemies.append(newEnemy)

    if moveLeft and playerRect.left > 0:
      playerRect.move_ip(-1 * p1Movement, 0)
    if moveRight and playerRect.right < windowWidth:
      playerRect.move_ip(p1Movement, 0)
    if moveUp and playerRect.top > 0:
      playerRect.move_ip(0, -1 * p1Movement)
    if moveDown and playerRect.bottom < windowHeight:
      playerRect.move_ip(0, p1Movement)
    
    pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

    for e in enemies:
      if not reverseCheat and not slowCheat:
        e['rect'].move_ip(0, e['speed'])
      elif reverseCheat:
        e['rect'].move_ip(0, -5)
      elif slowCheat:
        e['rect'].move_ip(0, 1)

    for e in enemies[:]:
      if e['rect'].top > windowHeight:
        enemies.remove(e)

    windowSurface.fill(backgroundColor)

    drawText('Score: %s'%(score),font, windowSurface, 10, 0)
    drawText('Top Score: %s'%(topScore),font, windowSurface, 10, 40)

    windowSurface.blit(playerImage, playerRect)

    for e in enemies:
      windowSurface.blit(e['surface'], e['rect'])

    pygame.display.update()

    if PlayerCollision(playerRect, enemies):
      if score > topScore:
        topScore = score
      break
            
    mainClock.tick(fps)

  pygame.mixer.music.stop()
  gameOverSound.play()

  drawText('GAME OVER', font, windowSurface, (windowWidth / 3) - 20, (windowHeight / 3))
  drawText('Press a key to play again',font, windowSurface, (windowWidth / 3) - 210 , (windowHeight / 3 ) + 50)
  pygame.display.update()
  waitForPlayerKeyDown()

  gameOverSound.stop()
    