#Olena
import tkinter
from tkinter import messagebox
import csv
from matplotlib import pyplot as plt
import matplotlib.image as img
from PIL import Image, ImageTk

Yellow = "#feb132"
Green ="#30a232"
Orange ="#e96024"
Red = "#c0101b"
bmi_categories_with_colors = [
    ("Underweight", 18.5, Yellow),
    ("Normal weight", 24.9, Green),
    ("Overweight", 29.9, Orange),
    ("Obese", float('inf'), Red)
]
def calculate():
    name = name_txt.get().title()
    height = height_txt.get()
    weight = weight_txt.get()
    if name == "" or height == "" or weight == "":
        messagebox.showerror(title="Invalid Input", message="All fields must be filled!")
    elif not name.isalpha() and name.isspace():
        messagebox.showerror(title="Invalid Input", message="Only letters are allowed in a field \"name\".")
    elif not height.isdigit():
        messagebox.showerror(title="Invalid Input", message="Only numbers are allowed in a field \"height\".")
    elif not weight.isdigit():
        messagebox.showerror(title="Invalid Input", message="Only numbers are allowed in a field \"weight\".")
    else:
        bmi = float(weight)/(float(height)/100)**2
        find_bmi_category_and_color(bmi)
        category, color = find_bmi_category_and_color(bmi)
        label1.config(text=f"{name}'s BMI is: {bmi:.1f}", bg=color, fg="white")
    # Write data to CSV
    with open("bmi_data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([name, height, weight, bmi])

def find_bmi_category_and_color(bmi):
    for category, upper_bound, color in bmi_categories_with_colors:
        if bmi <= upper_bound:
            return category, color

def plot_bmi_chart():
    names = []
    bmis = []
    colors = []
    with open("bmi_data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            names.append(row[0])
            bmis.append(float(row[3]))
            bmi_color = find_bmi_category_and_color(float(row[3]))
            color = bmi_color[1]
            colors.append(color)

    plt.figure(figsize=(4, 3))
    plt.bar(names, bmis, color=colors)
    # plt.xlabel("Name")
    plt.ylabel("BMI")
    plt.title("BMI Data")
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig("bmi_chart.png")
    plt.close()

    plot_image = Image.open("bmi_chart.png")
    plot_output_img = ImageTk.PhotoImage(plot_image)

    global plot_output
    plot_output = tkinter.Label(frame, image=plot_output_img)
    plot_output.image = plot_output_img
    plot_output.grid(row=4, column=0, padx=10, pady=10)

window = tkinter.Tk()
window.title("Adult BMI calculator")
frame = tkinter.Frame(window)
frame.grid()

#Entry data frame
entry_frame = tkinter.LabelFrame(frame, borderwidth=0, highlightthickness=0)
entry_frame.grid(row=0, column=0, sticky="news")

name_label = tkinter.Label(entry_frame, text="Your name: ")
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
name_txt = tkinter.Entry(entry_frame)
name_txt.grid(row=0, column=1, padx=10, pady=10)

height_label = tkinter.Label(entry_frame, text="Your height, (cm): ")
height_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
height_txt = tkinter.Entry(entry_frame)
height_txt.grid(row=1, column=1, padx=10, pady=10, sticky="e")

weight_label = tkinter.Label(entry_frame, text="Your weight, (kg): ")
weight_label.grid(row=2, column=0, padx=10, pady=10)
weight_txt = tkinter.Entry(entry_frame)
weight_txt.grid(row=2, column=1, padx=10, pady=10)

#Calculation button
calculate_button = tkinter.Button(entry_frame, text="Calculate BMI", command=calculate)
calculate_button.grid(row=3, column=1, padx=10, pady=10, sticky="news")

#BMI range frame
range_frame = tkinter.LabelFrame(frame, borderwidth=0, highlightthickness=0)
range_frame.grid(row=2, column=0, sticky="news")

label1 = tkinter.Label(range_frame, text="Your BMI", bg=Green, fg="white")
label1.grid(row=0, column=0, padx=10, pady=10, sticky="news")

img_bmi_range = tkinter.PhotoImage(file="BMIrange.png")
img_label = tkinter.Label(range_frame, image=img_bmi_range)
img_label.grid(row=1, column=0, padx=10, pady=10)

#Plotting the chart button
plot_button = tkinter.Button(frame, text="Plot BMI Chart", command=plot_bmi_chart)
plot_button.grid(row=3, column=0, padx=10, pady=10, sticky="news")


window.mainloop()

