import pygame as pyg
import random as rnd


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


class info_inbox:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT

        self.window_pos = [WIDTH / 4, HEIGHT / 6]
        self.exit_icon_pos = [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]] # To be used for checking if you click on the exit icon

        self.current_page = "Home" # Starts on home, can navigate to Phishing Styles or Third Party Services info

        self.navigation = {
            "Home": ["Phishing styles", "Third Party Services"],
            "Phishing styles": ["Impersonation", "Urgency", "Too Good", "Typos"],
            "Third Party Services": ['Extra Office Workers', 'Product Marketing Team', 'Workplace AI', 'Email Checker', 'Leprechauns Ltd', 'Clover Company', 'Echo Company', 'Communications Manager', 'Gold Earners', 'Mirror Company']
        }
        # The contents of each info page will be stored in a text file in a folder called "info", this is just for navigation

    def get_exit_icon_pos(self):
        return self.exit_icon_pos
    
    # ------------------------- NAVIGATION -----------------------

    def check_clicked_page(self, mouse_pos):
        mouse_rect = pyg.Rect(mouse_pos[0], mouse_pos[1], 10, 10) # A rect of the mouse position to check if it collides with the page option rects

        # Checks if you click on any of the options in the current page, if so changes the current page to that option
        if self.current_page in self.navigation.keys(): # If the current page is not one that contains info (so is one of home, phishing styles or third party services)
            index = 0
            shift_right = 0
            for page in self.navigation[self.current_page]:
                page_rect = pyg.Rect(self.window_pos[0] + 25 + shift_right, self.window_pos[1] + 125 + index * 75, self.width / 4 - 50, 50) # The rect of the page option

                if mouse_rect.colliderect(page_rect):
                    self.current_page = page
                    return
                index += 1
                if index >= 8 and shift_right == 0: # If there are more than 8 options, start a new column
                    shift_right = self.width / 4
                    index = 0
                    
        home_rect = pyg.Rect(self.window_pos[0] + 15, self.window_pos[1] + 65, 75, 30)
        if mouse_rect.colliderect(home_rect): # If you click on the home button, go back to the home page
            self.current_page = "Home"
        

    # ------------------------- DISPLAY -----------------------


    def display_info(self, screen):
        # Draws the purchase inbox window then the purchases, then the outlines so they are on top
        pyg.draw.rect(screen, "light gray", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3])

        shift_right = 0
        if self.current_page in self.navigation.keys(): # If the current page is not one that contains info (so is one of home, phishing styles or third party services)
            index = 0
            for page in self.navigation[self.current_page]:
                page_rect = pyg.Rect(self.window_pos[0] + 25 + shift_right, self.window_pos[1] + 125 + index * 75, self.width / 4 - 50, 50) # The rect of the page option

                mouse_pos = pyg.mouse.get_pos() # Gonna check if the user is hovering over a page option
                mouse_rect = pyg.Rect(mouse_pos[0], mouse_pos[1], 10, 10)
                if mouse_rect.colliderect(page_rect):
                    pyg.draw.rect(screen, "light blue", page_rect) # Makes the option visible
                    pyg.draw.rect(screen, "black", page_rect, 2) # Outline
                else:
                    pyg.draw.rect(screen, "white", page_rect) # Makes the option visible
                    pyg.draw.rect(screen, "black", page_rect, 2) # Outline
                display_text(page, self.window_pos[0] + 30 + shift_right, self.window_pos[1] + 145 + index * 75, "topleft", 20, "black", screen)
                index += 1
                if index >= 5 and shift_right == 0: # If there are more than 8 options, start a new column
                    shift_right = self.width / 4
                    index = 0

        if self.current_page != "Home": # Add a home button in top left corner
            home_rect = pyg.Rect(self.window_pos[0] + 15, self.window_pos[1] + 65, 75, 30)

            mouse_pos = pyg.mouse.get_pos() # Gonna check if the user is hovering over the home button
            mouse_rect = pyg.Rect(mouse_pos[0], mouse_pos[1], 10, 10)
            if mouse_rect.colliderect(home_rect):
                pyg.draw.rect(screen, "light blue", home_rect) # Makes the button blue if hovering
                pyg.draw.rect(screen, "black", home_rect, 2) # Outline
            else:
                pyg.draw.rect(screen, "white", home_rect)
                pyg.draw.rect(screen, "black", home_rect, 2) # Outline
            display_text("Home", self.window_pos[0] + 20, self.window_pos[1] + 72, "topleft", 16, "black", screen)


        # Draws the outside of the window
        pyg.draw.rect(screen, "black", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3], 5)
        pyg.draw.line(screen, "black", [self.window_pos[0], self.window_pos[1] + 50], [self.window_pos[0] + self.width / 2, self.window_pos[1] + 50], 2)
        screen.blit(exit_icon, [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]])

        # Draws a light blue box that reaches the bottom of the screen to hide stuff that shouldn't be on screen
        pyg.draw.rect(screen, "light blue", [self.window_pos[0], self.window_pos[1] + self.height / 4 * 3, self.width / 2, self.height - (self.window_pos[1] + self.height / 4 * 3)])