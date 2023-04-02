from customtkinter import CTk, CTkFrame, CTkButton, CTkScrollableFrame, CTkLabel, CTkEntry, StringVar, CTkOptionMenu
from tkinter import filedialog
from pathlib import Path
import json

INT, FLT, STR, LST, DCT = range(5)
TYPES = ("Boolean", "Integer", "Float", "String", "List", "Dictionary")
DEFAULTS = (True, 0, .0, "text", [], {})
VARS = []


class Element(CTkFrame):
    def __init__(self, master, _type=TYPES[0], **kwargs):
        super(Element, self).__init__(master)
        self.type, self.value = StringVar(self), StringVar(self)
        self.value_entry = CTkEntry(self, textvariable=self.value)
        self.type_options = CTkOptionMenu(self, 100, values=TYPES)
        self.type_options.set(_type)
        self.pack(**kwargs), self.value_entry.pack(side="left"), self.type_options.pack(side="left")

    def get(self):
        return self.value.get()


class MenuBar(CTkFrame):
    def __init__(self, master, part_width=80, corner_radius=0, **kwargs):
        super(MenuBar, self).__init__(master)
        self.pack(fill="x", **kwargs)
        self.buttons, self.menus = [], []
        self.corner_radius = corner_radius
        self.part_width = part_width

    def add_command(self, label, command):
        button = CTkButton(self, self.part_width, text=label, command=command, corner_radius=self.corner_radius)
        button.pack(side="left", padx=1)
        self.buttons.append(button)

    def add_options(self, values, command=None):
        menu = CTkOptionMenu(self, self.part_width, corner_radius=self.corner_radius,
                             dynamic_resizing=False, values=values, command=command)
        menu.pack(side="left", padx=1)
        self.menus.append(menu)


class App(CTk):
    def __init__(self):
        super(App, self).__init__()
        self.filename = StringVar(self, "")
        self.filepath = ""
        self.data = []

        self.title("PyE-JSON")
        self.upper_menu, self.lower_menu = MenuBar(self), MenuBar(self, side="bottom")
        self.upper_menu.add_command("Open", self.open)
        self.upper_menu.add_command("Save", self.save)
        self.upper_menu.add_command("Save a copy", self.save_copy)
        self.heading_frame = CTkFrame(self)
        self.heading_frame.pack(fill="x", padx=10, pady=5)
        self.heading_label = CTkEntry(self.heading_frame, textvariable=self.filename, font=("Arial", 30, "normal"))
        self.heading_label.pack(side="left", padx=3, pady=3, fill="x", expand=True)
        self.heading_label_extension = CTkLabel(self.heading_frame, text=".json", font=("Arial", 30, "normal"))
        self.heading_label_extension.pack(side="right", padx=3)
        self.elements_frame = CTkScrollableFrame(self)
        # , label_text="No element to show.", label_font=("Arial", 24, "normal"), label_anchor="w")
        self.elements_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.lower_menu.add_command("Format", self.format)
        self._config()

    def _config(self):
        for data in self.data:
            print(data)
        menu = MenuBar(self.elements_frame, 100, None, anchor="s")
        menu.add_options(TYPES)
        menu.add_command("New", lambda: (Element(self.elements_frame, menu.menus[0].get(), anchor="w"), menu.pack_forget()))

    def open(self):
        path = Path(filedialog.askopenfilename(filetypes=("json {.json} {}", )))
        if not path.name:
            return
        self.filepath = path.parent
        self.filename.set(path.stem)
        with open(path, "r") as f:
            self.data = json.load(f)

    def save(self):
        file = self.filepath.join(self.filename.get())
        with open(file, "w") as f:
            json.dump(self.data, f)

    def save_copy(self):
        path = Path(filedialog.asksaveasfilename(filetypes=("json {.json} {}", )))
        if not path:
            return
        if not path.suffix:
            path = path.parent.joinpath(path.name + ".json")
        with open(path, "w") as f:
            json.dump(self.data, f)

    def format(self):
        pass


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
