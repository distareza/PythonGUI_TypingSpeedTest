import tkinter
import time
import threading
import tkinter.messagebox
import englishWord

window = tkinter.Tk()
window.title("Python GUI Typing Contest")
window.config(width=640, height=480, padx=50, pady=50)

labelHeader = tkinter.Label(text="Typing Test Contest", font=("Arial", 24, "bold italic"))
textWords = tkinter.Label(height=8, font=("Courier", 14), wraplength=400, justify="left")
labelStatus = tkinter.Label(font=("Courier", 14))
labelResult = tkinter.Label(font=("Arial", 14))
frameInput = tkinter.Frame(borderwidth=20)
inputText = tkinter.Entry(frameInput, width=30, justify="center", font=("Courier", 14))
buttonReset = tkinter.Button(text="Restart", font=("Times New Roman", 16), padx=20, pady=20)

labelHeader.pack()
textWords.pack()
frameInput.pack()
inputText.pack()
labelStatus.pack()
labelResult.pack()
buttonReset.pack()

words = []
correct_typing_counter = 0
wrong_typing_counter = 0
score = 0
start_counter = False

def initData():
    global words, correct_typing_counter, wrong_typing_counter, start_counter, score

    inputText.delete(0, len(inputText.get()))
    buttonReset.config(state="disabled")
    inputText.config(state="disabled")
    labelHeader.config(text="Retriving word data")

    correct_typing_counter = 0
    wrong_typing_counter = 0
    score = 0
    start_counter = False
    try:
        words = englishWord.readLocalData()
        updateLabel()
    except Exception as e:
        print(e)
    finally:
        labelHeader.config(text="Typing Test")
        inputText.config(state="normal")

def updateLabel():
    word_to_type = []
    for i in range(20):
        word_to_type.append(words[i])
    textWords.config(text=' '.join(word_to_type))
    labelStatus.config(text=f"Correct Word Count: {correct_typing_counter}, score: {score}")

def key_press(event):
    try:
        global words, correct_typing_counter, wrong_typing_counter, start_counter, score
        if not start_counter:
            start_counter = True
            threading.Thread(target=startCounter).start()

        update_score = 0

        # Press spacebar or Enter
        if event.keycode == 32 or event.keycode == 13:
            text = inputText.get().strip()

            # empty string will be ignored
            if not bool(text):
                return

            print(text)
            correct_word = False
            for i in range(20):
                if text == words[i]:
                    words.pop(i)
                    correct_word = True
                    break

            if correct_word:
                update_score = 10
                correct_typing_counter += 1
            else:
                update_score = -5
                wrong_typing_counter += 1

            score += update_score
            updateLabel()
            inputText.delete(0, len(inputText.get()))

        # Press backspace
        elif event.keycode == 8:
            if bool(inputText.get().strip()):
                update_score = -1
                score += update_score
                updateLabel()


    except Exception as ex:
        print(ex)

def startCounter():
    start_time = time.perf_counter()
    while True:
        delta_time = time.perf_counter() - start_time
        labelResult.config(text=f"Time : {60-int(delta_time):02d} ")
        time.sleep(0.5)
        if delta_time > 60:
           break

    message = f"Correct Word Count Type Per Minutes is {correct_typing_counter}\n" \
              f"Wrong Word Count : {wrong_typing_counter}\n" \
              f"Score : {score}"
    labelResult.config(text=message)
    inputText.delete(0, len(inputText.get()))
    inputText.config(state="disabled")
    tkinter.messagebox.showinfo(title="Your Typing Speed Result", message=message)
    buttonReset.config(state="normal")

# https://python-course.eu/tkinter/events-and-binds-in-tkinter.php
# https://www.pythontutorial.net/tkinter/tkinter-event-binding/
inputText.bind('<Key>', key_press)

buttonReset.config(command=initData)

thread_init = threading.Thread(target=initData)
thread_init.start()

if __name__ == '__main__':
    inputText.focus()
    window.mainloop()


