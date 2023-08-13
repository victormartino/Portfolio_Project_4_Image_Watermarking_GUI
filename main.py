from tkinter import *
from PIL import Image, ImageTk, ImageFont, ImageDraw
from tkinter import filedialog, messagebox

MAIN_WHITE = '#F7F7F7'
BUTTON_WIDTH = 18

uploaded_image = None
final_image = None


def upload_image(window, label):
    global uploaded_image
    f_types = [('Image files', '*.jpg *.jpeg *.png *.gif *.bmp *.ico *.tiff *.webp')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    uploaded_image = img.copy()
    img.thumbnail((500, 500))
    display_image(window, label, ImageTk.PhotoImage(img))
    entry_label.grid(column=0, columnspan=2, row=2, sticky='w')
    entry_text.grid(column=2, columnspan=2, row=2, sticky='e')
    entry_text.focus()
    txt_size_label.grid(column=0, columnspan=2, row=3, sticky='w')
    text_size.grid(column=2, columnspan=2, row=3, sticky='e')
    watermark_button.grid(column=0, row=4, columnspan=2, sticky='w')
    export_button.grid(column=3, row=4, columnspan=2, sticky='e')
    export_button.config(state=DISABLED)


def add_watermark(image, wm_text, txt_size):
    global final_image
    if image is None:
        return None
    manipulated_img = image.copy()
    manipulated_img = manipulated_img.convert("RGBA")
    width, height = manipulated_img.size

    # Create an empty image with the exact same dimensions as the uploaded image, with an alpha of 0,
    # meaning it's fully transparent

    txt = Image.new("RGBA", manipulated_img.size, (255, 255, 255, 0))
    painter = ImageDraw.Draw(txt)
    font_type = ImageFont.truetype("arial.ttf", txt_size)
    # Get the measurement of the textbox so that you can consider the offset when drawing the text
    _, _, text_width, text_height = painter.textbbox((0, 0), text=wm_text, font=font_type)
    # Use the measurements to position the text bang in the center
    x_position = (width - text_width) // 2
    y_position = (height - text_height) // 2
    text_color = (255, 255, 255, 128)
    painter.text((x_position, y_position), wm_text, fill=text_color, font=font_type)
    manipulated_img = Image.alpha_composite(manipulated_img, txt)
    final_image = manipulated_img.copy()
    manipulated_img.thumbnail((500, 500))
    display_image(window, e1, ImageTk.PhotoImage(manipulated_img))
    export_button.config(state=NORMAL)


def display_image(window, label, image):
    label.image = image
    label['image'] = image
    label.config(borderwidth=0)
    label.grid(pady=20, column=0, columnspan=4, row=6)
    window.minsize(800, 600)


def export_image(image):
    f_types = [
        ('PNG files', '*.png'),
        ('JPEG files', '*.jpg'), ]
    file_path = filedialog.asksaveasfilename(filetypes=f_types, defaultextension=".png",
                                             initialfile="exported_image.png")
    if file_path:
        image.save(file_path)
        messagebox.showinfo(title="Export Successful", message="Image successfully exported")


# Create the main window
window = Tk()
window.title('Own It! - Image Watermarking')
window.config(padx=20, pady=20, bg='black')

my_label = Label(text='Own It!', font=("Arial", 24, "bold"), bg='black', fg=MAIN_WHITE, pady=10)
my_label.grid(column=0, row=0, columnspan=4)

upload_button = Button(text='Upload image', command=lambda: upload_image(window, e1), bg='black', fg=MAIN_WHITE,
                       highlightbackground=MAIN_WHITE,
                       font=("Arial", 9, "bold"),
                       highlightthickness=3, borderwidth=3, width=BUTTON_WIDTH)
upload_button.grid(column=0, row=1, columnspan=4)

# Create and hide entry label and entry text
entry_label = Label(text='Enter your watermark text:', font=("Arial", 10, 'bold'), bg='black', fg=MAIN_WHITE,
                    anchor='w',
                    pady=10)
entry_label.grid_remove()

entry_text = Entry(bg='black', fg=MAIN_WHITE, insertbackground='white')
entry_text.grid_remove()

watermark_button = Button(text='Add watermark',
                          command=lambda: add_watermark(uploaded_image, entry_text.get(), int(text_size.get())),
                          bg='black', fg=MAIN_WHITE, highlightbackground=MAIN_WHITE, borderwidth=3, width=BUTTON_WIDTH,
                          font=("Arial", 9, "bold"),
                          highlightthickness=3)
watermark_button.grid_remove()

export_button = Button(text='Export Image', command=lambda: export_image(final_image), bg='black', fg=MAIN_WHITE,
                       highlightbackground=MAIN_WHITE, borderwidth=3, width=BUTTON_WIDTH,
                       font=("Arial", 9, "bold"),
                       highlightthickness=3)
export_button.grid_remove()

# Create the label to display the image
e1 = Label(window)

txt_size_label = Label(text="Enter font size:", font=("Arial", 10, 'bold'), bg='black', fg=MAIN_WHITE, anchor='w',
                       pady=10)
txt_size_label.grid_remove()

text_size = Entry(bg='black', fg=MAIN_WHITE, insertbackground='white')
text_size.grid_remove()

# This makes columns resize as the window resizes, so they take up all available space
for col in range(4):
    window.grid_columnconfigure(col, weight=1)

window.mainloop()
