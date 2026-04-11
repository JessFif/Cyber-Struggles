import pygame as pyg
from pygame.locals import*
from win32api import GetSystemMetrics

from purchase import purchase_inbox
from shop import shop_inbox
from emails import email_inbox
from info import info_inbox

pyg.init()


# A function to get each text element displayed correctly
def display_text(text, x, y, size, colour, screen):
    font = pyg.font.Font("freesansbold.ttf", size) # Gets the font freesansbold and sets it size
    text = font.render(text, True, colour) # Renders the font with the text and colour
    textRect = text.get_rect() # Turns the font into a rect
    textRect.center = (x, y) # Sets the centre of the font rect
    screen.blit(text, textRect) # Display the text


def display_screen(display_screen, purchase_inbox, email_inbox, money):
    display_screen.fill("light blue")
    # display_screen.blit(background, [0, 0])


    # Display icons
    # display_screen.blit(menu_icon, [0, 0])
    display_screen.blit(exit_icon, [WIDTH - 50, 0])

    if state == "background": # Shows the app icons
        display_screen.blit(purchases_icon, [WIDTH / 3, HEIGHT / 5])
        display_screen.blit(email_icon, [WIDTH / 3, HEIGHT / 5 * 2])
        display_screen.blit(info_icon, [WIDTH / 3, HEIGHT / 5 * 3])
        display_screen.blit(shop_icon, [WIDTH / 3, HEIGHT / 5 * 4])

    # Display money and multiplier
    display_text("Money: $" + str(round(money, 2)), int(WIDTH / 2), 40, 25, "black", display_screen)
    if purchase_inbox.overall_money_multiplier < 10:
        display_text("Multiplier: " + str(round(purchase_inbox.overall_money_multiplier, 2)) + "x", int(WIDTH / 2), 70 + 2.5 * purchase_inbox.overall_money_multiplier, int(15 + 5 * purchase_inbox.overall_money_multiplier), "black", display_screen)
    else:
        display_text("Multiplier: " + str(round(purchase_inbox.overall_money_multiplier, 2)) + "x", int(WIDTH / 2), 70 + 2.5 * 10, int(15 + 5 * 10), "black", display_screen)
    if purchase_inbox.overall_money_multiplier_timers != []:
        lowest_timer = purchase_inbox.overall_money_multiplier_timers[0] # It was already sorted!
        pyg.draw.line(screen, "black", [int(WIDTH / 5 * 2) - 5, 55], [int(WIDTH / 5 * 3) + 5, 55], 10)
        pyg.draw.line(screen, "red", [int(WIDTH / 5 * 2), 55], [int(WIDTH / 5 * 3), 55], 5)
        pyg.draw.line(screen, "green", [int(WIDTH / 5 * 2), 55], [int(WIDTH / 5 * 2) + int(WIDTH / 5) * (lowest_timer[1] / lowest_timer[2]), 55], 5)
        
    
    if state == "purchases":
        purchase_inbox.show_purchases(display_screen)
    
    if state == "email":
        email_inbox.show_emails(display_screen)
    
    if state == "shop":
        inbox_shop.show_shop(display_screen, money, purchase_inbox)

    if state == "info":
        inbox_info.display_info(display_screen)

    # The particles are always shown
    purchase_inbox.show_particles(display_screen)


WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)


# Overarching icons
exit_icon = pyg.image.load("images/exit icon.png")
menu_icon = pyg.image.load("images/menu icon.png")

# App icons
purchases_icon = pyg.image.load("images/verify icon.png")
purchases_icon = pyg.transform.scale(purchases_icon, (100, 100))
email_icon = pyg.image.load("images/email icon.png")
email_icon = pyg.transform.scale(email_icon, (100, 100))
info_icon = pyg.image.load("images/info icon.png")
info_icon = pyg.transform.scale(info_icon, (100, 100))
shop_icon = pyg.image.load("images/shop icon.png")
shop_icon = pyg.transform.scale(shop_icon, (100, 100))

background = pyg.image.load("images/jhamel-namibia.jpg")
background = pyg.transform.scale(background, (WIDTH, HEIGHT))

inbox_purchases = purchase_inbox(WIDTH, HEIGHT)
inbox_email = email_inbox(WIDTH, HEIGHT)
inbox_shop = shop_inbox(WIDTH, HEIGHT)
inbox_info = info_inbox(WIDTH, HEIGHT)

money = 0

state = "background"

screen = pyg.display.set_mode((WIDTH, HEIGHT))

clock = pyg.time.Clock()

running = True
while running:
    
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
        if event.type == pyg.MOUSEBUTTONDOWN:
            mouse_pos = pyg.mouse.get_pos()
            
            if state == "purchases": # If you are currently in the "purchases" app, check if you clicked on one of them
                money += inbox_purchases.check_purchase_clicked(mouse_pos)
                if money > inbox_purchases.max_money_reached:
                    inbox_purchases.max_money_reached = money

                # Check if you clicked on the exit icons
                exit_icon_pos = inbox_purchases.get_exit_icon_pos()
                if mouse_pos[0] >= exit_icon_pos[0] and mouse_pos[0] <= exit_icon_pos[0] + 50:
                    if mouse_pos[1] >= exit_icon_pos[1] and mouse_pos[1] <= exit_icon_pos[1] + 50:
                        state = "background"
            
            if state == "email": # If you are currently in the "email" app, check if you clicked on one of them
                scam_clicked = inbox_email.check_email_click(mouse_pos, inbox_purchases, inbox_info)
                if scam_clicked == True:
                    state = "info"

                # Check if you clicked on the exit icons
                exit_icon_pos = inbox_email.get_exit_icon_pos()
                if mouse_pos[0] >= exit_icon_pos[0] and mouse_pos[0] <= exit_icon_pos[0] + 50:
                    if mouse_pos[1] >= exit_icon_pos[1] and mouse_pos[1] <= exit_icon_pos[1] + 50:
                        state = "background"
            
            if state == "shop": # If you are currently in the "shop" app, check if you clicked on one of the upgrades/services
                money = inbox_shop.check_upgrade_clicked(mouse_pos, inbox_purchases, inbox_email, money)

                inbox_shop.check_service_clicked(mouse_pos, inbox_purchases)
                
                # Check if you clicked on the exit icons
                exit_icon_pos = inbox_shop.get_exit_icon_pos()
                if mouse_pos[0] >= exit_icon_pos[0] and mouse_pos[0] <= exit_icon_pos[0] + 50:
                    if mouse_pos[1] >= exit_icon_pos[1] and mouse_pos[1] <= exit_icon_pos[1] + 50:
                        state = "background"
            
            if state == "info": # If you are currently in the "info" app, check if you clicked on one of them
                inbox_info.check_clicked_page(mouse_pos)

                # Check if you clicked on the exit icons
                exit_icon_pos = inbox_info.get_exit_icon_pos()
                if mouse_pos[0] >= exit_icon_pos[0] and mouse_pos[0] <= exit_icon_pos[0] + 50:
                    if mouse_pos[1] >= exit_icon_pos[1] and mouse_pos[1] <= exit_icon_pos[1] + 50:
                        state = "background"

            if state == "background": # If you are on the background screen, check if you clicked on an app icon
                if mouse_pos[0] >= WIDTH / 3 and mouse_pos[0] <= WIDTH / 3 + 100:
                    if mouse_pos[1] >= HEIGHT / 5 and mouse_pos[1] <= HEIGHT / 5 + 100:
                        state = "purchases"
                    elif mouse_pos[1] >= HEIGHT / 5 * 2 and mouse_pos[1] <= HEIGHT / 5 * 2 + 100:
                        state = "email"
                    elif mouse_pos[1] >= HEIGHT / 5 * 3 and mouse_pos[1] <= HEIGHT / 5 * 3 + 100:
                        state = "info"
                    elif mouse_pos[1] >= HEIGHT / 5 * 4 and mouse_pos[1] <= HEIGHT / 5 * 4 + 100:
                        state = "shop"

            if mouse_pos[0] >= WIDTH - 50 and mouse_pos[1] <= 50:
                running = False

    # Makes sure that inbox fills up whislt you're not looking at it
    inbox_purchases.move_particles()
    inbox_purchases.move_purchases()
    inbox_purchases.update_multipliers()
    inbox_purchases.check_auto_collect_purchases(money)
    inbox_purchases.update_combos()

    inbox_email.increment_timer()

    inbox_shop.check_service_unlocked(inbox_purchases)


    display_screen(screen, inbox_purchases, inbox_email, money)
    pyg.display.flip()

    clock.tick(60)

pyg.quit()