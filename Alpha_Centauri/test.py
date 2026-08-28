import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Choose an Option")
font = pygame.font.Font(None, 36)

# Define 3 option rectangles
rects = [
    pygame.Rect(220, 120, 200, 50),  # Option 1
    pygame.Rect(220, 200, 200, 50),  # Option 2
    pygame.Rect(220, 280, 200, 50)   # Option 3
]

options = ["Option A", "Option B", "Option C"]
selected_option = None

# Main game loop
running = True
while running:
    screen.fill((30, 30, 30))  # Dark background
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check which rectangle was clicked
            for i, rect in enumerate(rects):
                if rect.collidepoint(event.pos):
                    selected_option = options[i]
                    print(f"You chose: {selected_option}")

    # Draw the 3 buttons
    for i, rect in enumerate(rects):
        # Change color if mouse hovers over button
        color = (100, 200, 100) if rect.collidepoint(pygame.mouse.get_pos()) else (70, 70, 70)
        
        pygame.draw.rect(screen, color, rect, border_radius=8)
        
        # Render text inside button
        txt_surface = font.render(options[i], True, (255, 255, 255))
        txt_rect = txt_surface.get_rect(center=rect.center)
        screen.blit(txt_surface, txt_rect)

    pygame.display.flip()

pygame.quit()
