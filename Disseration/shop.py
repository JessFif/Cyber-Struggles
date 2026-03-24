import pygame as pyg
import random as rnd

# cost = 125
# loops = 9
# overall = cost
# for i in range(loops):
#     print(i + 1, int(cost), overall)
#     cost *= 2 - (i / (loops))
#     overall += int(cost)

# print(overall)



exit_icon = pyg.image.load("images/exit icon.png")

# A function to get each text element displayed correctly ALSO USES ANCHOR!!!!!!!!!!!
def display_text(text, x, y, anchor, size, colour, screen):
    font = pyg.font.Font("freesansbold.ttf", size) # Gets the font freesansbold and sets it size
    text = font.render(text, True, colour) # Renders the font with the text and colour
    textRect = text.get_rect() # Turns the font into a rect
    if anchor == "center":
        textRect.center = (x, y) # Sets the centre of the font rect
    if anchor == "topleft":
        textRect.topleft = (x, y) # Sets the topleft of the font rect
    screen.blit(text, textRect) # Display the text

class shop_inbox:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT

        self.window_pos = [WIDTH / 4, HEIGHT / 6]
        self.exit_icon_pos = [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]] # To be used for checking if you click on the exit icon

        self.upgrade_cost_multiplier = 2 # Each upgrade increases the cost of the next upgrade by multiplying it by this number

        self.upgrades = { # [Level, max level, cost]
            "Purchase move speed": [0, 9, 100], # Max of 9 upgrades, each reduces by 1 second
            "Money per purchase": [0, 10, 50], # Max of 10 upgrades, each increases by 1
            "Special purchase multiplier": [0, 11, 25], # max of 11 upgrades, each increases multiplier by 5
            "Email multiplier": [0, 10, 75], # Max of 10 upgrades, each increases multiplier by 0.5
            "Extra Office Workers": [0, 14, 250], # Max of 14 upgrades, automatically collect a purchase every 2 seconds (reduce by 0.1)
            "Communications Manager": [0, 12, 20], # Max of 12 upgrades, reduce email spawn time by 10s
            "Leprechauns Ltd": [0, 7, 150], # Max of 7 upgrades, multiplies chance of special purchases by 1.5
            "Product Marketing Team": [0, 14, 10], # Max of 14 upgrades, reduces purchase spawn distance by 10 
            "Echo Company": [0, 10, 150], # Max of 10 upgrades, increases chance to collect two purchases at once by 5%
        }

        # self.upgrades = { # [Level, max level, cost]
        #     "Purchase move speed": [0, 9, 100], # Max of 9 upgrades, each reduces by 1 second
        #     "Money per purchase": [0, 10, 50], # Max of 10 upgrades, each increases by 1
        #     "Special purchase multiplier": [0, 11, 25], # max of 11 upgrades, each increases multiplier by 5
        #     "Email multiplier": [0, 10, 75] # Max of 10 upgrades, each increases multiplier by 0.5
        # } 

        self.all_optional_services = { # [Level, max level, cost, real/fake, description] You can unlock these as you play the game
            "Extra Office Workers": [0, 10, 250, "Real", "Automatically collects purchases"], # Automatically collects purchases
            "Communications Manager": [0, 12, 20, "Real", "Reduces email spawn time"], # Email spawn time 
            "Leprechauns Ltd": [0, 9, 125, "Real", "Increases chances of special purchases"], # Increases chance of special purchases spawning
            "Product Marketing Team": [0, 14, 10, "Real", "Reduces time between purchases"], # Reduces purchase spawn distance
            "Echo Company": [0, 10, 150, "Real", "Chance to collect multiple purchases"], # Chance to collect two purchases at once

            "Email Checker" : [0, 0, 0, "Fake", "Reduces scam emails"], # Reduces chance of emails being a scam
            "Workplace AI": [0, 0, 0, "Fake", "Automatically collect emails"], # Automatically collects emails
            "Clover Company": [0, 0, 0, "Fake", "Massively increase all luck odds"], # Massively increases all luck chances
            "Gold Earners": [0, 0, 0, "Fake", "Multiplies all money earned"], # Multiplies all money eared
            "Mirror Company": [0, 0, 0, "Fake", "Chance to collect multiple purchases"], # Chance to collect two purchases at once
        }

        self.real_optional_services = ["Extra Office Workers", "Communications Manager", "Leprechauns Ltd", "Product Marketing Team","Echo Company"]
        self.fake_optional_services = ["Email Checker", "Workplace AI", "Clover Company", "Gold Earners", "Mirror Company"]

        self.currently_available_services = []

        self.money_barrier = 10 # Amount needed to unlock next optional service

        # Purchase spawn distance, Purchase move speed, Money per purchase, Special purchase multiplier, Special purchase chance, Email spawn time, Email multiplier, Automatically collect purchases, Chance to collect multiple purchases at once
        # Option to turn off particles (if too laggy)

    def get_exit_icon_pos(self):
        return self.exit_icon_pos
    
    # ------------------------ THIRD PARTY SERVICES -----------------------

    def check_service_unlocked(self, purchase_inbox):
        if purchase_inbox.max_money_reached >= self.money_barrier and self.currently_available_services != []: # Gets a random three services for the user to choose from
            # Always gets at least one real service and one fake service (and one random)
            possible_services = []
            random_num = rnd.randint(0, len(self.real_optional_services))
            service = self.real_optional_services[random_num]
            possible_services.append([service, "Real"])
            self.real_optional_services.remove(service)

            random_num = rnd.randint(0, len(self.fake_optional_services))
            service = self.fake_optional_services[random_num]
            possible_services.append([service, "Fake"])
            self.fake_optional_services.remove(service)

            if rnd.randint(0, 1) == 0:
                random_num = rnd.randint(0, len(self.real_optional_services))
                service = self.real_optional_services[random_num]
                possible_services.append([service, "Real"])
                self.real_optional_services.remove(service)
            else:
                random_num = rnd.randint(0, len(self.fake_optional_services))
                service = self.fake_optional_services[random_num]
                possible_services.append([service, "Fake"])
                self.fake_optional_services.remove(service)

            self.currently_available_services = possible_services

            
    
    # ------------------------ UPGRADES -----------------------

    def check_upgrade_clicked(self, mouse_pos, purchase_inbox, email_inbox, money):
        mouse_rect = pyg.Rect(mouse_pos[0], mouse_pos[1], 10, 10)

        clicked_upgrade = None
        index = 0
        for upgrade in self.upgrades:
            upgrade_rect = pyg.Rect(self.window_pos[0] + 600, self.window_pos[1] + 70 + index * 75, 80, 30)
            if mouse_rect.colliderect(upgrade_rect): # What upgrade you clicked on
                if self.upgrades[upgrade][0] < self.upgrades[upgrade][1]: # Is it already at max
                    if int(self.upgrades[upgrade][2]) <= money:# Can you afford it
                        clicked_upgrade = upgrade
                        break
            index += 1
        
        if clicked_upgrade != None:
            cost = self.upgrades[clicked_upgrade][2]

            self.upgrades[clicked_upgrade][0] += 1 # Increases the level of the upgrade

            self.upgrades[clicked_upgrade][2] *= self.upgrade_cost_multiplier - (self.upgrades[clicked_upgrade][0] / self.upgrades[clicked_upgrade][1]) # Increases the cost of the next upgrade, but it increases less and less as you get closer to max level

            # Applies the upgrade
            if clicked_upgrade == "Purchase spawn distance":
                purchase_inbox.purchase_spawn_distance -= 10
            if clicked_upgrade == "Purchase move speed":
                purchase_inbox.purchase_time_to_move -= 1
                purchase_inbox.purchase_move_speed = 70 / purchase_inbox.purchase_time_to_move # Has to calculate immediately so that it moves 70
            if clicked_upgrade == "Money per purchase":
                purchase_inbox.money_per_purchase += 1
            if clicked_upgrade == "Special purchase multiplier":
                purchase_inbox.special_purchase_multiplier += 5
            if clicked_upgrade == "Special purchase chance":
                purchase_inbox.special_purchase_chance *= 1.5
            if clicked_upgrade == "Email spawn time":
                email_inbox.email_timer[1] -= 10 * 60 # Reduce 10 seconds
            if clicked_upgrade == "Email multiplier":
                email_inbox.email_multiplier += 0.5


            purchase_inbox.add_particles(upgrade_rect.left, upgrade_rect.right, upgrade_rect.y, self.upgrades[clicked_upgrade][0]) # Add some particles to make it more satisfying to buy an upgrade, increases the higher level it is
            
            return money - cost # Returns the money after buying the upgrade
        return money



    # ------------------------- DISPLAY -----------------------

    def show_shop(self, screen, money):
        # Draws the purchase inbox window then the purchases, then the outlines so they are on top
        pyg.draw.rect(screen, "light gray", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3])

        index = 0
        x_adjust = 0 # Have all the standard upgrades on the left, and the third party upgrades on the right
        for upgrade in self.upgrades:

            display_text(upgrade + ":", self.window_pos[0] + 20 + x_adjust, self.window_pos[1] + 70 + index * 75, "topleft", 20, "black", screen)

            # level_text = str(self.upgrades[upgrade][0]) + "/" + str(self.upgrades[upgrade][1])
            # display_text("Level: " + level_text, self.window_pos[0] + 350, self.window_pos[1] + 70 + index * 75, "topleft", 20, "black", screen)
            for i in range(self.upgrades[upgrade][1]):
                if i < self.upgrades[upgrade][0]:
                    pyg.draw.rect(screen, "green", [self.window_pos[0] + 20 + i * 20 + x_adjust, self.window_pos[1] + 100 + index * 75, 15, 15])
                pyg.draw.rect(screen, "black", [self.window_pos[0] + 20 + i * 20 + x_adjust, self.window_pos[1] + 100 + index * 75, 15, 15], 2)

            # Upgrade button
            if self.upgrades[upgrade][2] <= money and self.upgrades[upgrade][0] < self.upgrades[upgrade][1]:
                pyg.draw.rect(screen, "green", [self.window_pos[0] + 310 + x_adjust, self.window_pos[1] + 80 + index * 75, 60, 30])
            else:
                pyg.draw.rect(screen, "red", [self.window_pos[0] + 310 + x_adjust, self.window_pos[1] + 80 + index * 75, 60, 30])
            pyg.draw.rect(screen, "black", [self.window_pos[0] + 310 + x_adjust, self.window_pos[1] + 80 + index * 75, 60, 30], 2)

            if self.upgrades[upgrade][0] < self.upgrades[upgrade][1]:
                cost_text = "$" + str(int(self.upgrades[upgrade][2]))
            else:
                cost_text = "MAX"
            # display_text("Cost: " + cost_text, self.window_pos[0] + 310, self.window_pos[1] + 80 + index * 75, "topleft", 20, "black", screen)

            display_text(cost_text, self.window_pos[0] + 340 + x_adjust, self.window_pos[1] + 95 + index * 75, "center", 15, "white", screen)
            index += 1
            if index >= 4 and x_adjust == 0:
                x_adjust = self.width / 4 - 10
                index = 0 # Resets the y value
        
        pyg.draw.rect(screen, "black", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3], 5)
        pyg.draw.line(screen, "black", [self.window_pos[0], self.window_pos[1] + 50], [self.window_pos[0] + self.width / 2, self.window_pos[1] + 50], 2)
        screen.blit(exit_icon, [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]])

        # Draws a light blue box that reaches the bottom of the screen to hide purchases that shouldn't be on screen
        pyg.draw.rect(screen, "light blue", [self.window_pos[0], self.window_pos[1] + self.height / 4 * 3, self.width / 2, self.height - (self.window_pos[1] + self.height / 4 * 3)])
