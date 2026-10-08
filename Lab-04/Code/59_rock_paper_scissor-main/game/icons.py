import pygame
import math


def draw_rock(surface, cx, cy, size):
    """Draw a rock icon – rounded stone shape with highlight."""
    body = (150, 142, 130)
    shadow = (110, 104, 94)
    highlight = (185, 178, 168)

    # Main stone body (slightly squashed ellipse)
    body_rect = pygame.Rect(cx - size, cy - int(size * 0.78), size * 2, int(size * 1.56))
    pygame.draw.ellipse(surface, body, body_rect)

    # Upper-left highlight
    hl_rect = pygame.Rect(cx - int(size * 0.55), cy - int(size * 0.55),
                          int(size * 0.9), int(size * 0.6))
    pygame.draw.ellipse(surface, highlight, hl_rect)

    # Outline
    pygame.draw.ellipse(surface, shadow, body_rect, 2)


def draw_paper(surface, cx, cy, size):
    """Draw a paper icon – sheet with corner fold and text lines."""
    w = int(size * 1.5)
    h = int(size * 1.8)
    left = cx - w // 2
    top = cy - h // 2

    # Sheet
    sheet = pygame.Rect(left, top, w, h)
    pygame.draw.rect(surface, (240, 240, 245), sheet, border_radius=3)
    pygame.draw.rect(surface, (170, 175, 190), sheet, width=2, border_radius=3)

    # Corner fold (top-right triangle)
    fold = int(size * 0.35)
    pygame.draw.polygon(surface, (210, 215, 225),
                        [(left + w - fold, top), (left + w, top), (left + w, top + fold)])
    pygame.draw.line(surface, (170, 175, 190),
                     (left + w - fold, top), (left + w, top + fold), 2)

    # Horizontal text lines
    mx = int(size * 0.3)
    ly = top + int(size * 0.55)
    gap = int(size * 0.35)
    for i in range(3):
        lw = w - 2 * mx - (fold if i == 0 else 0)
        pygame.draw.line(surface, (195, 200, 215),
                         (left + mx, ly + i * gap),
                         (left + mx + lw, ly + i * gap), 2)


def draw_scissors(surface, cx, cy, size):
    """Draw scissors icon – two crossing blades with ring handles."""
    blade = (190, 195, 210)
    handle = (200, 70, 70)
    pivot = (160, 165, 175)

    bl = int(size * 0.9)      # blade length from pivot
    spread = int(size * 0.45)  # vertical spread
    hr = int(size * 0.26)      # handle ring radius

    # Upper blade + ring handle
    tip_x = cx - bl
    pygame.draw.line(surface, blade, (tip_x, cy - spread), (cx, cy), 3)
    pygame.draw.circle(surface, handle,
                       (cx + int(bl * 0.28), cy - spread + int(size * 0.12)), hr, 3)

    # Lower blade + ring handle
    pygame.draw.line(surface, blade, (tip_x, cy + spread), (cx, cy), 3)
    pygame.draw.circle(surface, handle,
                       (cx + int(bl * 0.28), cy + spread - int(size * 0.12)), hr, 3)

    # Pivot dot
    pygame.draw.circle(surface, pivot, (cx, cy), 3)


def draw_question(surface, cx, cy, size):
    """Question-mark placeholder for unrevealed choices."""
    font = pygame.font.SysFont(None, int(size * 2))
    q = font.render("?", True, (90, 95, 110))
    surface.blit(q, (cx - q.get_width() // 2, cy - q.get_height() // 2))


def draw_fist(surface, cx, cy, size, shake_offset=0):
    """Shaking fist used during the countdown animation."""
    y = cy + shake_offset
    # Main fist circle
    pygame.draw.circle(surface, (130, 128, 135), (cx, y), size)
    # Knuckle highlight
    pygame.draw.arc(surface, (165, 162, 170),
                    pygame.Rect(cx - int(size * 0.6), y - int(size * 0.7),
                                int(size * 1.2), int(size * 0.9)),
                    0.3, 2.8, 2)
    # Outline
    pygame.draw.circle(surface, (95, 92, 100), (cx, y), size, 2)


def draw_icon(surface, choice, cx, cy, size):
    """Dispatch to the correct icon-drawing function."""
    _drawers = {
        "ROCK": draw_rock,
        "PAPER": draw_paper,
        "SCISSORS": draw_scissors,
    }
    drawer = _drawers.get(choice)
    if drawer:
        drawer(surface, cx, cy, size)
    else:
        draw_question(surface, cx, cy, size)
