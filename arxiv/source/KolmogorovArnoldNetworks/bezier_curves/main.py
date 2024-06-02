import pygame
import sys
from bezier import bezier_curve
from moving_object import MovingObject

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Bezier Curve with Control Points')

# Colors
BACKGROUND = (5, 10, 15)
LINE = (90, 250, 200)
POINT = (124, 198, 254)
OBJECT_COLOR = (255, 100, 100)

# List to store control points
control_points = []
curve_points = []

# Initialize moving object with a default speed
default_speed = 0.001
moving_object = None

# UI Elements
font = pygame.font.Font(None, 36)
slider_rect = pygame.Rect(50, 550, 200, 10)
slider_handle_rect = pygame.Rect(50, 540, 10, 30)
slider_dragging = False
speed_label_rect = pygame.Rect(10, 540, 40, 30)

# Initialize slider handle position based on default speed
slider_handle_rect.x = int(slider_rect.x + (default_speed / 0.01) * slider_rect.width)

# Toggle for continuous shapes
toggle_rect = pygame.Rect(300, 540, 100, 30)
toggle = False

def draw_ui(speed):
    pygame.draw.rect(screen, (200, 200, 200), slider_rect)
    pygame.draw.rect(screen, (100, 100, 100), slider_handle_rect)
    #speed_text = font.render(f'{speed:.3f}', True, (255, 255, 255))
    #screen.blit(speed_text, speed_label_rect)
    
    toggle_color = (0, 200, 0) if toggle else (200, 0, 0)
    pygame.draw.rect(screen, toggle_color, toggle_rect)
    toggle_text = font.render('Loop' if toggle else 'Single', True, (255, 255, 255))
    screen.blit(toggle_text, (310, 545))

# Main loop
running = True
selected_point = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right-click to add a point
                control_points.append(list(event.pos))
                if len(control_points) > 1:
                    curve_points = bezier_curve(control_points, loop=toggle)
                    if not moving_object:
                        moving_object = MovingObject(curve_points, default_speed)
                    else:
                        moving_object.path = curve_points
            elif event.button == 1:  # Left-click to select a point
                for point in control_points:
                    if pygame.Rect(point[0]-5, point[1]-5, 10, 10).collidepoint(event.pos):
                        selected_point = point
                if slider_handle_rect.collidepoint(event.pos):
                    slider_dragging = True
                if toggle_rect.collidepoint(event.pos):
                    toggle = not toggle
                    if len(control_points) > 1:
                        curve_points = bezier_curve(control_points, loop=toggle)
                        moving_object.path = curve_points
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected_point = None
                slider_dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if selected_point:
                selected_point[0] = event.pos[0]
                selected_point[1] = event.pos[1]
                if len(control_points) > 1:
                    curve_points = bezier_curve(control_points, loop=toggle)
                    moving_object.path = curve_points
            if slider_dragging:
                slider_handle_rect.x = min(max(event.pos[0], slider_rect.x), slider_rect.x + slider_rect.width - slider_handle_rect.width)
                speed = (slider_handle_rect.x - slider_rect.x) / slider_rect.width * 0.01
                if moving_object:
                    moving_object.set_speed(speed)

    # Update the moving object
    if moving_object:
        moving_object.update()

    # Drawing
    screen.fill(BACKGROUND)
    
    if len(control_points) > 1:
        pygame.draw.lines(screen, LINE, False, curve_points, 2)
    
    for point in control_points:
        pygame.draw.circle(screen, POINT, point, 5)
    
    if moving_object:
        moving_object.draw(screen, OBJECT_COLOR)
    
    if moving_object:
        draw_ui(moving_object.speed)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
