import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class robot_controller():
    def __init__(self):
        super.__init__()

        self.logged_state = 0


class App(customtkinter.CTk, robot_controller):
    def __init__(self):
        # robot_controller.__init__(self)
        
        super().__init__()

        # robot_controller.__init__(self) 
        self.logged_state = 0       
        # configure window
        self.title("Robot Controller")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Modes", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Manual Mode", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Program Mode",command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Debug Mode", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance :", anchor="w", font=customtkinter.CTkFont(size=16))
        # self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        # self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Robot Status : Ideal")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="red", text="Disconnected",border_width=2, text_color=("gray10", "#DCE4EE"), command=self.connect)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")



        # create slider and progressbar frame
        self.row_for_slide = 1
        self.colum_for_slider = 0
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=0, column=1, columnspan=6, rowspan=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure((1,2,3,4,5,6), weight=1) 
        self.slider_progressbar_frame.grid_rowconfigure(6, weight=1)

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(0, 10), pady=(10, 10), sticky="ew")


        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_1.grid(row=self.row_for_slide , column= 0, rowspan=5, padx=(10, 10), pady=(10, 10),sticky="wn")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_2.grid(row=self.row_for_slide , column= 0, rowspan=5, padx=(80, 40), pady=(10, 10), sticky="wn")

        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=self.row_for_slide , column= 3, rowspan=5, padx=(10, 10), pady=(10, 10))
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=self.row_for_slide , column= 4, rowspan=5, padx=(10, 20), pady=(10, 10))


        print("initi")
        # set default values
        # self.sidebar_button_3.configure(state="disabled", text="Debug Mode")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("110%")

        # self.slider_1.configure(command=self.progressbar_2.set)
        # self.slider_2.configure(command=self.progressbar_3.set)
        # self.progressbar_1.configure(mode="indeterminnate")
        # self.progressbar_1.start()
        # self.textbox.insert("0.0", "CTkTextbox\n\n" + "Hello Robu \n\n" * 20)
        self.seg_button_1.configure(values=["Servo 1", "Servo 2", "Servo 3", "Servo 4", "Servo 5", "Servo 6"])
        self.seg_button_1.set("Servo 1")

        self.entry.configure(state="disabled")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def connect(self):
        print("connect to robot called")
        if self.logged_state == 0:
            self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="green", text="Connected",border_width=2, text_color=("gray10", "#DCE4EE"), command=self.connect)
            self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.logged_state=1
        elif self.logged_state == 1:
            self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="red", text="Disconnected",border_width=2, text_color=("gray10", "#DCE4EE"), command=self.connect)
            self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.logged_state=0           

if __name__ == "__main__":
    app = App()

    try:
        print("API has started" )
        app.mainloop()
    except KeyboardInterrupt:
        print("closing the app" )
        app.destroy()
        
