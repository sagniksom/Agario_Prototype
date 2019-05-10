import pygame
pygame.font.init()
myfont = pygame.font.SysFont("monospace",15)

def render_score_label(screen_width,screen_height,score,surface):
    """(int),(int),(int),(object) ---> (none)
    Renders your personal score(mass) in the top left corner of your screen.
    """
    x = screen_width / 40
    y = screen_height / 40
    score_label = myfont.render("Score: " + (str(int(score))),1,(0,0,0))
    surface.blit(score_label, (x,y))
