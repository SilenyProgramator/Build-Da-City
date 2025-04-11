import pygame

pygame.init()

vyska_okna = 600
sirka_okna = 600

okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption("HRA")

zapadni = (0,131,109)
ruda = (190,25,24)
zelena = (100, 230, 90)
bila = (255, 255, 255)

x = (sirka_okna // 2) - 15
y = (vyska_okna // 2) - 15

rychlost_x = 10
rychlost_y = 10

class Plosina:
  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, 100, 15)
    
    
  def pohyb(self, x):
    self.rect.x += x
    
    if self.rect.left < 0:
      self.rect.left = 0
      
    if self.rect.right > sirka_okna:
      self.rect.right = sirka_okna
      
      

      
      
      
class Mic:
  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, 15, 15)
    self.rychlost_x = rychlost_x
    self.rychlost_y = rychlost_y
    
  def pohyb(self):
    self.rect.x += self.rychlost_x
    self.rect.y += self.rychlost_y
    
    if self.rect.left <= 0 or self.rect.right >= sirka_okna:
      self.rychlost_x = -self.rychlost_x
      
    if self.rect.top <= 0:
      self.rychlost_y = -self.rychlost_y
      
      
  def reset(self):
    self.rect.x = sirka_okna // 2 - 7
    self.rect.y = vyska_okna // 2 - 7
    self.rychlost_x = rychlost_x
    self.rychlost_y = rychlost_y

 



class Kostka:
  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, 60, 20)
    
    
    
  def reset(self):
    self.rect.x = sirka_okna // 2 - 7
    self.rect.y = vyska_okna // 2 - 7
    self.rychlost_x = rychlost_x
    self.rychlost_y = rychlost_y
    
  class Kostka:
    def __init__(self, x, y):
      self.rect = pygame.Rect(x, y, 60, 20)
      
      
      
      
    
def hra():
  plosina = Plosina(sirka_okna // 2 - 50, vyska_okna -40)
  pygame.draw.rect(okno, ruda, plosina.rect)
  
  mic = Mic(sirka_okna // 2 - 7, vyska_okna // 2 - 7)
  pygame.draw.circle(okno, zapadni, mic.rect.center, 10)
  
 
  kostky = []
  for i in range (8):
    for j in range(4):
      kostka = Kostka((i *74)+10, (j * 29)+10)
      kostky.append(kostka)
      

      
  hra_bezi = True
  plosina_x = 0
  
  
  while hra_bezi:
    pygame.time.delay(30)
  
  
    
    for udalost in pygame.event.get():
      if udalost.type == pygame.QUIT:
        hra_bezi = False
        
        
      
    klik = pygame.key.get_pressed()
    
    if klik[pygame.K_LEFT]:
      plosina_x = -rychlost_x
    elif klik[pygame.K_RIGHT]:
      plosina_x = rychlost_x
    else:
      plosina_x = 0
      
      
    plosina.pohyb(plosina_x)
    
    mic.pohyb()
    
    if mic.rect.colliderect(plosina.rect):
      mic.rychlost_y = -mic.rychlost_y
      
    for kostka in kostky[:]:
      if mic.rect.colliderect(kostka.rect):
        mic.rychlost_y = -mic.rychlost_y
        kostky.remove(kostka)
          
    
    if mic.rect.bottom >= vyska_okna:
      mic.reset()
      kostky = [Kostka((i *74)+10, (j * 29)+10) for i in range(1) for j in range(1)]
  
    
    
    okno.fill(bila)
    pygame.draw.rect(okno, ruda, plosina.rect)
    pygame.draw.circle(okno, zapadni, mic.rect.center, 10)
    
    for kostka in kostky:
      pygame.draw.rect(okno, zelena, kostka.rect)
        
    if not kostky:
      font = pygame.font.SysFont(None, 50)
      text = font.render("Porazil si kapitalismus!", True, ruda)
      okno.blit(text, (sirka_okna // 2 - text.get_width()//2, vyska_okna//2 - text.get_height()//2))
      pygame.display.update()
      pygame.time.wait(4000)
      hra_bezi = False
        
        
        
    pygame.display.flip()
    
  pygame.quit()
  
hra()



































