import tkinter
import time
import threading
import tkinter.messagebox
import englishWord

window = tkinter.Tk()
window.title("Python GUI Typing Contest")
window.minsize(width=640, height=480)
window.config(padx=50, pady=50)

labelHeader = tkinter.Label(text="Typing Test Contest", font=("Arial", 24, "bold italic"))
labelWords = tkinter.Label()
labelStatus = tkinter.Label()
labelResult = tkinter.Label()
input = tkinter.Entry(width=30)
buttonReset = tkinter.Button(text="Restart")

labelHeader.pack()
labelWords.pack()
input.pack()
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

    input.delete(0, len(input.get()))
    buttonReset.config(state="disabled")
    input.config(state="disabled")
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
        input.config(state="normal")

def updateLabel():
    word_to_type = []
    for i in range(20):
        word_to_type.append(words[i])
    labelWords.config(text=' '.join(word_to_type))
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
            text = input.get().strip()
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
                wrong_typing_counter -= 1

            score += update_score
            updateLabel()
            input.delete(0, len(input.get()))

        # Press backspace
        elif event.keycode == 8:
            if bool(input.get().strip()):
                update_score = -1
                score += update_score
                updateLabel()


    except Exception as ex:
        print(ex)

def startCounter():
    start_time = time.perf_counter()
    while True:
        delta_time = time.perf_counter() - start_time
        labelResult.config(text=f"Time : {int(delta_time)} ")
        time.sleep(0.5)
        if delta_time > 60:
           break

    message = f"Correct Word Count Type Per Minutes is {correct_typing_counter}\nScore : {score}"
    labelResult.config(text=message)
    tkinter.messagebox.showinfo(title="Your Typing Speed Result", message=message)
    input.config(state="disabled")
    buttonReset.config(state="normal")

# https://python-course.eu/tkinter/events-and-binds-in-tkinter.php
# https://www.pythontutorial.net/tkinter/tkinter-event-binding/
input.bind('<Key>', key_press)

buttonReset.config(command=initData)

thread_init = threading.Thread(target=initData)
thread_init.start()

if __name__ == '__main__':
    input.focus()
    window.mainloop()


