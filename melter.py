import sys
import pyautogui
import time
import os


class MelterBot:
    # Initialized PyAutoGUI
    pyautogui.FAILSAFE = True

    class FinishExecution(Exception):
        pass

    def __init__(self, bags):
        self.bags = bags

        self.bags_len = len(self.bags)
        # Values X-Y all these values are considered for 1920 x 1080 screens

        # consumable's tab button
        self.cmX = 412
        self.cmY = 190

        # Inventory bags coordinates
        self.bags_coors = [{1: {"x": 1382, "y": 561}},
                           {2: {"x": 1421, "y": 560}},
                           {3: {"x": 1469, "y": 558}},
                           {4: {"x": 1516, "y": 563}},
                           {5: {"x": 1564, "y": 559}},
                           {6: {"x": 1611, "y": 562}},
                           {7: {"x": 1657, "y": 561}},
                           {8: {"x": 1698, "y": 560}},
                           {9: {"x": 1745, "y": 558}}
                           ]

        self.cubbies_coors = [
            {1: {"x": 1400, "y": 618}},
            {2: {"x": 1400, "y": 685}},
            {3: {"x": 1400, "y": 779}},
            {4: {"x": 1400, "y": 845}},

            {5: {"x": 1470, "y": 620}},
            {6: {"x": 1470, "y": 690}},
            {7: {"x": 1470, "y": 760}},
            {8: {"x": 1470, "y": 830}},

            {9: {"x": 1551, "y": 619}},
            {10: {"x": 1551, "y": 689}},
            {11: {"x": 1551, "y": 759}},
            {12: {"x": 1551, "y": 829}},

            {13: {"x": 1628, "y": 622}},
            {14: {"x": 1628, "y": 692}},
            {15: {"x": 1628, "y": 762}},
            {16: {"x": 1628, "y": 832}},

            {17: {"x": 1705, "y": 619}},
            {18: {"x": 1705, "y": 689}},
            {19: {"x": 1705, "y": 759}},
            {20: {"x": 1705, "y": 829}},

            {21: {"x": 1775, "y": 621}},
            {22: {"x": 1775, "y": 691}},
            {23: {"x": 1775, "y": 761}},
            {24: {"x": 1775, "y": 831}},

            {25: {"x": 1853, "y": 624}},
            {26: {"x": 1853, "y": 694}},
            {27: {"x": 1853, "y": 764}},
            {28: {"x": 1853, "y": 834}},
        ]

        # Remove all gems button
        self.rmX = 196
        self.rmY = 850

    def move_and_click(self, x, y, btn):
        pyautogui.moveTo(x, y)
        pyautogui.click(button=btn)

    def clear_gems(self):
        self.move_and_click(self.rmX, self.rmY, 'primary')
        self.move_and_click(self.cmX, self.cmY, 'primary')

    def clear_gems2(self):
        self.move_and_click(self.rmX, self.rmY, 'primary')

    def incr_decr_gem(self):
        incx = 511
        incy = 793
        self.move_and_click(incx, incy, 'primary')
        decx = 505
        decy = 773
        self.move_and_click(decx, decy, 'primary')

    def combine_gem(self):
        combinex = 656
        combiney = 663
        self.move_and_click(combinex, combiney, 'primary')

    def cycle_gems(self):
        self.incr_decr_gem()
        self.combine_gem()
        time.sleep(1.4)
        self.clear_gems()

    def find_gem_to_melt(self, img):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.argv[0])
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))

        image_path = os.path.join(base_path, 'imgs', img)

        try:
            image_pos = pyautogui.locateOnScreen(image_path, confidence=0.9)

            if image_pos:
                # print(f"Image found at: {image_pos}")
                return True
            else:
                return False

        except pyautogui.ImageNotFoundException:
            return False

    # Main method
    def inv_bags(self, coors_list, btn_type):
        try:
            for coors in coors_list:
                for (key, value) in coors.items():
                    if key in self.bags:
                        x = value["x"]
                        y = value["y"]
                        self.move_and_click(x, y, btn_type)
                        self.click_cubbies()

        except self.FinishExecution:
            return

    def inventory_squares(self, btn_type):
        for coors in self.cubbies_coors:
            for (key, value) in coors.items():
                x = 0
                y = 0
                for (key2, value2) in value.items():
                    if key2 == "x":
                        x = value2
                    else:
                        y = value2

                self.move_and_click(x, y, btn_type)

                time.sleep(0.3)
                # FOUND A GEM
                if self.find_gem_to_melt('gemtxt.png') or self.find_gem_to_melt('gemtxt2.png'):

                    time.sleep(0.2)
                    # Just one gem
                    if self.find_gem_to_melt('justonegem.png'):
                        self.clear_gems2()

                    # MORE THAN ONE GEM
                    elif self.find_gem_to_melt('morethanone.png'):
                        self.cycle_gems()

                else:
                    # NOT A GEM OR JUST ONE GEM
                    self.clear_gems()

    def click_invBags(self):
        self.inv_bags(self.bags_coors, 'primary')

    def click_cubbies(self):
        self.inventory_squares('secondary')

    def timer(self):
        # Countdown timer
        print("Starting", end="")
        for i in range(0, 3):
            print(".", end="")
            time.sleep(1)

        print("Initializing...")

    def melt(self):
        try:
            self.timer()
            self.move_and_click(self.cmX, self.cmY, 'primary')
            time.sleep(0.3)
            self.click_invBags()

            print("\nFinished iterating through bags. Exiting...")

        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            sys.exit()
