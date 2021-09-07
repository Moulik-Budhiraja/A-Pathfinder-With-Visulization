import pygame
import os
pygame.init()


def fill(surface, color):  # Change colors of image
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


def take_input():
    # Basic window information
    WIDTH, HEIGHT = 300, 150
    INPUT = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Plot points")
    clock = pygame.time.Clock()  # basicly fps
    base_font = pygame.font.Font(None, 25)

    # color info
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')

    # custom pygame events
    INVALID_INPUT = pygame.USEREVENT + 1

    # define information and objects for the start_position input field
    origin_rect = pygame.Rect(25, 40, 100, 25)
    origin_color = color_passive
    origin_active = False
    origin_point = ''

    # define information and objects for the end_position input field
    end_rect = pygame.Rect(25, 100, 100, 25)
    end_color = color_passive
    end_active = False
    end_point = ''

    # ^ this was a bad name but to lazy to change it

    # submit button information
    submit = pygame.Rect(WIDTH - 85, HEIGHT - 40, 75, 30)
    submit_text = "Submit"

    # checkbox information
    checkbox_text = base_font.render("Visualize", True, (255, 255, 255))
    checkbox = pygame.Rect(WIDTH - 35, 15, 26, 26)
    checkmark = pygame.Rect(checkbox.x + (checkbox.width // 2 - 9),
                            checkbox.y + (checkbox.height // 2 - 9), 18, 18)
    checked = False

    # place holder information (when there is no text in an input field)
    place_holder = 'ex. 2, 8'
    place_holder_surface = base_font.render(
        place_holder, True, (128, 128, 128))

    # used when an invalid input is detected
    invalid_text = ""

    # this is information used to make sure backspacing is smooth
    tick = 0
    backspace_tick = -1
    backspace_tick_mod = -1

    run = True
    while run:
        INPUT.fill((0, 0, 0))

        for event in pygame.event.get():  # if the "x" is clicked close window
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # start input field clicked
                if origin_rect.collidepoint(event.pos):
                    origin_active = True
                else:
                    origin_active = False

                if end_rect.collidepoint(event.pos):  # end input field clicked
                    end_active = True
                else:
                    end_active = False

                if submit.collidepoint(event.pos):  # submit button clicked

                    # confirm start and end points are not the same
                    origin_tuple = validate(origin_point)
                    end_tuple = validate(end_point)

                    if not origin_tuple:
                        origin_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    if not end_tuple:
                        end_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    if origin_tuple == end_tuple:
                        end_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    elif origin_tuple and end_tuple:
                        return (origin_tuple, end_tuple, checked)

                # toggle checked state when clicked
                if checkbox.collidepoint(event.pos):
                    if checked == False:
                        checked = True
                    else:
                        checked = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:  # enter key pressed
                    # does the same as submit button
                    origin_tuple = validate(origin_point)
                    end_tuple = validate(end_point)

                    if not origin_tuple:
                        origin_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    if not end_tuple:
                        end_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    if origin_tuple == end_tuple:
                        end_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    elif origin_tuple and end_tuple:
                        return (origin_tuple, end_tuple, checked)

                if event.key == pygame.K_TAB:  # tab pressed
                    # tab between input fields
                    if origin_active == True:
                        origin_active = False
                        end_active = True
                    elif end_active == True:
                        origin_active = True
                        end_active = False

                if origin_active == True:
                    # if the key pressed isn't a predefined key, add it to the input field
                    if event.key not in {pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_RETURN}:
                        origin_point += event.unicode

                elif end_active == True:
                    if not event.key in {pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_RETURN}:
                        end_point += event.unicode

            if event.type == INVALID_INPUT:
                invalid_text = "Invalid Input"

        if origin_active == True:
            # gets every key that is being pressed right now
            keys_pressed = pygame.key.get_pressed()
            # Backspace logic:
            # So the way this works is pretty straight forward
            # if the backspace key is pressed -> remove a character and record the tick it was pressed on
            # if the backspace key has been held down for at least 15 ticks,
            # remove 1 character every 2 ticks
            # if the backspace key has been released reset and wait for another press to repeat the process

            if keys_pressed[pygame.K_BACKSPACE]:
                if backspace_tick == -1:  # -1 = hasn't been pushed. pos int = first push
                    origin_point = origin_point[:-1]  # remove last character
                    backspace_tick = tick
                elif tick - backspace_tick > 15:
                    backspace_tick_mod = backspace_tick % 2
                    if tick % 2 == backspace_tick_mod:
                        origin_point = origin_point[:-1]
            else:
                backspace_tick = -1

        elif end_active == True:
            keys_pressed = pygame.key.get_pressed()
            # Backspace logic for second text box
            if keys_pressed[pygame.K_BACKSPACE]:
                if backspace_tick == -1:  # -1 = hasn't been pushed. pos int = first push
                    end_point = end_point[:-1]  # remove last character
                    backspace_tick = tick
                elif tick - backspace_tick > 15:
                    backspace_tick_mod = backspace_tick % 2
                    if tick % 2 == backspace_tick_mod:
                        end_point = end_point[:-1]
            else:
                backspace_tick = -1

        # set the colors of the input field borders based on whats in mouse focus
        if origin_active:
            origin_color = color_active
        else:
            origin_color = color_passive

        if end_active:
            end_color = color_active
        else:
            end_color = color_passive

        # draw text input fields with borders of 2 px
        pygame.draw.rect(INPUT, origin_color, origin_rect, 2)
        pygame.draw.rect(INPUT, end_color, end_rect, 2)

        pygame.draw.rect(INPUT, (184, 65, 44), submit)  # submit button

        pygame.draw.rect(INPUT, color_passive, checkbox)
        if checked:
            pygame.draw.rect(INPUT, color_active, checkmark)

        # Render text
        origin_surface = base_font.render(origin_point, True, (255, 255, 255))
        start_surface = base_font.render("Start point", True, (255, 255, 255))

        end_surface = base_font.render(end_point, True, (255, 255, 255))
        finish_surface = base_font.render("End point", True, (255, 255, 255))

        submit_surface = base_font.render(submit_text, True, (255, 255, 255))

        invalid_text_display = base_font.render(
            invalid_text, True, (255, 0, 0))

        # draw all text on the screen
        INPUT.blit(invalid_text_display, (submit.x + submit.width -
                   invalid_text_display.get_width(), submit.y - invalid_text_display.get_height() - 4))

        INPUT.blit(start_surface, (origin_rect.x,
                   origin_rect.y - origin_rect.height + 4))

        INPUT.blit(finish_surface, (end_rect.x,
                   end_rect.y - end_rect.height + 4))

        INPUT.blit(origin_surface, (origin_rect.x + 4, origin_rect.y + 4))
        INPUT.blit(end_surface, (end_rect.x + 4, end_rect.y + 4))

        INPUT.blit(submit_surface, (submit.x + (submit.width // 2) - submit_surface.get_width() //
                   2, submit.y + (submit.height // 2) - submit_surface.get_height() // 2))

        INPUT.blit(checkbox_text, (checkbox.x - checkbox_text.get_width() -
                   10, checkbox.y + (checkbox.height // 2 - checkbox_text.get_height() // 2)))

        if origin_point == '' and origin_active == False:
            INPUT.blit(place_holder_surface,
                       (origin_rect.x + 4, origin_rect.y + 4))

        if end_point == '' and end_active == False:
            INPUT.blit(place_holder_surface,
                       (end_rect.x + 4, end_rect.y + 4))

        # resize text boxes if text is too long

        origin_rect.w = max(100, origin_surface.get_width() + 8)
        end_rect.w = max(100, end_surface.get_width() + 8)

        pygame.display.update()

        # set fps and tick the clock
        clock.tick(60)
        tick += 1


def validate(coords: str):
    if ',' in coords:
        try:
            coords = coords.split(',')
            coords = [i.strip() for i in coords]
            coords = [int(i) for i in coords]
            coords = tuple(coords)
            return coords
        except Exception:
            return False
    else:
        return False


if __name__ == '__main__':
    take_input()
