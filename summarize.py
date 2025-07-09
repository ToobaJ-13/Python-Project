import tkinter as tk
from tkinter import *
import tkinter.messagebox as mbox
from PIL import Image, ImageTk
import nltk
from PIL.SpiderImagePlugin import iforms
from nltk.corpus import stopwords, framenet, words
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure necessary NLTK data is downloded
nltk.download('punkt')
nltk.download('stopwords')

# Main starting window
def main_window():
    frame = Tk()
    frame.title('Text Summarizer')
    frame.geometry('1000x700')

    #Add an image (ensure you have an appropriate image at the given path)
    path = "Images/front.jpg"  #update this path to an existing image on your system
    try:
        img1 = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(frame, image=img1)
        panel.place(x=110, y=120)
    except FileNotFoundError:
        print("Image not found. Ensure the image path is correct.")

    #Title label
    Label(frame, text='Text Summarizer', font=("Times New Roman", 55,), fg="black").place(x=140, y=10)

    def start_fun():
        frame.destroy()
        summarizer_window()

    # Start Button
    Button(frame, text='Start', command=start_fun, font=("Times New Roman", 25), bg="dark green", fg="white", borderwidth=1,
           relief="raised").place(x=150, y=600)

    # End function
    def exit_fun():
        if mbox.askokcancel("Exit", "Do you want to exit?"):
            frame.destroy()

    # Exit Button
    Button(frame, text='Exit', command=exit_fun, font=("Times New Roman", 25), bg="dark blue", fg="white", borderwidth=1,
           relief="raised").place(x=740, y=600)

    # Protocol for close button
    frame.protocol("WM_DELETE_WINDOW",exit_fun)
    frame.mainloop()


# Summarizer window
def summarizer_window():
    window = Tk()
    window.title("Text Summarizer")
    window.geometry("1000x700")

    def summarize_text():
        text = text_enter.get("1.0", "end-1c")
        if not text.strip():
            mbox.showerror("Error", "Please enter text to summarize!")
            return

        stop_words = set(stopwords.words("english"))
        words = [word for word in word_tokenize(text) if word.isalnum()]

        # Frequency table
        freq_table = {}
        for word in words:
            word = word.lower()
            if word not in stop_words:
                freq_table[word] = freq_table.get(word, 0) + 1

        # Sentence scoring
        sentences = sent_tokenize(text)
        sentence_value = {}
        for sentence in sentences:
            for word, freq in freq_table.items():
                if word in sentence.lower():
                    sentence_value[sentence] = sentence_value.get(sentence, 0) + freq

        # Average score
        if sentence_value:
            average = sum(sentence_value.values()) / len(sentence_value)
        else:
            average = 0

        # Generate summary
        summary = ' '.join([sentence for sentence in sentences if sentence_value.get(sentence, 0) > 1.2 * average])

        if not summary.strip():
            summary = "No summary could be generated. Please provide a more detailed input."

        display_summary_window(text, summary)

    def clear_text():
        text_enter.delete("1.0", END)

    def exit_fun():
        if mbox.askokcancel("Exit", "Do you want to exit?"):
            window.destroy()

    # Title label
    Label(window, text="Text Summarizer", font=("Times New Roman", 55), fg="black").place(x=140, y= 10)
    Label(window, text="Enter Any Paragraph/Text and Summarize it.......", font=("Times New Roman", 30), fg="teal").place(x=100,
                                                                                                                          y=100)

    #Text input area
    text_enter = Text(window, height=20, width=85, font=("Times New Roman", 15), bg="white",fg="black", borderwidth=3,
                      relief="solid")
    text_enter.place(x=80, y=150)

    #Buttons
    Button(window, text="Summarize", command=summarize_text, font=("Times New Roman", 25), bg="dark green", fg="white",
           borderwidth=3, relief="raised").place(x=150, y=600)
    Button(window, text="Clear", command=clear_text, font=("Times New Roman", 25), bg="black", fg="white",
           borderwidth=3, relief="raised").place(x=480, y=600)
    Button(window, text="Exit", command=exit_fun, font=("Times New Roman", 25), bg="grey", fg="white",
           borderwidth=3, relief="raised").place(x=740, y=600)

    window.protocol("WM_DELETE_WINDOW", exit_fun)
    window.mainloop()

# Display summary in a new window
def display_summary_window(original_text, summary):
    window = Tk()
    window.title("Text Summarizer")
    window.geometry("1000x700")


    #Title label
    Label(window, text="Text Summarizer", font=("Times New Roman", 55), fg="black").place(x=140, y= 10)
    Label(window, text="Text After Summarizing...", font=("Time New Roman", 30), fg="black").place(x=250, y=100)

    # Display summarized text
    text_display = Text(window, height=16, width=79, font=("Time New Roman",15), bg="white", fg="black",borderwidth=3,
                        relief="solid")
    text_display.place(x=80, y=150)
    text_display.insert(END, summary)

    # Length display
    Label(window, text=f"Original Text Length:{len(original_text)}", font=("Times New Roman",30), fg="black").place(x=185,
                                                                                                                   y=550)
    Label(window, text=f"Summarized Text Length:{len(summary)}", font=("Times New Roman", 30), fg="black").place(x=150,y=610)

    # Convert summary to bullet points
    def convert_to_bullets():
        bullet_points = "\n".join([f".{line.strip()}" for line in summary.split(". ")if line.strip()])
        text_display.delete("1.0", END)
        text_display.insert(END, bullet_points)

    # Close button
    def close_fun():
        window.destroy()

    # Add buttons
    Button(window, text="Close", command=close_fun, font=("Times New Roman",25), bg="orange", fg="blue", borderwidth=3,
           relief="raised").place(x=350, y=670)
    Button(window, text="Bullet Points", command= convert_to_bullets, font=("Times New Roman", 25), bg="light green", fg="blue",
           borderwidth=3, relief="raised").place(x=600, y=670)
    window.mainloop()

# Run the main window
main_window()