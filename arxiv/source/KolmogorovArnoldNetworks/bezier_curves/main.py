import pygame
import sys
from bezier import bezier_curve
from bspline import BSpline
from moving_object import MovingObject

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Bezier and B-Spline Curve with Control Points')

# Colors
BACKGROUND = (5, 10, 15)
LINE = (90, 250, 200)
POINT = (124, 198, 254)
KNOT = (200, 200, 0)
CONTROL_LINE = (60, 60, 60)
OBJECT_COLOR = (255, 100, 100)
BUTTON_ACTIVE = (0, 200, 0)
BUTTON_INACTIVE = (200, 0, 0)

# List to store control points and knots
control_points = []
knot_points = []
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
bspline_button_rect = pygame.Rect(450, 540, 100, 30)
toggle = False
use_bspline = False

# Start screen
start_button_bezier = pygame.Rect(250, 250, 150, 50)
start_button_bspline = pygame.Rect(450, 250, 150, 50)
start_screen = True

def draw_ui(speed):
    pygame.draw.rect(screen, (200, 200, 200), slider_rect)
    pygame.draw.rect(screen, (100, 100, 100), slider_handle_rect)
    speed_text = font.render(f'{speed:.3f}', True, (255, 255, 255))
    screen.blit(speed_text, speed_label_rect)
    
    toggle_color = BUTTON_ACTIVE if toggle else BUTTON_INACTIVE
    pygame.draw.rect(screen, toggle_color, toggle_rect)
    toggle_text = font.render('Loop' if toggle else 'Single', True, (255, 255, 255))
    screen.blit(toggle_text, (310, 545))

    bspline_color = BUTTON_ACTIVE if use_bspline else BUTTON_INACTIVE
    pygame.draw.rect(screen, bspline_color, bspline_button_rect)
    bspline_text = font.render('B-Spline', True, (255, 255, 255))
    screen.blit(bspline_text, (460, 545))

def calculate_curve():
    global curve_points
    if use_bspline:
        if len(control_points) > 1:
            bspline = BSpline(control_points)
            if len(knot_points) == len(bspline.knot_vector):
                bspline.update_knot_vector(knot_points)
            curve_points = bspline.calculate()
        else:
            curve_points = []
    else:
        if len(control_points) > 1:
            curve_points = bezier_curve(control_points, loop=toggle)
        else:
            curve_points = []
    if moving_object and len(curve_points) > 0:
        moving_object.path = curve_points

def draw_start_screen():
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, BUTTON_ACTIVE, start_button_bezier)
    bezier_text = font.render('Bezier', True, (255, 255, 255))
    screen.blit(bezier_text, (265, 260))
    
    pygame.draw.rect(screen, BUTTON_ACTIVE, start_button_bspline)
    bspline_text = font.render('B-Spline', True, (255, 255, 255))
    screen.blit(bspline_text, (465, 260))
    pygame.display.flip()

# Main loop
running = True
selected_point = None
selected_knot = None
redraw_needed = True
clock = pygame.time.Clock()

def object_movement():

    if(moving_object!=None):
        moving_object.update()
        print(moving_object.get_speed())

        screen.fill(BACKGROUND)
        if len(control_points) > 1 and len(curve_points) > 0:
            pygame.draw.lines(screen, LINE, False, curve_points, 2)
        
        for point in control_points:
            pygame.draw.circle(screen, POINT, point, 5)

        if len(control_points) > 1:
            for i in range(len(control_points) - 1):
                pygame.draw.line(screen, CONTROL_LINE, control_points[i], control_points[i + 1], 1)
        
        if len(control_points) > 1:
            for i, knot in enumerate(knot_points):
                pygame.draw.circle(screen, KNOT, (int(knot / (len(control_points) - 1) * 800), 520), 5)
        
        if moving_object:
            moving_object.draw(screen, OBJECT_COLOR)
        
        if moving_object:
            draw_ui(moving_object.speed)
        
        pygame.display.flip()

while running:
    object_movement() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if start_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_bezier.collidepoint(event.pos):
                    use_bspline = False
                    start_screen = False
                    redraw_needed = True
                elif start_button_bspline.collidepoint(event.pos):
                    use_bspline = True
                    start_screen = False
                    redraw_needed = True
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right-click to add a point
                    control_points.append(list(event.pos))
                    calculate_curve()
                    if not moving_object and len(curve_points) > 0:
                        moving_object = MovingObject(curve_points, default_speed)
                    redraw_needed = True
                elif event.button == 1:  # Left-click to select a point or knot
                    for point in control_points:
                        if pygame.Rect(point[0]-5, point[1]-5, 10, 10).collidepoint(event.pos):
                            selected_point = point
                    for i, knot in enumerate(knot_points):
                        if pygame.Rect(100 + i * 20 - 5, 520 - 5, 10, 10).collidepoint(event.pos):
                            selected_knot = i
                    if slider_handle_rect.collidepoint(event.pos):
                        slider_dragging = True
                    if toggle_rect.collidepoint(event.pos):
                        toggle = not toggle
                        calculate_curve()
                        redraw_needed = True
                    if bspline_button_rect.collidepoint(event.pos):
                        use_bspline = not use_bspline
                        calculate_curve()
                        redraw_needed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected_point = None
                    selected_knot = None
                    slider_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if selected_point:
                    selected_point[0] = event.pos[0]
                    selected_point[1] = event.pos[1]
                    calculate_curve()
                    redraw_needed = True
                if selected_knot is not None:
                    knot_points[selected_knot] = event.pos[0] / 800 * (len(control_points) - 1)
                    calculate_curve()
                    redraw_needed = True
                if slider_dragging:
                    slider_handle_rect.x = min(max(event.pos[0], slider_rect.x), slider_rect.x + slider_rect.width - slider_handle_rect.width)
                    speed = (slider_handle_rect.x - slider_rect.x) / slider_rect.width * 0.01
                    if moving_object:
                        moving_object.set_speed(speed)
                    redraw_needed = True

        if start_screen:
            draw_start_screen()
        else:
            # Update the moving object
            if moving_object:
                print(moving_object.get_speed())
                moving_object.update()

            if redraw_needed:
                # Drawing
                screen.fill(BACKGROUND)
                
                if len(control_points) > 1 and len(curve_points) > 0:
                    pygame.draw.lines(screen, LINE, False, curve_points, 2)
                
                for point in control_points:
                    pygame.draw.circle(screen, POINT, point, 5)

                if len(control_points) > 1:
                    for i in range(len(control_points) - 1):
                        pygame.draw.line(screen, CONTROL_LINE, control_points[i], control_points[i + 1], 1)
                
                if len(control_points) > 1:
                    for i, knot in enumerate(knot_points):
                        pygame.draw.circle(screen, KNOT, (int(knot / (len(control_points) - 1) * 800), 520), 5)
                
                if moving_object:
                    moving_object.draw(screen, OBJECT_COLOR)
                
                if moving_object:
                    draw_ui(moving_object.speed)
                
                pygame.display.flip()
                redraw_needed = False
       


pygame.quit()
sys.exit()
