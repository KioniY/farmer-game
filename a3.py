import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *


# Implement your classes here
class InfoBar(AbstractGrid):
    """InfoBar should inherit from AbstractGrid, it is a grid with 2 rows and 3
columns., which displays information to the user about the number of days elapsed in the game,
as well as the player’s energy and health. The InfoBar should span the entire width of the farm
and inventory combined."""
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """Sets up this InfoBar to be an AbstractGrid with the appropriate
        number of rows and columns, and the appropriate width and height"""
        super().__init__(
            master,
            dimensions=(2, 3),
            size=(FARM_WIDTH + INVENTORY_WIDTH, INFO_BAR_HEIGHT)
        )
        self._master =master
        self.annotate_position((0, 0), "Day:", font=HEADING_FONT)
        self.annotate_position((1, 0), "1")
        self.annotate_position((0, 1), "Money:", font=HEADING_FONT)
        self.annotate_position((1, 1), "$0")
        self.annotate_position((0, 2), "Energy:", font=HEADING_FONT)
        self.annotate_position((1, 2), "100")

        self.redraw(1,0,100)
    def redraw(self, day: int, money: int, energy: int) -> None:
        """Clears the InfoBar and redraws it to display the provided day,
        money, and energy. E.g. in Figure 3, this method was called with day
        = 1, money = 0, and energy = 100."""

        self.clear()
        self.annotate_position((0, 0), "Day:", font=HEADING_FONT)
        self.annotate_position((1, 0), f"{day}")
        self.annotate_position((0, 1), "Money:", font=HEADING_FONT)
        self.annotate_position((1, 1), "$"+f"{money}")
        self.annotate_position((0, 2), "Energy:", font=HEADING_FONT)
        self.annotate_position((1, 2), f"{energy}")




class FarmView(AbstractGrid):
    """The FarmView is a grid displaying the farm map, player, and plants."""

    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int, int],
                 size: tuple[int, int], **kwargs) -> None:
        """ Sets up the FarmView to be an AbstractGrid with the appropriate
        dimensions and size, and creates an instance attribute of an empty
        dictionary to be used as an image cache."""

        super().__init__(master,
                         dimensions=dimensions,
                         size=(FARM_WIDTH,FARM_WIDTH))
        self._cache = {}


    def redraw(self, ground: list[str],
               plants: dict[tuple[int, int], 'Plant'],
               player_position: tuple[int, int],
               player_direction: str) -> None:
        """Clears the farm view, then creates (on the FarmView instance)
        the images for the ground, then the plants, then the player. That is, the player and plants should
render in front of the ground, and the player should render in front of the
plants."""
        self.clear()
        # draw grounds
        for index, row in enumerate(ground):
            i = index
            row = row
            for index, column in enumerate(row):
                j = index
                col = column
                point = (i, j)
                position= self.get_midpoint(point)
                pic= IMAGES.get(col)
                path = "images/" + pic
                image = get_image(path, self.get_cell_size(), self._cache)

                self.create_image(position, image=image)


        # draw plants
        for key, value in plants.items():
            x, y = self.get_midpoint(key)
            pname = "images/" + get_plant_image_name(value)
            ima=get_image(pname, self.get_cell_size(), self._cache)

            self.create_image(x, y, image=ima)

        # draw player
        player=IMAGES.get(player_direction)

        photo = "images/" + player
        image=get_image(photo, self.get_cell_size(), self._cache)

        position = self.get_midpoint(player_position)
        self.create_image(position, image=image)

    def clear_cache(self):
        self._cache = {}





class ItemView(tk.Frame):
    """The ItemView is a frame displaying relevant information
and buttons for a single item. There are 6 items available in the game"""
    """The ItemView is a frame displaying relevant information
   and buttons for a single item. There are 6 items available in the game"""

    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str],
                                                 None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        super().__init__(master, bg=INVENTORY_COLOUR, bd=1, relief=tk.RAISED)
        self.item_name = item_name
        self.amount = amount
        self.select_command = select_command
        self.sell_command = sell_command
        self.buy_command = buy_command

        sell_price = SELL_PRICES[item_name]
        if 'Seed' in item_name:
            buy_price = BUY_PRICES[item_name]
        else:
            buy_price = "N/A"


        # left frame of label with item_name sell_price and buy_price
            # left frame of label with item_name sell_price and buy_price
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.name_label = tk.Label(self.left_frame,
                                   text=f"{item_name:}" + " " + f"{amount}")
        self.name_label.pack(side="top", fill="both", expand=True)

        self.sell_label = tk.Label(self.left_frame, text=f"Sell price:"
                                                    f" ${sell_price}")
        self.sell_label.pack(side="top", fill="both", expand=True)
        self.buy_label = tk.Label(self.left_frame, text=f"Buy price:"
                                                    f" ${buy_price}")
        self.buy_label.pack(side="top", fill="both", expand=True)

        # right frame of two buttons
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)


        if 'Seed' in item_name:
            self.buy_button = tk.Button(self.right_frame, text="Buy",
                                        command=self.buy_command)
            self.buy_button.pack(side="right", fill="x", expand=True)


        self.sell_button = tk.Button(self.right_frame, text="Sell",
                                     command=self.sell_command)
        self.sell_button.pack(side="right", fill="x", expand=True)


        self.bind("<Button-1>", select_command)
        self.left_frame.bind("<Button-1>", select_command)
        self.right_frame.bind("<Button-1>", select_command)
        self.name_label.bind("<Button-1>", select_command)
        self.sell_label.bind("<Button-1>", select_command)
        self.buy_label.bind("<Button-1>", select_command)



    def update(self, amount: int, selected: bool = False) -> None:
        """Updates the text on the label, and the colour of this ItemView
        appropriately."""
        self._amount = amount

        self.name_label.configure(text=f"{self.item_name}: " + f""
                                                               f"{self._amount}")
        if self._amount > 0:
            self.name_label.configure(bg=INVENTORY_COLOUR)
            self.sell_label.configure(bg=INVENTORY_COLOUR)
            self.buy_label.configure(bg=INVENTORY_COLOUR)
            self.configure(bg=INVENTORY_COLOUR)
            self.left_frame.configure(bg=INVENTORY_COLOUR)
            self.right_frame.configure(bg=INVENTORY_COLOUR)


        else:
            self.name_label.configure(bg=INVENTORY_EMPTY_COLOUR)
            self.sell_label.configure(bg=INVENTORY_EMPTY_COLOUR)
            self.buy_label.configure(bg=INVENTORY_EMPTY_COLOUR)
            self.configure(bg=INVENTORY_EMPTY_COLOUR)
            self.left_frame.configure(bg=INVENTORY_EMPTY_COLOUR)
            self.right_frame.configure(bg=INVENTORY_EMPTY_COLOUR)

        if selected is True:
            self.name_label.configure(bg=INVENTORY_SELECTED_COLOUR)
            self.sell_label.configure(bg=INVENTORY_SELECTED_COLOUR)
            self.buy_label.configure(bg=INVENTORY_SELECTED_COLOUR)
            self.configure(bg=INVENTORY_SELECTED_COLOUR)
            self.left_frame.configure(bg=INVENTORY_SELECTED_COLOUR)
            self.right_frame.configure(bg=INVENTORY_SELECTED_COLOUR)






class FarmGame(object):
    """FarmGame is the controller class for the overall game. The controller
    is responsible for creating and
maintaining instances of the model and view classes, event handling,
and facilitating communication between the model and view classes."""
    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """set the title of the window"""
        master.title('Farm Game')
        self._master = master
        # Create the title banner
        self._cache = {}

        self._Model = FarmModel(map_file)
        self._player = self._Model.get_player()
        self._inventory = self._player.get_inventory()
        dimensions = self._Model.get_dimensions()
        banner_image = get_image("images/header.png",
                                 (FARM_WIDTH + INVENTORY_WIDTH,
                                  BANNER_HEIGHT), self._cache)
        self._label = tk.Label(master, image=banner_image)
        self._label.pack(side="top", fill="x", expand=True)
        #Next Day Button
        self._button = tk.Button(master, text="Next day",
                                 command=self.next_day_button)
        self._button.pack(side="bottom")
        # infobar
        self.info_bar = InfoBar(master)
        self.info_bar.pack(side="bottom", fill="both", expand=True)
        # create farmview
        self.farmview = FarmView(master, dimensions=dimensions,
                                 size=(FARM_WIDTH, FARM_WIDTH))
        self.farmview.pack(side="left", fill="both")


        # create itemview
        frame = tk.Frame()
        frame.pack(side="left", fill="both", expand=True)

        self._item_views = []
        for item_name in ITEMS:
            item = item_name
            if item in self._inventory:
                amount = self._inventory[item]


            else:
                amount = 0
            dic = {item:amount}

            for name, value in dic.items():

                itemview = ItemView(frame, item_name=name, amount=value,
                                     select_command=lambda
                                      _, name=name:self.select_item(
                                        name), sell_command=
                                    lambda name=name:self.sell_item(
                        name), buy_command= lambda name=name:self.buy_item(
                        name))

                itemview.pack(side="top", fill="both", expand=True)
                itemview.update(amount)

                self._item_views.append(itemview)




        # – Bind the handle keypress method to the ‘<KeyPress>’ event
        master.bind('<KeyPress>', self.handle_keypress)


        # Call the redraw method to ensure the view draws according to the
        # current model state.
        self.redraw()


        # create the menu
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Quit", command=self.quit)
        filemenu.add_command(label="Map selection", command=self.map_selection)
    def quit(self):
        self._master.destroy()


    def map_selection(self):
        self._filename = filedialog.askopenfilename()
        self.farmview.clear_cache()
        self._Model = FarmModel(self._filename)
        dimensions = self._Model.get_dimensions()
        self.farmview.set_dimensions(dimensions)
        self._player=self._Model.get_player()
        self._inventory=self._player.get_inventory()

        self.redraw()





    def next_day_button(self):
        self._Model.new_day()
        self.info_bar.redraw(self._Model.get_days_elapsed(),
                             self._player.get_money(),
                             self._player.get_energy())
        self.farmview.redraw(self._Model.get_map(),
                             self._Model.get_plants(),
                             self._Model.get_player_position(),
                             self._Model.get_player_direction())

    def redraw(self):
        self.info_bar.redraw(self._Model.get_days_elapsed(),
                         self._player.get_money(), self._player.get_energy())

        self.farmview.redraw(self._Model.get_map(),
                              self._Model.get_plants(),
                              self._Model.get_player_position(),
                              self._Model.get_player_direction())

        # Iterate over self._item_views and update each in turn
        for i, item_view in enumerate(self._item_views):

            item_name = ITEMS[i]

            if item_name in self._inventory:
                amount = self._inventory[item_name]
            else:
                amount = 0
            idx = ITEMS.index(item_name)
            self._item_views[idx].update(amount, selected=False)












            # item_view.update(amount, selected=False)



    def handle_keypress(self, event: tk.Event) -> None:
        # this is use keyboard



        if event.char in [UP, DOWN, RIGHT, LEFT]:

            self._Model.move_player(event.char)
            self.redraw()
            #If that position does not contain soil, a plant already exists
            # in that spot, or a seed is not currently selected, do nothing.
        if event.char == 'p':
            position = self._Model.get_player_position()
            x = position[0]
            y = position[1]
            if self._player.get_selected_item() != None:
                item = self._player.get_selected_item().split(" ")
                map_data = self._Model.get_map()
                row = map_data[x]
                element = row[y]


                if 'Seed' in item:
                    if element =="G":
                        return None
                    else:

                        plants = self._Model.get_plants()

                        if plants.get(position) != None:
                            return None
                        else:
                            if item[0] == 'Potato':
                                plant = PotatoPlant()

                            elif item[0] == 'Kale':
                                plant = KalePlant()
                            elif item[0] == 'Berry':
                                plant = BerryPlant()
            else:
                return None

            self._Model.add_plant(position, plant)
            item_name = item[0]+" "+item[1]
            print(item_name)
            self._player.remove_item((item_name, 1))
            print(self._inventory)

            self.redraw()
        # harvest the plant
        if event.char == 'h':
            position = self._Model.get_player_position()
            plants = self._Model.get_plants()
            if plants.get(position) is None:
                return None
            plant = plants.get(position)
            if plant.can_harvest() is False:
                return None
            item = plant.harvest()
            self._Model.harvest_plant(position)
            self._player.add_item(item)
            self._Model.remove_plant(position)
            self.redraw()
        #  remove the plant
        if event.char == 'r':
            position = self._Model.get_player_position()
            plants = self._Model.get_plants()
            # If no plant exists at
            # the player’s currently location, do nothing.
            if plants.get(position) is None:
                return None
            else:
                self._Model.remove_plant(position)
                self.redraw()
        # till the soil
        if event.char == 't':
            position = self._Model.get_player_position()
            x = position[0]
            y = position[1]
            map_data = self._Model.get_map()
            row = map_data[x]
            element = row[y]
            if element != "U":
                    return None
            else:
                self._Model.till_soil(position)
            self.redraw()
        # untill the soil
        if event.char == 'u':
            position = self._Model.get_player_position()
            x = position[0]
            y = position[1]
            plants = self._Model.get_plants()
            map_data = self._Model.get_map()
            row = map_data[x]
            element = row[y]
            if plants.get(position) is not None:
                return None

            elif element != "S":
                return None
            else:
                self._Model.untill_soil(position)
            self.redraw()

    # If the player has a non-zero amount of that item, set the
    # selected item to the name of that item
    def select_item(self, item_name):

        amount = self._player.get_inventory().get(item_name)
        if self._player.get_inventory().get(item_name) is not None:

            if self._player.get_inventory().get(item_name) > 0:

                self._player.select_item(item_name)
        else:
            return None

        self.redraw()
        idx = ITEMS.index(item_name)
        self._item_views[idx].update(amount, selected=True)
        print(self._item_views[idx])

    # buy the item
    def buy_item(self, item_name):
        price = BUY_PRICES[item_name]
        self._player.buy(item_name, price)
        amount = self._inventory.get(item_name, 0)
        idx = ITEMS.index(item_name)
        self._item_views[idx].update(amount,
                                     self._player.get_selected_item() == \
                                     item_name)
        self.redraw()

    # If player has a non-zero quantity of that item, attempt to sell
    # one of the item
    def sell_item(self, item_name):
        price= SELL_PRICES[item_name]
        self._player.sell(item_name, price)
        amount = self._inventory.get(item_name, 0)
        idx = ITEMS.index(item_name)
        self._item_views[idx].update(amount,
                                           self._player.get_selected_item() ==\
            item_name)
        self.redraw()








def play_game(root: tk.Tk, map_file: str) -> None:

    game = FarmGame(root, map_file)
    root.mainloop()
    pass  # Implement your play_game function here


def main() -> None:
    root = tk.Tk()
    map_file = "maps/map1.txt"
    play_game(root, map_file)
    pass  # Implement your main function here


if __name__ == '__main__':
    main()
