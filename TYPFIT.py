import tkinter
from tkinter import *
import time

# --- Color Palette ---
BG_DARK = "#000000"
BG_MEDIUM = "#404040"
BG_LIGHT = "#727272"
FG_MAIN = "#ffffff"
FG_SECONDARY = "#ababab"

root = Tk()
root.title("TYPFIT")
root.geometry("600x600")
root.configure(bg=BG_DARK)  # Main background

# Main canvas setup
main_canvas = Canvas(root, bg=BG_DARK, highlightthickness=0)
scrollbar = Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = Frame(main_canvas, bg=BG_DARK)

def on_canvas_configure(event):
    main_canvas.itemconfig("frame", width=event.width)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="frame")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
main_canvas.bind("<Configure>", on_canvas_configure)

def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ----------------------------------------------------

def main():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    title()
    do_nothing()
    exit_and_profile_buttons()
    start_test_button()
    info_button()

def title():
    Label(scrollable_frame, text='TYPFIT',
          font=("Helvetica Neue", 26, "bold"),
          bg=BG_DARK, fg=FG_MAIN).pack(pady=(20, 10))

def do_nothing():
    pass

def cycle():
    try:
        with open("s.txt", "r", encoding="utf-8") as story:
            paragraphs = story.read().split("\n\n")
    except Exception as e:
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        Label(scrollable_frame, text=f"Error loading s.txt: {e}", font=("Helvetica Neue", 14),
              bg=BG_DARK, fg=FG_MAIN).pack()
        return

    state = {"index": 0, "T": [], "A": [], "C": [], "L": [], "stopped": False}

    def show_paragraph():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        if state["index"] >= len(paragraphs) or state["stopped"]:
            summary = ""
            if state["T"]:
                total_time = sum(state["T"])
                avg_acc = sum(state["A"]) / len(state["A"])
                summary = f"\n⏱️ Total typing time: {total_time:.2f} seconds\n🎯 Average Accuracy: {avg_acc:.2f}%"
            Label(scrollable_frame, text="Test complete!" + summary,
                  font=("Helvetica Neue", 14), bg=BG_DARK, fg=FG_MAIN).pack(pady=10)
            Button(scrollable_frame, text="Return to Home", command=main,
                   bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
                   font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(pady=10)
            return

        paragraph = paragraphs[state["index"]]
        Label(scrollable_frame, text="\n🔹 Type the following paragraph:\n" + paragraph,
              font=("Helvetica Neue", 10), justify="left", anchor="w",
              bg=BG_DARK, fg=FG_MAIN, wraplength=500).pack(pady=10)

        Button(scrollable_frame, text="Start Typing", command=lambda: time_start(paragraph),
               bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
               font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(pady=4)

    def time_start(paragraph):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        Label(scrollable_frame, text="\n⚡ Time starts now! Type the paragraph below and hit ENTER when done.\n",
              font=("Helvetica Neue", 10), justify="left", anchor="w",
              bg=BG_DARK, fg=FG_MAIN).pack(pady=5)

        Label(scrollable_frame, text=paragraph,
              font=("Helvetica Neue", 11), justify="left", anchor="w",
              wraplength=500, bg=BG_DARK, fg=FG_MAIN).pack()

        text_box = Text(scrollable_frame, height=10, width=60,
                        bg=BG_MEDIUM, fg=FG_MAIN, insertbackground=FG_MAIN,
                        font=("Helvetica Neue", 11), padx=10, pady=6,
                        highlightbackground=BG_LIGHT, highlightthickness=1)
        text_box.pack(pady=10)

        start_time = time.time()

        Button(scrollable_frame, text="Submit",
               command=lambda: get_text(text_box, paragraph, start_time),
               bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
               font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(pady=4)

    def get_text(text_box, paragraph, start_time):
        user_input = text_box.get("1.0", "end-1c")
        end_time = time.time()
        elapsed_time = end_time - start_time

        original_words = paragraph.split()
        typed_words = user_input.split()
        correct = sum(1 for i in range(min(len(original_words), len(typed_words)))
                      if original_words[i] == typed_words[i])
        state["C"].append(correct)
        state["L"].append(len(typed_words))
        accuracy = (correct / len(typed_words)) * 100 if typed_words else 0
        state["A"].append(accuracy)
        state["T"].append(elapsed_time)

        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        Label(scrollable_frame, text=f"\n⏱️ Elapsed time: {elapsed_time:.2f} seconds",
              font=("Helvetica Neue", 11), bg=BG_DARK, fg=FG_MAIN).pack(pady=5)

        Label(scrollable_frame, text=f"🎯 Accuracy: {accuracy:.2f}%",
              font=("Helvetica Neue", 11), bg=BG_DARK, fg=FG_MAIN).pack(pady=5)

        Button(scrollable_frame, text="Next Test", command=next_paragraph,
               bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
               font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(pady=4)

    def next_paragraph():
        state["index"] += 1
        show_paragraph()

    def stop_test():
        state["stopped"] = True
        show_paragraph()

    show_paragraph()

def exit_and_profile_buttons():
    row = Frame(scrollable_frame, bg=BG_DARK)
    row.pack(side="top", fill="x", pady=10)
    Button(row, text="⬅️", command=do_nothing,
           bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
           font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
    Button(row, text="👤", command=do_nothing,
           bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
           font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(side="right", padx=5)

def start_test_button():
    Label(scrollable_frame, text="", font=("Helvetica Neue", 9),
          bg=BG_DARK).pack(fill="x", pady=5)
    Button(scrollable_frame, text="Start Test", command=cycle,
           bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
           font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(pady=10)

def instructions():
    text = (
        "⭕ INSTRUCTIONS:\n"
        "   - Expand your window for better readability.\n"
        "   - Do not press ENTER until you finish typing.\n"
        "   - Once finished, press ENTER to submit.\n"
    )
    Label(scrollable_frame, text=text, justify="left", anchor="w",
          font=("Helvetica Neue", 10), bg=BG_DARK, fg=FG_SECONDARY, wraplength=550).pack(pady=10)
    Button(scrollable_frame, text="OK", command=do_nothing,
           bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
           font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(pady=5)

def info_button():
    Button(scrollable_frame, text="ℹ️", command=instructions,
           bg=BG_MEDIUM, fg=FG_MAIN, activebackground=BG_LIGHT,
           font=("Helvetica Neue", 11), relief="flat", padx=10, pady=5).pack(pady=10)

if __name__ == "__main__":
    main()
    root.mainloop()

