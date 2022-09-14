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

labelHeader.pack()
labelWords.pack()
input.pack()
labelStatus.pack()
labelResult.pack()

words = []
typing_counter = 0
def initData():
    global words, typing_counter
    input.config(state="disabled")
    labelHeader.config(text="Retriving word data")
    typing_counter = 0
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
    labelStatus.config(text=f"Correct Word Count : {typing_counter}")

start_counter = False
def key_press(event):
    try:
        global words, typing_counter, start_counter
        if not start_counter:
            start_counter = True
            threading.Thread(target=startCounter).start()

        # Press spacebar or Enter
        if event.keycode == 32 or event.keycode == 13:
            text = input.get().strip()
            print(text)
            for i in range(20):
                if text == words[i]:
                    words.pop(i)
                    typing_counter += 1
                    updateLabel()
                    break

            input.delete(0, len(input.get()))
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
    labelResult.config(text=f"Correct Word Count Type Per Minutes is {typing_counter}")

# https://python-course.eu/tkinter/events-and-binds-in-tkinter.php
# https://www.pythontutorial.net/tkinter/tkinter-event-binding/
input.bind('<Key>', key_press)

thread_init = threading.Thread(target=initData)
thread_init.start()

if __name__ == '__main__':
    input.focus()
    window.mainloop()


