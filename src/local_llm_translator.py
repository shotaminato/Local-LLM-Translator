import customtkinter, threading, time, os
from llama_cpp import Llama

LLAMA_MODEL_PATH = os.path.dirname(__file__) + r"/../Llama-3-ELYZA-JP-8B-GGUF/Llama-3-ELYZA-JP-8B-q4_k_m.gguf"

FONT_TYPE = "meiryo"

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode    ("dark")  # Modes : system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.fonts = (FONT_TYPE, 15)
        self.geometry("800x800")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("MINATO Translator")

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Three rows. (Height = 10:1:10) 
        self.frame.grid_rowconfigure(0, weight=10)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=10)

        # Four columns.
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        # Input Text box.
        self.in_textbox = customtkinter.CTkTextbox(master=self.frame, font=self.fonts, wrap="word")
        self.in_textbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        self.in_textbox.bind("<Control-Key-Return>", self.button_function)

        # Start button.
        self.button = customtkinter.CTkButton(master=self.frame, text="翻訳開始", command=self.button_function, font=self.fonts)
        self.button.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='nsew')

        # Radio Button.
        self.radiobutton_1 = customtkinter.CTkRadioButton(master=self.frame, text="Markdown Mode")
        self.radiobutton_1.grid(row=1, column=2, padx=10, pady=0, sticky='nsew')
        self.radiobutton_2 = customtkinter.CTkRadioButton(master=self.frame, text="Asciidoc Mode")
        self.radiobutton_2.grid(row=1, column=3, padx=10, pady=0, sticky='nsew')

        # Result Text Box.
        self.out_textlabel = customtkinter.CTkTextbox(master=self.frame, font=self.fonts, wrap="word")
        self.out_textlabel.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        self.out_textlabel.insert(0.0, "Results here.")

        self.llm = Llama(
            model_path= LLAMA_MODEL_PATH,
            chat_format="llama-3",
            n_ctx=1024,
        )



    def button_function(self, key = ""):
        self.button.configure(state="disabled")
        self.loading_index :int = 0
        waiting_thread   = threading.Thread(target=self.update_display)
        translate_thread = threading.Thread(target=self.translate, args=[str(self.in_textbox.get(0.0, "end"))])
        waiting_thread.start()
        translate_thread.start()
        
        
    
    def translate(self, input_sentence :str):

        self.response = self.llm.create_chat_completion(
            messages=[
                # {
                #     "role": "system",
                #     "content": "You are responsible for translation. Please translate the input Japanese into English and output the translation. Your response should be the result of the translation only, and should not contain any extra text. Please make sure to translate all the input sentences accurately.",
                # },
                {
                    "role": "user",
                    "content": "Please translate the following Japanese into English and output. Your response should be the result of the translation only, and should not contain any extra text. Please make sure to translate all the input sentences accurately. Please translate accurately each sentence. Make sure that the number of sentences in the input equals the number of sentences in the output. The Japanese sentences to be translated are as follows:\n" + input_sentence,
                },
            ],
            max_tokens=4048,
        )

        print(self.response["choices"][0]["message"]["content"])

        self.button.configure(state="normal")

        self.out_textlabel.delete(0.0, "end")
        self.out_textlabel.insert(0.0, self.response["choices"][0]["message"]["content"])
        print()
        print(self.response["choices"][0]["message"]["content"])

    def update_display(self):
        self.loading_index = 0
        while True:
            if self.button.cget("state") == "disabled":
                loading_text = "." * ((self.loading_index % 3) + 1)
                self.loading_index += 1
                self.out_textlabel.delete(0.0, "end")
                self.out_textlabel.insert(0.0, f"翻訳中{loading_text}")
                time.sleep(0.5)
            else:
                break

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()