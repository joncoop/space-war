def draw_text(surface, text, font, color, loc, anchor='topleft'):
    text = str(text)
    text = font.render(text, True, color)
    rect = text.get_rect()

    if anchor == 'topleft':
        rect.topleft = loc
    elif anchor == 'bottomleft':
        rect.bottomleft = loc
    elif anchor == 'topright':
        rect.topright = loc
    elif anchor == 'bottomright':
        rect.bottomright = loc
    elif anchor == 'midtop':
        rect.midtop = loc
    elif anchor == 'midleft':
        rect.midleft = loc
    elif anchor == 'midbottom':
        rect.midbottom = loc
    elif anchor == 'midright':
        rect.midleft = loc
    elif anchor == 'center':
        rect.center = loc

    surface.blit(text, rect)
