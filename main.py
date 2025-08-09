import pygame
import math

# Initialize
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Force Components on Incline with Gravity and Friction")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)     # Applied force
GREEN = (50, 200, 50)   # Parallel component
BLUE = (50, 50, 220)    # Normal component
GREY = (200, 200, 200)
YELLOW = (230, 200, 50) # Gravity

# Physics
incline_angle = 30  # degrees
object_shape = "rectangle"  # or "circle"
object_size = (80, 50)  # width, height if rectangle; radius if circle
gravity = 200  # pixels/s²
friction_coeff = 0.2
object_dist_from_left = 200
velocity = 0.0  # along incline

# State variables
dragging = False
end_pos = None
applied_force = 0.0  # along incline

font = pygame.font.SysFont(None, 22)

def draw_incline(angle):
    rad = math.radians(angle)
    slope_length = WIDTH
    x1 = 100
    y1 = HEIGHT - 100
    x2 = x1 + slope_length
    y2 = y1 - math.tan(rad) * slope_length
    pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 4)
    return (x1, y1, x2, y2)

def get_base_point_on_incline(x1, y1, angle, dist_from_left):
    rad = math.radians(angle)
    bx = x1 + dist_from_left * math.cos(rad)
    by = y1 - dist_from_left * math.sin(rad)
    return (bx, by)

def draw_object_on_slope(base_point, angle, shape):
    theta = math.radians(angle)
    if shape == "rectangle":
        normal_offset = object_size[1] / 2
        center_x = base_point[0] - normal_offset * math.sin(theta)
        center_y = base_point[1] - normal_offset * math.cos(theta)
        rect_surface = pygame.Surface(object_size, pygame.SRCALPHA)
        rect_surface.fill(GREY)
        rotated_surface = pygame.transform.rotate(rect_surface, angle)
        rect_rect = rotated_surface.get_rect(center=(center_x, center_y))
        screen.blit(rotated_surface, rect_rect)
        return (center_x, center_y)
    elif shape == "circle":
        radius = object_size[0]
        center_x = base_point[0] - radius * math.sin(theta)
        center_y = base_point[1] - radius * math.cos(theta)
        pygame.draw.circle(screen, GREY, (int(center_x), int(center_y)), radius)
        return (center_x, center_y)

def draw_force_components(center, vector, angle, color_main, label):
    end = (center[0] + vector[0], center[1] + vector[1])
    pygame.draw.line(screen, color_main, center, end, 3)
    pygame.draw.circle(screen, color_main, (int(end[0]), int(end[1])), 4)

    dx, dy = vector
    theta = math.radians(angle)
    incline_dir = (math.cos(theta), -math.sin(theta))
    normal_dir = (math.sin(theta), math.cos(theta))

    f_parallel_mag = dx * incline_dir[0] + dy * incline_dir[1]
    f_normal_mag = dx * normal_dir[0] + dy * normal_dir[1]

    parallel_end = (center[0] + f_parallel_mag * incline_dir[0],
                    center[1] + f_parallel_mag * incline_dir[1])
    normal_end = (center[0] + f_normal_mag * normal_dir[0],
                  center[1] + f_normal_mag * normal_dir[1])

    pygame.draw.line(screen, GREEN, center, parallel_end, 2)
    pygame.draw.line(screen, BLUE, center, normal_end, 2)

    screen.blit(font.render(f"{label}", True, color_main), ((center[0]+end[0])//2, (center[1]+end[1])//2))
    screen.blit(font.render("Parallel", True, GREEN), ((center[0]+parallel_end[0])//2, (center[1]+parallel_end[1])//2))
    screen.blit(font.render("Normal", True, BLUE), ((center[0]+normal_end[0])//2, (center[1]+normal_end[1])//2))

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0
    screen.fill(WHITE)

    # Draw incline
    incline_line = draw_incline(incline_angle)

    # Stopper line at bottom
    stopper_length = 50
    stopper_angle_rad = math.radians(90 - incline_angle)
    stopper_x = incline_line[0] - stopper_length * math.cos(stopper_angle_rad)
    stopper_y = incline_line[1] - stopper_length * math.sin(stopper_angle_rad)
    pygame.draw.line(screen, BLACK, (incline_line[0], incline_line[1]), (stopper_x, stopper_y), 4)

    # Base point of object
    base_point = get_base_point_on_incline(incline_line[0], incline_line[1], incline_angle, object_dist_from_left)
    object_center = draw_object_on_slope(base_point, incline_angle, object_shape)

    # Gravity vector
    gravity_vec = (0, gravity/2)  # scaled for display
    draw_force_components(object_center, gravity_vec, incline_angle, YELLOW, "Gravity")

    # Physics: acceleration along incline
    g_parallel = -gravity * math.sin(math.radians(incline_angle))
    friction_force = friction_coeff * gravity * math.cos(math.radians(incline_angle))
    net_force = g_parallel + applied_force

    if abs(net_force) > friction_force:
        net_force -= math.copysign(friction_force, net_force)
    else:
        net_force = 0

    acc = net_force
    velocity += acc * dt
    object_dist_from_left += velocity * dt

    # Collision with stopper
    if object_dist_from_left < 50:
        object_dist_from_left = 50
        velocity = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            end_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            end_pos = None
            applied_force = 0
        elif event.type == pygame.MOUSEMOTION and dragging:
            end_pos = event.pos
            dx = end_pos[0] - object_center[0]
            dy = end_pos[1] - object_center[1]
            theta = math.radians(incline_angle)
            incline_dir = (math.cos(theta), -math.sin(theta))
            applied_force = (dx * incline_dir[0] + dy * incline_dir[1]) * 5  # scaling
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                incline_angle = min(incline_angle + 5, 85)
            elif event.key == pygame.K_DOWN:
                incline_angle = max(incline_angle - 5, 0)
            elif event.key == pygame.K_s:
                object_shape = "circle" if object_shape == "rectangle" else "rectangle"
            elif event.key == pygame.K_LEFT:
                object_dist_from_left = max(50, object_dist_from_left - 10)
            elif event.key == pygame.K_RIGHT:
                object_dist_from_left = min(WIDTH - 100, object_dist_from_left + 10)
            elif event.key == pygame.K_f:
                friction_coeff = max(0, min(1, friction_coeff + 0.05))
            elif event.key == pygame.K_d:
                friction_coeff = max(0, min(1, friction_coeff - 0.05))

    # Draw applied force if dragging
    if dragging and end_pos:
        draw_force_components(object_center, (end_pos[0] - object_center[0], end_pos[1] - object_center[1]),
                              incline_angle, RED, "Applied Force")

    # Show friction
    screen.blit(font.render(f"Friction Coefficient: {friction_coeff:.2f}", True, BLACK), (20, 20))

    pygame.display.flip()

pygame.quit()
