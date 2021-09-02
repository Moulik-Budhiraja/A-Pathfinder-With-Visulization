import pygame
pygame.init()


def take_input():
    WIDTH, HEIGHT = 300, 150

    INPUT = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Plot points")
    clock = pygame.time.Clock()
    base_font = pygame.font.Font(None, 25)

    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')

    INVALID_INPUT = pygame.USEREVENT + 1

    origin_rect = pygame.Rect(25, 40, 100, 25)
    origin_color = color_passive
    origin_active = False
    origin_point = ''

    end_rect = pygame.Rect(25, 100, 100, 25)
    end_color = color_passive
    end_active = False
    end_point = ''

    submit = pygame.Rect(WIDTH - 85, HEIGHT - 40, 75, 30)
    submit_text = "Submit"

    place_holder = 'ex. 2, 8'

    invalid_text = ""

    run = True
    tick = 0
    backspace_tick = -1
    backspace_tick_mod = -1
    while run:
        INPUT.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if origin_rect.collidepoint(event.pos):
                    origin_active = True
                else:
                    origin_active = False

                if end_rect.collidepoint(event.pos):
                    end_active = True
                else:
                    end_active = False

                if submit.collidepoint(event.pos):
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
                        return (origin_tuple, end_tuple)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    origin_tuple = validate(origin_point)
                    end_tuple = validate(end_point)

                    if not origin_tuple:
                        origin_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    if not end_tuple:
                        end_point = ''
                        pygame.event.post(pygame.event.Event(INVALID_INPUT))

                    if origin_tuple and end_tuple:
                        return (origin_tuple, end_tuple)

                if event.key == pygame.K_TAB:
                    if origin_active == True:
                        origin_active = False
                        end_active = True
                    elif end_active == True:
                        origin_active = True
                        end_active = False

                if origin_active == True:
                    if event.key in {pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_RETURN}:
                        pass
                    else:
                        origin_point += event.unicode

                elif end_active == True:
                    if event.key in {pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_RETURN}:
                        pass
                    else:
                        end_point += event.unicode

            if event.type == INVALID_INPUT:
                invalid_text = "Invalid Input"

        if origin_active == True:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_BACKSPACE]:
                if backspace_tick == -1:  # -1 = hasn't been pushed. pos int = first push
                    origin_point = origin_point[:-1]
                    backspace_tick = tick
                elif tick - backspace_tick > 15:
                    backspace_tick_mod = backspace_tick % 2
                    if tick % 2 == backspace_tick_mod:
                        origin_point = origin_point[:-1]
            else:
                backspace_tick = -1

        elif end_active == True:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_BACKSPACE]:
                if backspace_tick == -1:  # -1 = hasn't been pushed. pos int = first push
                    end_point = end_point[:-1]
                    backspace_tick = tick
                elif tick - backspace_tick > 15:
                    backspace_tick_mod = backspace_tick % 2
                    if tick % 2 == backspace_tick_mod:
                        end_point = end_point[:-1]
            else:
                backspace_tick = -1

        if origin_active:
            origin_color = color_active
        else:
            origin_color = color_passive

        if end_active:
            end_color = color_active
        else:
            end_color = color_passive

        pygame.draw.rect(INPUT, origin_color, origin_rect, 2)
        pygame.draw.rect(INPUT, end_color, end_rect, 2)

        pygame.draw.rect(INPUT, (184, 65, 44), submit)

        origin_surface = base_font.render(origin_point, True, (255, 255, 255))
        end_surface = base_font.render(end_point, True, (255, 255, 255))

        place_holder_surface = base_font.render(
            place_holder, True, (128, 128, 128))

        start_surface = base_font.render("Start point", True, (255, 255, 255))
        finish_surface = base_font.render("End point", True, (255, 255, 255))

        submit_surface = base_font.render(submit_text, True, (255, 255, 255))

        invalid_text_display = base_font.render(
            invalid_text, True, (255, 0, 0))

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

        if origin_point == '' and origin_active == False:
            INPUT.blit(place_holder_surface,
                       (origin_rect.x + 4, origin_rect.y + 4))

        if end_point == '' and end_active == False:
            INPUT.blit(place_holder_surface,
                       (end_rect.x + 4, end_rect.y + 4))

        origin_rect.w = max(100, origin_surface.get_width() + 8)
        end_rect.w = max(100, end_surface.get_width() + 8)

        pygame.display.update()
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
