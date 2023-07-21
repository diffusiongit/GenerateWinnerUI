import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import csv
import random

class NameFloaterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Name Floater")
        self.root.geometry("1000x1000")

        self.select_file_button = tk.Button(root, text="Select CSV File", command=self.select_csv_file)
        self.select_file_button.pack()

        self.generate_winner_button = tk.Button(root, text="Generate Winner", state="disabled", command=self.generate_winner)
        self.generate_winner_button.pack()

        self.pause_button = tk.Button(root, text="Pause/Reset", command=self.toggle_animation)
        self.pause_button.pack()

        self.total_count_label = tk.Label(root, text="Total Names: 0")
        self.total_count_label.pack(side="top")

        self.canvas = tk.Canvas(root, width=1000, height=800, bg="black")
        self.canvas.pack()

        self.names = []
        self.name_labels = {}
        self.trail_circles = {}
        self.animation_paused = True
        self.all_loaded = False
        self.winner_selected = False

    def select_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.file_path = file_path
            self.load_names()

    def load_names(self):
        try:
            with open(self.file_path, 'r') as csv_file:
                participants = list(csv.reader(csv_file))
                self.names = [participant[0] for participant in participants]
                self.total_count_label.config(text="Total Names: {}".format(len(self.names)))
                self.create_name_labels()
                self.generate_winner_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_name_labels(self):
        for name in self.names:
            x = random.randint(50, 950)
            y = random.randint(50, 950)
            label = self.canvas.create_text(x, y, text=name, font=("Arial", 12), fill="black", anchor="w")
            self.name_labels[label] = {'x': x, 'y': y, 'dx': random.uniform(-2, 2), 'dy': random.uniform(-2, 2)}
            #self.float_name(label)
        self.all_loaded = True
        if not self.animation_paused:
            self.start_animation()

    def start_animation(self):
        if self.all_loaded:
            self.animation_paused = False
            self.animate_label()

    def animate_label(self):
        if self.animation_paused:
            return
        for label, values in list(self.name_labels.items()):
            x = values['x']
            y = values['y']
            dx = values['dx']
            dy = values['dy']

            x += dx
            y += dy
            #print(x,y)
            _, _, label_width, _ = self.canvas.bbox(label)
            if x < 0:
                x = 0
                dx = abs(dx)
                #self.canvas.itemconfigure(label, fill=self.get_random_color())
            elif x > self.canvas.winfo_width():
                x = self.canvas.winfo_width()
                dx = -abs(dx)
                #self.canvas.itemconfigure(label, fill=self.get_random_color())
            if y < 0:
                y = 0
                dy = abs(dy)
                #self.canvas.itemconfigure(label, fill=self.get_random_color())
            elif y > self.canvas.winfo_height():
                y = self.canvas.winfo_height()
                dy = -abs(dy)
                #self.canvas.itemconfigure(label, fill=self.get_random_color())

            #self.canvas.coords(label, x, y)
            self.canvas.move(label, x - values['x'], y - values['y'])
            self.name_labels[label]['x'] = x
            self.name_labels[label]['y'] = y
            self.name_labels[label]['dx'] = dx
            self.name_labels[label]['dy'] = dy

        if self.winner_selected:
            self.pulse_winner_label()
        self.root.after(10, self.animate_label)


    def toggle_animation(self):
        self.animation_paused = not self.animation_paused
        if self.animation_paused:
            for label in self.name_labels.keys():
                self.canvas.itemconfigure(label, fill='lightblue')
        else:
            for label in self.name_labels.keys():
                self.canvas.itemconfigure(label, fill='lightblue')
            self.start_animation()

    def generate_winner(self):
        if self.winner_selected:
            return
        winner_label_id = random.choice(list(self.name_labels.keys()))
        self.canvas.itemconfigure(winner_label_id, fill='red')
        self.winner_label_id = winner_label_id
        for label in self.name_labels:
            if label != winner_label_id:
                self.canvas.itemconfigure(label, fill='lightblue')
        self.winner_selected = True
        self.generate_winner_button.config(state="disabled")

    def pulse_winner_label(self):
        pulsing_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        if self.winner_label_id:
            current_color = self.canvas.itemcget(self.winner_label_id, 'fill')
            if current_color == 'lightblue':
                next_color = 'red'  # Special case for initial color
            else:
                next_color_index = (pulsing_colors.index(current_color) + 1) % len(pulsing_colors)
                next_color = pulsing_colors[next_color_index]
            self.canvas.itemconfigure(self.winner_label_id, fill=next_color)
            # Increase font size for the winner label
            if current_color == 'red':
                self.canvas.itemconfigure(self.winner_label_id, font=("Arial", 26))


        self.root.after(500, self.pulse_winner_label)



    def get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

root = tk.Tk()
app = NameFloaterUI(root)
root.mainloop()
