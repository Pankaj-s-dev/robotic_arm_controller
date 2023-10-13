import tkinter
import tkinter.messagebox
import customtkinter
import socket
import time 


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class robot_controller():
    def __init__(self) -> None:
        self.communication_state=0


class push_action():
    def __init__(self, app_name, process_id):
        self.action_running=False
        self.app_name=app_name
        self.process_id=process_id

    def start_action(self, event):
        self.action_running = True
        self.perform_action()

    def stop_action(self, event):
        self.action_running = False

    def perform_action(self):
        if self.action_running:
            print(f"Action is running...{self.process_id}")
            self.app_name.after(100, self.perform_action)  # Continue the action if the button is held down


class App(customtkinter.CTk, robot_controller):
    def __init__(self):
        super().__init__()

        # initializating robot controller
        robot_controller.__init__(self)

        self.servo_1_pos = 90
        self.servo_2_pos = 90
        self.servo_3_pos = 90
        self.servo_4_pos = 90
        self.servo_5_pos = 90
        self.servo_6_pos = 90
        self.servo_speed = 50

        # configure window
        self.title("Robot Controller")
        self.geometry(f"{1300}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Controller", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Help",command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="About", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance :", anchor="w", font=customtkinter.CTkFont(size=16))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create robot status and connection button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Robot Status : Ideal")
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.connection_btn = customtkinter.CTkButton(master=self, fg_color="red", text="Disconnected",border_width=2, text_color=("gray10", "#DCE4EE"), command=self.connect)
        self.connection_btn.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, columnspan=2,padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.tabview.add("Manual Mode")
        self.tabview.add("Programming Mode")
        self.tabview.add("Debug Mode")

        # configuring manual mode tab grid
        self.tabview.tab("Manual Mode").grid_rowconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabview.tab("Manual Mode").grid_rowconfigure(1, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Manual Mode").grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13), weight=1)

        # adding servo id for manual mode
        self.seg_button_1 = customtkinter.CTkSegmentedButton( self.tabview.tab("Manual Mode"))
        self.seg_button_1.grid(row=0, column=0, columnspan=14, padx=0, pady=(10, 10), sticky="nsew")

        # slider for jogging the arm 
        self.row_for_slider = 1
        # Servo ID = 1
        self.servo_1 = customtkinter.CTkSlider( self.tabview.tab("Manual Mode"),  orientation="vertical", command=self.servo_1_position_updater)
        self.servo_1.grid(row=self.row_for_slider, column=0, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.servo_1_state = customtkinter.CTkProgressBar( self.tabview.tab("Manual Mode"), orientation="vertical")
        self.servo_1_state.grid(row=self.row_for_slider, column=1, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 2
        self.servo_2 = customtkinter.CTkSlider( self.tabview.tab("Manual Mode"), orientation="vertical", command=self.servo_2_position_updater)
        self.servo_2.grid(row=self.row_for_slider, column=2, pady=(10, 10), sticky="ns")
        self.servo_2_state = customtkinter.CTkProgressBar( self.tabview.tab("Manual Mode"), orientation="vertical")
        self.servo_2_state.grid(row=self.row_for_slider, column=3, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 3
        self.servo_3 = customtkinter.CTkSlider( self.tabview.tab("Manual Mode"), orientation="vertical", command=self.servo_3_position_updater)
        self.servo_3.grid(row=self.row_for_slider, column=4, pady=(10, 10), sticky="ns")
        self.servo_3_state = customtkinter.CTkProgressBar( self.tabview.tab("Manual Mode"), orientation="vertical")
        self.servo_3_state.grid(row=self.row_for_slider, column=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 4
        self.servo_4 = customtkinter.CTkSlider( self.tabview.tab("Manual Mode"), orientation="vertical", command=self.servo_4_position_updater)
        self.servo_4.grid(row=self.row_for_slider, column=6, pady=(10, 10), sticky="ns")
        self.servo_4_state = customtkinter.CTkProgressBar( self.tabview.tab("Manual Mode"), orientation="vertical")
        self.servo_4_state.grid(row=self.row_for_slider, column=7, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 5
        self.servo_5 = customtkinter.CTkSlider( self.tabview.tab("Manual Mode"), orientation="vertical", command=self.servo_5_position_updater)
        self.servo_5.grid(row=self.row_for_slider, column=8, pady=(10, 10), sticky="ns")
        self.servo_5_state = customtkinter.CTkProgressBar( self.tabview.tab("Manual Mode"), orientation="vertical")
        self.servo_5_state.grid(row=self.row_for_slider, column=9, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 6
        self.servo_6 = customtkinter.CTkSlider( self.tabview.tab("Manual Mode"), orientation="vertical", command=self.servo_6_position_updater)
        self.servo_6.grid(row=self.row_for_slider, column=10, pady=(10, 10), sticky="ns")
        self.servo_6_state = customtkinter.CTkProgressBar( self.tabview.tab("Manual Mode"), orientation="vertical")
        self.servo_6_state.grid(row=self.row_for_slider, column=11, padx=(10, 10), pady=(10, 10), sticky="ns")
        # SServo Speed
        self.speed = customtkinter.CTkSlider( self.tabview.tab("Manual Mode"), orientation="vertical", command=self.speed_updater)
        self.speed.grid(row=self.row_for_slider, column=12, pady=(10, 10), sticky="ns")
        self.speed_state = customtkinter.CTkProgressBar( self.tabview.tab("Manual Mode"), orientation="vertical")
        self.speed_state.grid(row=self.row_for_slider, column=13, padx=(10, 10), pady=(10, 10), sticky="ns")
    
        self.servo_1_pos_info = customtkinter.CTkEntry(self.tabview.tab("Manual Mode"), placeholder_text="Servo 1 Pos : "+ str(self.servo_1_pos) +" deg")
        self.servo_1_pos_info.grid(row=2, column=0, columnspan=2,  pady=(10, 10), sticky="n")        

        self.servo_2_pos_info = customtkinter.CTkEntry(self.tabview.tab("Manual Mode"), placeholder_text="Servo 2 Pos : "+ str(self.servo_2_pos) +" deg")
        self.servo_2_pos_info.grid(row=2, column=2, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_3_pos_info = customtkinter.CTkEntry(self.tabview.tab("Manual Mode"), placeholder_text="Servo 3 Pos : "+ str(self.servo_3_pos) +" deg")
        self.servo_3_pos_info.grid(row=2, column=4, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_4_pos_info = customtkinter.CTkEntry(self.tabview.tab("Manual Mode"), placeholder_text="Servo 4 Pos : "+ str(self.servo_4_pos) +" deg")
        self.servo_4_pos_info.grid(row=2, column=6, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_5_pos_info = customtkinter.CTkEntry(self.tabview.tab("Manual Mode"), placeholder_text="Servo 5 Pos : "+ str(self.servo_5_pos) +" deg")
        self.servo_5_pos_info.grid(row=2, column=8, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_6_pos_info = customtkinter.CTkEntry(self.tabview.tab("Manual Mode"), placeholder_text="Servo 6 Pos : "+ str(self.servo_6_pos) +" deg")
        self.servo_6_pos_info.grid(row=2, column=10, columnspan=2,  pady=(10, 10), sticky="n") 

        self.speed_info = customtkinter.CTkEntry(self.tabview.tab("Manual Mode"), placeholder_text="Servo Speed : "+ str(self.servo_speed) +" %")
        self.speed_info.grid(row=2, column=12, columnspan=2,  pady=(10, 10), sticky="n")

        # Programming Mode mode tab grid
        self.tabview.tab("Programming Mode").columnconfigure((0,1,2,3,4,5), weight=1)
        self.tabview.tab("Programming Mode").rowconfigure((0,1,2), weight=1)

        self.stick_for_programming=""

        self.move_front = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Move Front", command=self.sidebar_button_event)
        self.move_front.grid(row=0, column=1, pady=(10, 10),ipady=(2), sticky=self.stick_for_programming)

        self.move_back = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Move Back", command=self.sidebar_button_event)
        self.move_back.grid(row=2, column=1, pady=(10, 10),ipady=(2), sticky=self.stick_for_programming)

        self.move_left = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Move Left", command=self.sidebar_button_event)
        self.move_left.grid(row=1, column=0, pady=(10, 10), ipady=(2),sticky=self.stick_for_programming)

        self.move_right = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Move Right", command=self.sidebar_button_event)
        self.move_right.grid(row=1, column=2, pady=(10, 10),ipady=(2), sticky=self.stick_for_programming)

        self.move_up = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Move Up", command=self.sidebar_button_event)
        self.move_up.grid(row=0, column=3, pady=(10, 10),ipady=(2), sticky=self.stick_for_programming)

        self.move_down = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Move Down", command=self.sidebar_button_event)
        self.move_down.grid(row=2, column=3, pady=(10, 10),ipady=(2), sticky=self.stick_for_programming)

        self.open_gripper = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Open Gripper", command=self.sidebar_button_event)
        self.open_gripper.grid(row=0, column=4, pady=(10, 10),ipady=(2), sticky=self.stick_for_programming)

        self.close_gripper = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Close Gripper", command=self.sidebar_button_event)
        self.close_gripper.grid(row=2, column=4, pady=(10, 10),ipady=(2), sticky=self.stick_for_programming)

        self.record_pos = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Record Pos", command=self.sidebar_button_event)
        self.record_pos.grid(row=0, column=5, pady=(10, 10), ipady=(2),sticky=self.stick_for_programming)

        self.start_execution = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Start Execution", command=self.sidebar_button_event)
        self.start_execution.grid(row=1, column=5, pady=(10, 10), ipady=(2),sticky=self.stick_for_programming)

        self.stop_execution = customtkinter.CTkButton(self.tabview.tab("Programming Mode"), text="Stop Execution", command=self.sidebar_button_event)
        self.stop_execution.grid(row=2, column=5, pady=(10, 10), ipady=(2), sticky=self.stick_for_programming)

        self.execution_speed = customtkinter.CTkSlider( self.tabview.tab("Programming Mode"), orientation="horizontal", command=self.speed_updater)
        self.execution_speed.grid(row=1, column=3, columnspan=2, padx=(20, 20), sticky="ew")

        self.action_stop_execution=push_action(self, "Stop Exexution")
        self.stop_execution.bind("<ButtonPress-1>", self.action_stop_execution.start_action)  # Bind mouse button press to start action
        self.stop_execution.bind("<ButtonRelease-1>", self.action_stop_execution.stop_action)  # Bind mouse button release to stop action

        self.action_start_execution=push_action(self, "Start Execution")
        self.start_execution.bind("<ButtonPress-1>", self.action_start_execution.start_action)
        self.start_execution.bind("<ButtonRelease-1>", self.action_start_execution.stop_action)


        # Programming Mode mode tab grid
        self.tabview.tab("Debug Mode").columnconfigure((0), weight=1)
        self.tabview.tab("Debug Mode").rowconfigure(0, weight=0)
        self.tabview.tab("Debug Mode").rowconfigure(1, weight=1)

        self.console_heading = customtkinter.CTkLabel(self.tabview.tab("Debug Mode"), text="[ Debug Console logs ]")
        self.console_heading.grid(row=0, column=0, pady=(5, 5))

        self.console=customtkinter.CTkTextbox(self.tabview.tab("Debug Mode"))
        self.console.grid(row=1, column=0, padx=(20,20),sticky="nsew")
        self.console.insert("0.0","Hello World!\n")
        self.console.configure(state="disabled")


        self.set_initial_parameter()

    def set_initial_parameter(self):
        # set default values
        self.sidebar_button_3.configure(state="disabled", text="About")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.seg_button_1.configure(values=["Servo 1", "Servo 2", "Servo 3", "Servo 4", "Servo 5", "Servo 6", "Servo Speed"])
        self.seg_button_1.set("Servo 1")

        self.entry.configure(state="disabled")
        self.servo_1_pos_info.configure(state="disabled")
        self.servo_2_pos_info.configure(state="disabled")
        self.servo_3_pos_info.configure(state="disabled")
        self.servo_4_pos_info.configure(state="disabled")
        self.servo_5_pos_info.configure(state="disabled")
        self.servo_6_pos_info.configure(state="disabled")
        self.speed_info.configure(state="disabled")

    def servo_1_position_updater(self, value):
        self.servo_1_state.set(value) 
        slider_val=self.translate(value, 1, 100, 1, 180)
        self.servo_1_pos=slider_val
        self.seg_button_1.set("Servo 1")
        self.position_entry_updater()

    def servo_2_position_updater(self, value):
        self.servo_2_state.set(value) 
        self.servo_2_pos=self.translate(value, 1, 100, 1, 180)
        self.seg_button_1.set("Servo 2")
        self.position_entry_updater()

    def servo_3_position_updater(self, value):
        self.servo_3_state.set(value) 
        self.servo_3_pos=self.translate(value, 1, 100, 1, 180)
        self.seg_button_1.set("Servo 3")
        self.position_entry_updater()

    def servo_4_position_updater(self, value):
        self.servo_4_state.set(value) 
        self.servo_4_pos=self.translate(value, 1, 100, 1, 180)
        self.seg_button_1.set("Servo 4")
        self.position_entry_updater()

    def servo_5_position_updater(self, value):
        self.servo_5_state.set(value) 
        self.servo_5_pos=self.translate(value, 1, 100, 1, 180)
        self.seg_button_1.set("Servo 5")
        self.position_entry_updater()

    def servo_6_position_updater(self, value):
        self.servo_6_state.set(value) 
        self.servo_6_pos=self.translate(value, 1, 100, 1, 180)
        self.seg_button_1.set("Servo 6")
        self.position_entry_updater()

    def speed_updater(self, value):
        self.speed_state.set(value)
        self.servo_speed=self.translate(value, 1, 100, 1, 100)
        self.seg_button_1.set("Servo Speed")
        self.speed_info.configure(state="normal")
        self.speed_info.configure(placeholder_text="Servo Speed : "+ str(self.servo_speed) +" %")
        self.speed_info.configure(state="disabled")

    def position_entry_updater(self):
        self.servo_1_pos_info.configure(state="normal")
        self.servo_2_pos_info.configure(state="normal")
        self.servo_3_pos_info.configure(state="normal")
        self.servo_4_pos_info.configure(state="normal")
        self.servo_5_pos_info.configure(state="normal")
        self.servo_6_pos_info.configure(state="normal")
        self.servo_1_pos_info.configure(placeholder_text="Servo 1 Pos : "+ str(self.servo_1_pos) +" deg")
        self.servo_2_pos_info.configure(placeholder_text="Servo 2 Pos : "+ str(self.servo_2_pos) +" deg")
        self.servo_3_pos_info.configure(placeholder_text="Servo 3 Pos : "+ str(self.servo_3_pos) +" deg")
        self.servo_4_pos_info.configure(placeholder_text="Servo 4 Pos : "+ str(self.servo_4_pos) +" deg")
        self.servo_5_pos_info.configure(placeholder_text="Servo 5 Pos : "+ str(self.servo_5_pos) +" deg")
        self.servo_6_pos_info.configure(placeholder_text="Servo 6 Pos : "+ str(self.servo_6_pos) +" deg")
        self.servo_1_pos_info.configure(state="disabled")
        self.servo_2_pos_info.configure(state="disabled")
        self.servo_3_pos_info.configure(state="disabled")
        self.servo_4_pos_info.configure(state="disabled")
        self.servo_5_pos_info.configure(state="disabled")
        self.servo_6_pos_info.configure(state="disabled")


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        value = self.servo_1.get()
        value_1=self.translate(value, 1, 100, 1, 180)
        print("sidebar_button click", value_1)

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        value = value*100
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return int(rightMin + (valueScaled * rightSpan))

    def connect(self):
        print("connect to robot called")
        if self.communication_state == 0:
            self.connection_btn.configure(fg_color="green",text="Connected")
            self.communication_state=1
        elif self.communication_state == 1:
            self.connection_btn.configure(fg_color="red", text="Disconnected")
            self.communication_state=0   


if __name__ == "__main__":
    app = App()
    app.mainloop()