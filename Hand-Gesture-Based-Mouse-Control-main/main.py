# Import the necessary modules
import tkinter as tk
import webbrowser
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import mouse_and_drawing as md


# Create the Customtkinter app instance
app = ctk.CTk()
app.bind('<Escape>', lambda e: app.quit())

cap = cv2.VideoCapture(0)

width, height =  640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


label_widget = tk.Label(app)
label_widget.pack()

# Set the title of the window
app.title("WaveClick")

# Set the size of the window
app.geometry("1000x500")

def button_click():
    # Capture the video frame by frame
    _, frame = cap.read()

    frame = md.open_camera(frame)

    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)

    # Convert captured image to photoimage
    photo_image = ImageTk.PhotoImage(image=captured_image)

    # Displaying photoimage in the label
    label_widget.photo_image = photo_image

    # Configure image in the label
    label_widget.configure(image=photo_image)

    # Maximize the application window
    # label_widget.master.wm_state('zoomed')

    # Repeat the same process after every 10 seconds
    label_widget.after(10, button_click)


# Create the container frame
container = tk.Frame(app)
container.pack(fill=tk.BOTH, expand=True)

# Create the left column frame
left_frame = tk.Frame(container, bg="#222831", width=300)
left_frame.pack(side="left", fill="y")

# Create the right column frame
right_frame = tk.Frame(container, bg="#2D4059", padx=10, pady=10)
right_frame.pack(side="left", fill="both", expand=True)



# Define a function to show the home page and hide other pages
def show_home_page():
    # Clear the current contents of the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()
     # Create a label widget for the heading
    heading_label = tk.Label(right_frame, text="Welcome to Waveclick", font=("TkDefaultFont", 18), fg="white", bg="#2D4059", padx=10, pady=10)
    heading_label.pack(side="top", fill="x", padx=10, pady=10, anchor="n")
    heading_label.config(bg="#1E2A3A")

  # Add two paragraphs to the right frame using a Text widget
    text = tk.Text(right_frame, font=("Arial", 12), bg="#2D4059", fg="white", wrap="word", highlightthickness=0, borderwidth=0)
    text.insert(tk.END, "Say goodbye to clunky mouse devices and embrace a more natural and precise way of interacting with your computer. With just a wave of your hand, you can move the cursor, click, scroll, and perform a range of other actions with ease.\n\nOur cutting-edge technology tracks your hand movements with precision and accuracy, making it the perfect solution for gamers, graphic designers, and anyone looking for a more comprehensive and exciting way to interact with their computer.\n\nExperience a new level of control and freedom with Hand Gesture Based Mouse control.")
    text.configure(state="disabled")
    text.pack(side="top", pady=10)

#############################
#Tutorial Page Code
def show_guide_page():
    # Clear the current contents of the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Load the image
    image = Image.open("assets/Tutorial.png")
    # Resize the image to fit the right frame
    image = image.resize((right_frame.winfo_width(), right_frame.winfo_height()), Image.Resampling.LANCZOS)
    # Convert the image to Tkinter-compatible format
    image_tk = ImageTk.PhotoImage(image)

    # Create a label widget for the image
    image_label = tk.Label(right_frame, image=image_tk, bg="#2D4059")
    image_label.pack(side="top", fill="both", expand=True)

    # Keep a reference to the image_tk object to prevent it from being garbage collected
    image_label.image_tk = image_tk

###############################################
#About us page Code
def show_aboutUs_page():
    # Clear the current contents of the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Create a label widget for the heading
    heading_label = tk.Label(right_frame, text="Meet Our Team", font=("TkDefaultFont", 18), fg="white", bg="#2D4059", padx=10, pady=10)
    heading_label.pack(side="top", fill="x", padx=10, pady=10, anchor="n")
    heading_label.config(bg="#1E2A3A")

    # Create a frame for the team members
    team_frame = tk.Frame(right_frame, bg="#2D4059", padx=10, pady=10)
    team_frame.pack(side="top", fill="both", expand=True)

    # Create a list of team members with their name, photo and icons
    team_members = [
    {"name": "Arnav Modanwal", "photo": "assets/Arnav.jpg", "icons": ["assets/gmail.png", "assets/linkedin.png", "assets/github.png"],
     "links": ["mailto:200390107011@saffrony.ac.in", "https://www.linkedin.com/in/arnav-modanwal-b4b111188", "https://github.com/Arnav1145"]},
    {"name": "Hepil Italiya", "photo": "assets/Hepil.jpg", "icons": ["assets/gmail.png", "assets/linkedin.png", "assets/github.png"],
     "links": ["mailto:200390107049@saffrony.ac.in", "https://www.linkedin.com/in/hepil-italiya", "https://github.com/hepil-italiya"]},
    {"name": "Pratik Solanki", "photo": "assets/Pratik.png", "icons": ["assets/gmail.png", "assets/linkedin.png", "assets/github.png"],
     "links": ["mailto:200390107045@saffrony.ac.in", "http://www.linkedin.com/in/pratiksolanki", "https://github.com/Pratik960"]},
    {"name": "Krushi Monpara", "photo": "assets/Krushi.jpg", "icons": ["assets/gmail.png", "assets/linkedin.png", "assets/github.png"],
     "links": ["mailto:200390107037@saffrony.ac.in", "https://www.linkedin.com/in/krushi-monpara-k24112002", "https://github.com/Krushi24112002"]},
]

    # Create a label widget for each team member
    member_labels = []
    for i, member in enumerate(team_members):
        # Load the member's photo
        photo = Image.open(member["photo"])
        # Resize the photo to the desired size
        photo = photo.resize((150, 150), Image.Resampling.LANCZOS)
        # Convert the photo to Tkinter-compatible format
        photo_tk = ImageTk.PhotoImage(photo)

        # Create a frame for the member's photo and name
        member_frame = tk.Frame(team_frame, bg="#2D4059")
        member_frame.grid(row=i//2, column=i%2, padx=10, pady=10)

        # Create a label widget for the member's photo
        photo_label = tk.Label(member_frame, image=photo_tk, bg="#2D4059")
        photo_label.photo = photo_tk  # Save the PhotoImage as an instance variable of the label
        photo_label.pack(side="left", padx=10, pady=10)

        # Create a frame for the member's name and icons
        name_icons_frame = tk.Frame(member_frame, bg="#2D4059")
        name_icons_frame.pack(side="left", padx=10, pady=10)

        # Create a label widget for the member's name
        name_label = tk.Label(name_icons_frame, text=member["name"], font=("TkDefaultFont", 14), fg="white", bg="#2D4059")
        name_label.pack(side="top", padx=10, pady=5)

        # Create a frame for the member's icons
        icons_frame = tk.Frame(name_icons_frame, bg="#2D4059")
        icons_frame.pack(side="top", padx=10, pady=5)

        # Create a label widget for each icon
        for i, icon in enumerate(member["icons"]):
            icon_photo = Image.open(icon)
            icon_photo = icon_photo.resize((30, 30), Image.Resampling.LANCZOS)
            icon_tk = ImageTk.PhotoImage(icon_photo)
            icon_label = tk.Label(icons_frame, image=icon_tk, bg="#2D4059")
            icon_label.photo = icon_tk
            icon_label.pack(side="left", padx=5, pady=5)
            link = member["links"][i]
            icon_label.bind("<Button-1>", lambda e, link=link: webbrowser.open_new_tab(link))



# Define a function to change the background color of the home button on mouse enter
def on_enter(button):
    button.config(bg="#2D4059")

# Define a function to change the background color of the home button on mouse leave
def on_leave(button):
    button.config(bg="#222831")

########################################
# Left frame buttons added from here
########################################

# Load the home icon image
home_icon = Image.open("assets\home.png")
home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
home_icon = ImageTk.PhotoImage(home_icon)

# Create the home button with the home icon image
home_button = tk.Button(left_frame, image=home_icon,text=" Home",compound="left",font=("TkDefaultFont", 16), bg="#222831",fg="white", bd=0, padx=0, pady=0, command=show_home_page)
home_button.pack(side="top", padx=50, pady=50, anchor="w")
home_button.bind("<Enter>", lambda e: on_enter(home_button))
home_button.bind("<Leave>", lambda e: on_leave(home_button))

# Load the guide icon image
guide_icon = Image.open("assets\Setting.png")
guide_icon = guide_icon.resize((30, 30), Image.Resampling.LANCZOS)
guide_icon = ImageTk.PhotoImage(guide_icon)


# Create the guide button with the guide icon image
guide_button = tk.Button(left_frame, image=guide_icon,text=" Tutorial",compound="left",font=("TkDefaultFont", 16), bg="#222831",fg="white", bd=0, padx=0, pady=0, command=show_guide_page)
guide_button.pack(side="top", padx=50, pady=50, anchor="w")
guide_button.bind("<Enter>",lambda e: on_enter(guide_button))
guide_button.bind("<Leave>",lambda e: on_leave(guide_button))

# Load the about us icon image
aboutUs_icon = Image.open("assets\AboutUs.png")
aboutUs_icon = aboutUs_icon.resize((30, 30), Image.Resampling.LANCZOS)
aboutUs_icon = ImageTk.PhotoImage(aboutUs_icon)

# Create the about button with the aboutUs icon image
aboutUs_button = tk.Button(left_frame, image=aboutUs_icon,text=" About Us",compound="left",font=("TkDefaultFont", 16), bg="#222831",fg="white", bd=0, padx=0, pady=0,command=show_aboutUs_page)
aboutUs_button.pack(side="top", padx=50, pady=50, anchor="w")
aboutUs_button.bind("<Enter>",lambda e: on_enter(aboutUs_button))
aboutUs_button.bind("<Leave>",lambda e: on_leave(aboutUs_button))

# Buttons are added
########################################


# Create a label with the header text and pack it into the header frame
header_label = tk.Label(right_frame, text="WaveClick", font=("TkDefaultFont", 16), bg="#2D4059", fg="white")
header_label.pack(fill="x", padx=0, pady=0,ipady=5)

button1 = tk.Button(left_frame, text="Open Camera",command=button_click)
button1.pack()


# Show the header page on startup
header_label.pack(fill="x", padx=0, pady=0, ipady=5)




# Start the mainloop to display the GUI
app.mainloop()
