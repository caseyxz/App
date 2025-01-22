import customtkinter as ctk 
from tkinter import filedialog
from PIL import Image
from logic import load_dataset, run_algorithms_incrementally
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Global variables
X, y = None, None  # Przechowywane dane po załadowaniu
switches = []  # Lista przełączników dla algorytmów

# Dataset list
DATASETS = [
    'Adiac','ArrowHead','Beef','BeetleFly','BirdChicken','Car','CBF','ChlorineConcentration','Coffee','Computers',
    'CricketX','CricketY','CricketZ','DiatomSizeReduction','DistalPhalanxOutlineCorrect','DistalPhalanxOutlineAgeGroup',
    'DistalPhalanxTW','Earthquakes','ECG200','ECG5000','ECGFiveDays','ElectricDevices','FaceAll','FaceFour','FacesUCR',
    'FiftyWords','Fish','FordA','FordB','GunPoint','Ham','HandOutlines','Haptics','Herring','InlineSkate','InsectWingbeatSound',
    'ItalyPowerDemand','LargeKitchenAppliances','Lightning2','Lightning7','Mallat','Meat','MedicalImages',
    'MiddlePhalanxOutlineCorrect','MiddlePhalanxOutlineAgeGroup','MiddlePhalanxTW','MoteStrain',
    'OliveOil','OSULeaf','PhalangesOutlinesCorrect','Phoneme','Plane','ProximalPhalanxOutlineCorrect',
    'ProximalPhalanxOutlineAgeGroup','ProximalPhalanxTW','RefrigerationDevices','ScreenType','ShapeletSim','ShapesAll',
    'SmallKitchenAppliances','SonyAIBORobotSurface1','SonyAIBORobotSurface2','Strawberry','SwedishLeaf',
    'Symbols','SyntheticControl','ToeSegmentation1','ToeSegmentation2','Trace','TwoLeadECG','TwoPatterns','UWaveGestureLibraryX',
    'UWaveGestureLibraryY','UWaveGestureLibraryZ','UWaveGestureLibraryAll','Wafer','Wine','WordSynonyms','Worms','WormsTwoClass','Yoga'
]

# Functions

def change_mode(choice):
    ctk.set_appearance_mode(choice)

def load_file():
    global X, y
    dataset_name = dataset_dropdown.get()
    
    if dataset_name:
        X, y, message = load_dataset(dataset_name)
        file_label.configure(text=message)
        print(message)

def submit_process():
    if X is None or y is None:
        result_label.configure(text="No dataset loaded.")
        return

    selected_algorithms = [switch.cget("text") for switch in switches if switch.get()]
    if not selected_algorithms:
        result_label.configure(text="No algorithms selected.")
        return

    # Automatic transition to "Results" tab
    tabview.set("Result")

    # Threading
    def run_algorithms_in_thread():
        results = {}
        for algo_name, result in run_algorithms_incrementally(X, y, selected_algorithms):
            results[algo_name] = result
            display_results(results)
    threading.Thread(target=run_algorithms_in_thread, daemon=True).start()

def display_results(results):
    """
    Wyświetla wyniki w zakładce Result i rysuje wykres obok wyników.
    """
    # Czyszczenie widżetów w obu kolumnach
    for widget in result_text_frame.winfo_children():
        widget.destroy()
    for widget in result_chart_frame.winfo_children():
        widget.destroy()

    # Wyświetlanie wyników tekstowych w lewej kolumnie
    for algo, result in results.items():
        label = ctk.CTkLabel(master=result_text_frame, text=f"{algo}: {result}", font=("Helvetica", 14))
        label.pack(pady=5, anchor="w")
        print(f"{algo}: {result}")  # Debugowanie w konsoli

    # Przygotowanie danych do wykresu
    algorithms = list(results.keys())
    accuracies = [
        float(result.split(":")[1]) if "Accuracy" in result else 0
        for result in results.values()
    ]

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(algorithms, accuracies, color="skyblue")
    ax.set_title("Porównanie dokładności algorytmów")
    ax.set_xlabel("Algorytmy")
    ax.set_ylabel("Dokładność")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=45)

    # Osadzanie wykresu w prawej kolumnie
    canvas = FigureCanvasTkAgg(fig, master=result_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)


# Main Window
app = ctk.CTk()
app.geometry("800x600")
app.title("Demo")

# Main Grid Configuration
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=3)

# Picture
image_path = "pic.png"  
image = ctk.CTkImage(Image.open(image_path), size=(150, 600))  
label_image = ctk.CTkLabel(app, image=image, text="")
label_image.grid(row=0, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")  

# Gretting text
label_tabs = ctk.CTkLabel(app, text="Algorithm Testing Tool for Time Series Classification", font=("Helvetica", 24),anchor="w")
label_tabs.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")  

# Tabs 
tabview = ctk.CTkTabview(master=app, width=630, height=560)
tabview.grid(row=1, column=1, padx=5, pady=20, sticky="nsew")
tabview.add("Main")
tabview.add("Result")
tabview.add("Options")
tabview.tab("Main").grid_rowconfigure(0, weight=1)
tabview.tab("Main").grid_columnconfigure(0, weight=1)
tabview.tab("Main").grid_columnconfigure(1, weight=1)

# Tab1 left column
frame_left1 = ctk.CTkFrame(tabview.tab("Main"))
frame_left1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# File Load Label
file_label = ctk.CTkLabel(master=frame_left1, text="No file loaded.", font=("Helvetica", 16))
file_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Dataset Dropdown
dataset_dropdown = ctk.CTkOptionMenu(master=frame_left1, values=DATASETS)
dataset_dropdown.grid(row=1, column=0, pady=10)

# File Load Button
file_button = ctk.CTkButton(master=frame_left1, text="Load", command=load_file)
file_button.grid(row=2, column=0, padx=10, pady=10)

# TextBox Entry
entry = ctk.CTkEntry(master=frame_left1, 
                    placeholder_text="Your algorithm...",  
                    width=250,  
                    height=100) 
entry.grid(row=5, column=0, pady=10, padx=10)

# Load Algorithm Button 
load_algorithm = ctk.CTkButton(master=frame_left1, text="Load")
load_algorithm.grid(row=6, column=0, pady=10)

# Tab1 right column
frame_right1 = ctk.CTkFrame(tabview.tab("Main"))
frame_right1.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Switch Menu
label_title = ctk.CTkLabel(master=frame_right1, text="Choose algorithms", font=("Helvetica", 15))
label_title.grid(row=0, column=0, pady=11)

scrollable_frame = ctk.CTkScrollableFrame(master=frame_right1, width=150, height=150)
scrollable_frame.grid(row=2, column=0, padx=10, pady=11, sticky="n")

from logic import ALGORITHMS
for algo in ALGORITHMS.keys():
    switch = ctk.CTkSwitch(master=scrollable_frame, text=algo)
    switch.grid(pady=5)  # Zmiana z `pack()` na `grid()`
    switches.append(switch)

# Submit And Start The Process Button
submit = ctk.CTkButton(master=frame_right1, text="Submit", command=submit_process)
submit.grid(row=5, column=0, pady=79)

# Results Tab
result_frame = ctk.CTkFrame(tabview.tab("Result"))
result_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
result_frame.grid_columnconfigure(0, weight=1)
result_frame.grid_columnconfigure(1, weight=2)

# Progress Bar
progress_bar = ctk.CTkProgressBar(master=result_frame, orientation="horizontal", mode="indeterminate")
progress_bar.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Teksty wyników w lewej kolumnie
result_text_frame = ctk.CTkFrame(master=result_frame)
result_text_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Wykres w prawej kolumnie
result_chart_frame = ctk.CTkFrame(master=result_frame)
result_chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


# Options Tab
frame_left3 = ctk.CTkFrame(tabview.tab("Options"))
frame_left3.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

frame_right3 = ctk.CTkFrame(tabview.tab("Options"))
frame_right3.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Appearance Mode Dropdown Menu
appearance_menu = ctk.CTkOptionMenu(
    master = frame_left3,
    values=["Dark", "Light", "System"],  
    command=change_mode  
)
appearance_menu.grid(row=0, column=0, pady=10)  
appearance_menu.set("Dark") 

app.mainloop()

