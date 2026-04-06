import pygame as pyg
import random as rnd

# test = [[12, 23], [0.2, 135], [213, 2]]
# test = sorted(test, key=lambda x: x[1])
# print(test)



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

class email_inbox:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        
        self.window_pos = [WIDTH / 4, HEIGHT / 6]
        self.exit_icon_pos = [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]] # To be used for checking if you click on the exit icon

        self.emails = [] # [list of email class items]
        self.open_email = None # Shows what email has been clicked on

        self.email_timer = [0, 180 * 60] # [Current time, at whattime the next email spawns (in ticks)]
        # self.email_timer = [120 * 60, 10 * 60] # test

        self.email_multiplier = 2.5 # Multiplier for how much money you get for reporting emails, can be upgraded in the shop and by reporting emails correctly
    
    # ------------------------ RETURNS -----------------------

    def get_exit_icon_pos(self):
        return self.exit_icon_pos
    
    # ------------------------ EMAILS -----------------------

    def increment_timer(self):
        self.email_timer[0] += 1
        if self.email_timer[0] >= self.email_timer[1]:
            self.email_timer[0] = 0
            self.emails.append(email(len(self.emails), self))

    def update_all_emails(self, inbox):
        index = 0
        for email in self.emails:
            email.update_rect(index, inbox)
            index += 1

    def check_email_click(self, mouse_pos, inbox):
        if self.open_email != None: # If you have an email open, check if you clicked on the close button or a reporting button
            # Close button
            if mouse_pos[0] >= self.window_pos[0] + self.width / 2 - 100 and mouse_pos[0] <= self.window_pos[0] + self.width / 2 - 5:
                if mouse_pos[1] >= self.window_pos[1] + 50 and mouse_pos[1] <= self.window_pos[1] + 100:
                    self.open_email = None
                    return
            
            # Report as Scam
            if mouse_pos[0] >= self.window_pos[0] + self.width / 8 - 150 and mouse_pos[0] <= self.window_pos[0] + self.width / 8 + 50:
                if mouse_pos[1] >= self.window_pos[1] + self.height / 4 * 3 - 50 and mouse_pos[1] <= self.window_pos[1] + self.height / 4 * 3 - 20:
                    if self.open_email.email_type != "Real":
                        inbox.overall_money_multiplier_timers.append([self.email_multiplier, 60 * 60, 60 * 60]) # If you report an email as a scam and it is a scam, add a 2.5x multiplier for 3 minutes
                    else:
                        inbox.overall_money_multiplier_timers.append([0.5, 30 * 60, 30 * 60]) # If you report an email as a scam and it is real, add a 0.5x multiplier for 3 minutes
                    
                    inbox.overall_money_multiplier_timers = sorted(inbox.overall_money_multiplier_timers, key=lambda x:x[1]) # Sorts the multipliers so that the one that will dissapear first at first in queue

                    self.emails.remove(self.open_email) # Remove the email you just reported from the inbox
                    self.open_email = None
                    self.update_all_emails(inbox)
                    return 
            
            # Send to Security Team
            if mouse_pos[0] >= self.window_pos[0] + self.width / 8 * 2 - 100 and mouse_pos[0] <= self.window_pos[0] + self.width / 8 * 2 + 100: 
                if mouse_pos[1] >= self.window_pos[1] + self.height / 4 * 3 - 50 and mouse_pos[1] <= self.window_pos[1] + self.height / 4 * 3 - 20:
                    inbox.overall_money_multiplier_timers.append([self.email_multiplier / 2, 60 * 60, 60 * 60]) # You are guaranteed to select the correct answer so you get a smaller multiplier

                    inbox.overall_money_multiplier_timers = sorted(inbox.overall_money_multiplier_timers, key=lambda x:x[1]) # Sorts the multipliers so that the one that will dissapear first at first in queue
                    
                    self.emails.remove(self.open_email) # Remove the email you just reported from the inbox
                    self.open_email = None
                    self.update_all_emails(inbox)
                    return 
            
            # Mark as Valid
            if mouse_pos[0] >= self.window_pos[0] + self.width / 8 * 3 - 100 + 50 and mouse_pos[0] <= self.window_pos[0] + self.width / 8 * 3 + 100:    
                if mouse_pos[1] >= self.window_pos[1] + self.height / 4 * 3 - 50 and mouse_pos[1] <= self.window_pos[1] + self.height / 4 * 3 - 20:
                    if self.open_email.email_type == "Real":
                        inbox.overall_money_multiplier_timers.append([self.email_multiplier, 60 * 60, 60 * 60]) # If you report an email as real and it is real, add a 2.5x multiplier for 3 minutes
                    else:
                        inbox.overall_money_multiplier_timers.append([0.5, 30 * 60, 30 * 60]) # If you report an email as real and it is a scam, add a 0.5x multiplier for 3 minutes
                        
                    inbox.overall_money_multiplier_timers = sorted(inbox.overall_money_multiplier_timers, key=lambda x:x[1]) # Sorts the multipliers so that the one that will dissapear first at first in queue
                    
                    self.emails.remove(self.open_email) # Remove the email you just reported from the inbox
                    self.open_email = None
                    self.update_all_emails(inbox)
                    return  
        else:
            for email in self.emails:
                mouse_rect = pyg.Rect(mouse_pos[0], mouse_pos[1], 10, 10)
                if mouse_rect.colliderect(email.rect):
                    self.open_email = email
                    return

    # ------------------------ DISPLAY -----------------------

    def show_emails(self, screen):
        # Draws the email inbox window then the emails, then the outlines so they are on top
        pyg.draw.rect(screen, "light gray", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3])
        
        display_text("Email Inbox", self.window_pos[0] + self.width / 4, self.window_pos[1] + 25, "center", 30, "black", screen)

        if self.open_email == None:
            for email in self.emails:
                if email.rect.bottom > self.window_pos[1] + self.height / 4 * 3 + 100: # If the email is below the bottom of the inbox, don't draw it
                    break
                pyg.draw.rect(screen, "white", email.rect)
                display_text(email.sender, email.rect.x + 10, email.rect.y + 20, "topleft", 20, "black", screen)
                display_text(email.title, email.rect.x + 10, email.rect.y + 60, "topleft", 15, "black", screen)
                pyg.draw.rect(screen, "black", email.rect, 5)
        else:
            pyg.draw.rect(screen, "white", [self.window_pos[0], self.window_pos[1] + 50, self.width / 2, self.height / 4 * 3 - 50]) # Drawsa a white background for the opened email
            # Needs a close button
            pyg.draw.rect(screen, "red", [self.window_pos[0] + self.width / 2 - 100, self.window_pos[1] + 50, 95, 50], 5)
            display_text("Close", self.window_pos[0] + self.width / 2 - 50, self.window_pos[1] + 75, "center", 20, "black", screen)

            display_text(self.open_email.title, self.window_pos[0] + 10, self.window_pos[1] + 75, "topleft", 40, "black", screen)
            display_text(self.open_email.sender, self.window_pos[0] + 10, self.window_pos[1] + 115, "topleft", 30, "black", screen)

            whole_text = self.open_email.body_text.split("\n")
            index = 0
            for text in whole_text:
                while len(text) > 70: # Since pygame doesn't have text wrapping, I split the text into multiple chunks
                    check_space = 70
                    while text[check_space] != " ": # I try to split the text at a space words make sense
                        check_space -= 1
                        if check_space == 0:
                            check_space = 69 # Since I add 1 after the loop
                            break
                    check_space += 1 # To get rid of the space at the start of the next line
                    display_text(text[:check_space], self.window_pos[0] + 10, self.window_pos[1] + 155 + index * 25, "topleft", 20, "black", screen)
                    text = text[check_space:]
                    index += 1

                display_text(text, self.window_pos[0] + 10, self.window_pos[1] + 155 + index * 25, "topleft", 20, "black", screen)
                index += 1

            # Draws the "report as scam", "send to security team", and "mark as valid" buttons at the bottom of the email
            pyg.draw.rect(screen, "red", [self.window_pos[0] + self.width / 8 - 150, self.window_pos[1] + self.height / 4 * 3 - 50, 200, 30])
            display_text("Report as Scam", self.window_pos[0] + self.width / 8 - 50, self.window_pos[1] + self.height / 4 * 3 - 50 + 15, "center", 15, "black", screen)
            pyg.draw.rect(screen, "black", [self.window_pos[0] + self.width / 8 - 150, self.window_pos[1] + self.height / 4 * 3 - 50, 200, 30], 2)

            pyg.draw.rect(screen, "light gray", [self.window_pos[0] + self.width / 8 * 2 - 100, self.window_pos[1] + self.height / 4 * 3 - 50, 200, 30])
            display_text("Send to Security Team", self.window_pos[0] + self.width / 8 * 2, self.window_pos[1] + self.height / 4 * 3 - 50 + 15, "center", 15, "black", screen)
            pyg.draw.rect(screen, "black", [self.window_pos[0] + self.width / 8 * 2 - 100, self.window_pos[1] + self.height / 4 * 3 - 50, 200, 30], 2)

            pyg.draw.rect(screen, "green", [self.window_pos[0] + self.width / 8 * 3 - 100 + 50, self.window_pos[1] + self.height / 4 * 3 - 50, 200, 30])
            display_text("Mark as Valid", self.window_pos[0] + self.width / 8 * 3 + 50, self.window_pos[1] + self.height / 4 * 3 - 50 + 15, "center", 15, "black", screen)
            pyg.draw.rect(screen, "black", [self.window_pos[0] + self.width / 8 * 3 - 100 + 50, self.window_pos[1] + self.height / 4 * 3 - 50, 200, 30], 2)

        
        pyg.draw.rect(screen, "black", [self.window_pos[0], self.window_pos[1], self.width / 2, self.height / 4 * 3], 5)
        pyg.draw.line(screen, "black", [self.window_pos[0], self.window_pos[1] + 50], [self.window_pos[0] + self.width / 2, self.window_pos[1] + 50], 2)
        screen.blit(exit_icon, [self.window_pos[0] + self.width / 2 - 50, self.window_pos[1]])

        # Draws a light blue box that reaches the bottom of the screen to hide purchases that shouldn't be on screen
        pyg.draw.rect(screen, "light blue", [self.window_pos[0], self.window_pos[1] + self.height / 4 * 3, self.width / 2, self.height - (self.window_pos[1] + self.height / 4 * 3)])




class email:
    def __init__(self, index, inbox):
        self.email_type = "" # If it's a real email, or what type of scam it is

        self.body_text = "" # What the email will say
        self.sender = ""
        self.title = ""

        self.index = index # What index the email is at in the inbox
        self.rect = pyg.Rect(inbox.window_pos[0] + 25, inbox.window_pos[1] + 75 + self.index * 110, inbox.width / 2 - 50, 100) # The rect of the email, used for drawing and clicking

        self.generate_email()

    def update_rect(self, new_index, inbox):
        self.index = new_index
        self.rect = pyg.Rect(inbox.window_pos[0] + 25, inbox.window_pos[1] + 75 + self.index * 110, inbox.width / 2 - 50, 100)

    def generate_email(self):
        self.get_sender() # Gets a completely random sender


        if rnd.randint(1,2) == 1:
            self.email_type = "Real"
        else:
            scam_types = ["Impersonation", "Urgency", "Too good", "Typos"]
            # scam_types = ["Impersonation"]
            self.email_type = rnd.choice(scam_types)
            # Replace certain identifiers within the body text with extra words that make the email a certain scam type
            if self.email_type == "Impersonation":
                if rnd.randint(1,2) == 1:
                    self.sender = self.sender.replace("e", "3")
                    self.sender = self.sender.replace("o", "0")
                    self.sender = self.sender.replace("l", "1")
                else:
                    self.sender = self.sender + "_"
            
        
        # Gets a random title and body text (with the same random number chosen in get_title)
        if self.email_type == "Impersonation": # If impersonation, use real emails
            index = self.get_title("Real")
            self.get_body_text(index, "Real")
        else:
            index = self.get_title(self.email_type)
            self.get_body_text(index, self.email_type)
        
        self.sender = self.sender + "@gmail.com"

    def get_sender(self):
        f = open("emails/senders.txt", "r")
        possible_senders = []
        for line in f:
            if line.strip() != "":
                possible_senders.append(line.strip())

        self.sender = rnd.choice(possible_senders)
        f.close()

    def get_title(self, email_type):
        f = open("emails/" + email_type + "/titles.txt", "r")
        possible_titles = []
        for line in f:
            if line.strip() != "":
                possible_titles.append(line.strip())
        
        index = rnd.randint(0, len(possible_titles) - 1)
        self.title = possible_titles[index]
        f.close()
        return index

    def get_body_text(self, index, email_type):
        f = open("emails/" + email_type + "/body text.txt", "r")
        possible_body_text = []
        new_body_text = "" # Collects all of the body text into one string, appends to the possible body text list, then resets
        for line in f:
            if line.strip() != "-":
                new_body_text += line
            else:
                possible_body_text.append(new_body_text)
                new_body_text = ""
        possible_body_text.append(new_body_text) # Appends the last body text

        self.body_text = possible_body_text[index]
        f.close()
        return
