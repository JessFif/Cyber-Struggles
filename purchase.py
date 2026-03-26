import pygame as pyg
import random as rnd

particle_img = pyg.image.load("images/Particle.png")

exit_icon = pyg.image.load("images/exit icon.png")

# A function to get each text element displayed correctly
def display_text(text, x, y, size, colour, screen):
    font = pyg.font.Font("freesansbold.ttf", size) # Gets the font freesansbold and sets it size
    text = font.render(text, True, colour) # Renders the font with the text and colour
    textRect = text.get_rect() # Turns the font into a rect
    textRect.center = (x, y) # Sets the centre of the font rect
    screen.blit(text, textRect) # Display the text

class purchase_inbox:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.purchases = [] # [index, purchase_type, purchase_move_timers, purchase_rect]
        self.max_purchases = 0 # To be discovered in fill_purchases

        self.window_pos = [WIDTH / 4, HEIGHT / 6]
        self.exit_icon_pos = [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]] # To be used for checking if you click on the exit icon

        self.money_per_purchase = 1
        self.special_purchase_multiplier = 10
        self.special_purchase_chance = 0.02

        self.max_money_reached = 0 # To keep track of the most money user has had at any time, used to unlock third party services in the shop

        self.overall_money_multiplier = 1
        self.overall_money_multiplier_timers = [] # [multiplier, time until multiplier runs out (-1 is infinite)] Adds multipliers if you report emails correctly/incorrectly as scams

        self.purchase_spawn_distance = 140 # Starts out that purchases spawn extra far apart, so the user can upgrade it
        self.purchase_time_to_move = 14 # Starts out that purchases move for a long time, so the user can upgrade it. This combined with move speed needs to multiply to 70!
        self.purchase_move_speed = 70 / self.purchase_time_to_move # Needs to move 70 pixels total
        
        self.particles = [] # [Rect, velocity]
        self.combos = [] # [x, y, int, timer]

        self.extra_workers = None # These are how you automate collecting purchases. When you unlock it, it becomes [0, 5.5 * 60] for [ticks, ticks until auto collect]

        self.echo_chance = 0 # Chance to collect purchases multiple times in one click

        self.fill_purchases()

    # ------------------------ RETEURNS -----------------------

    def get_exit_icon_pos(self):
        return self.exit_icon_pos

    # ------------------------- MULTIPLIERS -----------------------

    def update_multipliers(self):
        to_be_removed = []
        self.overall_money_multiplier = 1
        for multiplier in self.overall_money_multiplier_timers:
            multiplier[1] -= 1
            self.overall_money_multiplier *= multiplier[0]
            if multiplier[1] <= 0:
                to_be_removed.append(multiplier)
        for multiplier in to_be_removed:
            self.overall_money_multiplier_timers.remove(multiplier)
        

    # ------------------------ PARTICLES -----------------------
    
    def move_particles(self):
        particles_to_remove = []
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[1][1] += 1.25
            particle[2] += 5
            if particle[0][1] > self.height:
                particles_to_remove.append(particle)
        for particle in particles_to_remove:
            self.particles.remove(particle)
        return 
    
    def add_particles(self, left_x, right_x, y, loops):
        
        # For each loop, randomly add a new particle with a random velocity on the either side of the purchase
        for i in range(loops):
            x_velo = 10 - rnd.random() * 7
            y_velo = -25 + rnd.random() * 10
            self.particles.append([[left_x, y], [-x_velo, y_velo], 0])
            self.particles.append([[right_x, y], [x_velo, y_velo], 0])

    def update_combos(self):
        finished_timers = []
        for combo in self.combos:
            combo[3] -= 1
            if combo[3] <= 0:
                finished_timers.append(combo)

        for combo in finished_timers:
            self.combos.remove(combo)
    #------------------------ PURCHASES -----------------------

    def fill_purchases(self):
        y_value =  self.window_pos[1] + 75
        index = 1
        while y_value < self.height - self.window_pos[1] - 10:
            new_purchase = pyg.Rect(self.window_pos[0] + 25, y_value, self.width / 2 - 50, 60)
            purchase_type = "normal"
            purchase_move_timers = 0
            self.purchases.append([index, purchase_type, purchase_move_timers, new_purchase])

            y_value += 70 # An extra 10 to leave some space between each purchase, since each purchase is 60 pixels high
            index += 1
        self.max_purchases = index - 1
    
    def move_purchases(self):
        for purchase in self.purchases:
            timer = purchase[2] # For every move timer on an purchase, move it up by 2 px and decrement that timer
            if timer >= 1:
                purchase[3].y -= self.purchase_move_speed
                if purchase[3].y < self.window_pos[1] + 75 + (purchase[0] - 1) * 70: # If the purchase has moved too far
                    purchase[3].y = self.window_pos[1] + 75 + (purchase[0] - 1) * 70
                purchase[2] -= 1  
            elif timer > 0:
                purchase[3].y -= timer * self.purchase_move_speed
                # purchase[3].y = self.window_pos[1] + 75 + (purchase[0] - 1) * 70 # Force sets the purchase to the right place
                purchase[2] -= timer 
            elif timer == 0: # If the purchase is in the wrong place
                purchase[2] = (purchase[3].y - (self.window_pos[1] + 75 + (purchase[0] - 1) * 70)) / self.purchase_move_speed # Makes sure that the purchase moves to the right position

    def check_purchase_clicked(self, mouse_pos):
        mouse_rect = pyg.Rect(mouse_pos[0], mouse_pos[1], 10, 10)
        clicked_purchase = None
        for purchase in self.purchases:
            if mouse_rect.colliderect(purchase[3]) == True:
                clicked_purchase = purchase
                break 
        
        if clicked_purchase == None or mouse_pos[1] > self.window_pos[1] + self.height / 4 * 3: # If you didn't click on a purchase or clicked below the window
            return 0

        left = clicked_purchase[3].left
        right = clicked_purchase[3].right
        y = clicked_purchase[3].y

        combo = 1
        while True:
            if rnd.randint(1, 100) <= self.echo_chance / combo:
                combo += 1
            else:
                break
        
        if combo > 1:
            self.combos.append([right - 50, clicked_purchase[3].top, combo, combo * 30]) # The timer goes on for (combo) seconds / 2

        if clicked_purchase[1] == "normal":
            income = self.money_per_purchase
            loops = self.money_per_purchase * 2
        if clicked_purchase[1] == "special":
            loops = self.special_purchase_multiplier * 2
            income = self.money_per_purchase * self.special_purchase_multiplier
        
        loops = int(loops * self.overall_money_multiplier) * combo
        income = income * self.overall_money_multiplier * combo

        if loops > 20: # Reduces lag hopefully
            loops = 20

        self.add_particles(left, right, y, loops)

        self.add_purchase(self.purchases[-1]) # Adds a new purchase below the very lowest purchase

        index = clicked_purchase[0]
        self.purchases.remove(clicked_purchase)
        # For every purchase below the one you just bought, decrement their index to account for the missing purchase, and add move timers
        for i in range(index -1, len(self.purchases)):
            self.purchases[i][0] -= 1 # Decrement all subsequent index by 1
            self.purchases[i][2] += self.purchase_time_to_move # Makes each needed purchase move up by 5px each tick for 14 ticks (70 total) to get back to correct position
        
        return income

    def add_purchase(self, lowest_purchase):
        latest_purchase = self.purchases[-1]

        y_value = lowest_purchase[3].y + 70 + self.purchase_spawn_distance # New purchases need to at least 70 pixels apart

        purchase_type = "normal"
        if rnd.randint(1,100) <= self.special_purchase_chance * 100:
            purchase_type = "special"

        new_purchase = pyg.Rect(self.window_pos[0] + 25, y_value, self.width / 2 - 50, 60)

        purchase_move_timer = lowest_purchase[2] + self.purchase_spawn_distance / self.purchase_move_speed # Makes sure the new purchase moves to the right position

        index = latest_purchase[0] + 1
        self.purchases.append([index, purchase_type, purchase_move_timer, new_purchase])

    def check_auto_collect_purchases(self, money):
        if self.extra_workers != None:
            self.extra_workers[0] += 1
            if self.extra_workers[0] >= self.extra_workers[1]: # If it is time to auto collect a purchase
                # Collect the top purchase always ([3] is its rect)
                if self.purchases[0][3].top <= self.window_pos[1] + self.height / 4 * 3: # If there is a purchase on screen
                    pos_x = self.purchases[0][3].x
                    pos_y = self.purchases[0][3].y
                    money = self.check_purchase_clicked((pos_x, pos_y))
                    self.extra_workers[0] = 0
        return money


    #------------------------ DISPLAY -----------------------
    
    def show_particles(self, screen):
        for particle in self.particles:
            new_particle = particle_img
            new_particle = pyg.transform.rotate(new_particle, particle[2])
            screen.blit(new_particle, particle[0])
        
        for combo in self.combos:
            display_text("Combo x" + str(combo[2]), combo[0], combo[1], int(5 + (combo[3] / 5)), "black", screen)

    def show_purchases(self, screen):
        # Draws the purchase inbox window then the purchases, then the outlines so they are on top
        pyg.draw.rect(screen, "light gray", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3])

        for purchase in self.purchases:
            if purchase[1] == "normal":
                colour = "green"
            if purchase[1] == "special":
                colour = "gold"
        
            pyg.draw.rect(screen, colour, purchase[3])
            pyg.draw.rect(screen, "black", purchase[3], 5)

        
        pyg.draw.rect(screen, "black", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3], 5)
        pyg.draw.line(screen, "black", [self.window_pos[0], self.window_pos[1] + 50], [self.window_pos[0] + self.width / 2, self.window_pos[1] + 50], 2)
        screen.blit(exit_icon, [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]])

        # Draws a light blue box that reaches the bottom of the screen to hide purchases that shouldn't be on screen
        pyg.draw.rect(screen, "light blue", [self.window_pos[0], self.window_pos[1] + self.height / 4 * 3, self.width / 2, self.height - (self.window_pos[1] + self.height / 4 * 3)])
