import tkinter
import tkinter.messagebox
import customtkinter
import socket
import serial
import time 
from datetime import datetime
import threading


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

my_socket = socket.socket()


class robot_controller():
    def __init__(self) -> None:
        # Servo angle init
        self.servo_1_pos = 90
        self.servo_2_pos = 130
        self.servo_3_pos = 130
        self.servo_4_pos = 180
        self.servo_5_pos = 90
        self.servo_6_pos = 100
        self.servo_speed = 50
        self.communication_state=0
        self.communication_button_toggle = 0
        self.client
        self.valid_servo_id = [1,2,3,4,5,6]
        self.ser = False
        self.servo_1_pos_written = 90
        self.servo_2_pos_written = 130
        self.servo_3_pos_written = 130
        self.servo_4_pos_written = 180
        self.servo_5_pos_written = 90
        self.servo_6_pos_written = 100
        self.programing_mode=False
        self.logself = 0

        self.recorded_pos= []

    # def connect(self):
    #     try:
    #         my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #         my_socket.bind(('0.0.0.0', 8090 ))
    #         my_socket.listen(0)
    #         self.client, addr = my_socket.accept()
    #         write = "hellow from script"
    #         self.client.send(write.encode())
    #         content = self.client.recv(10)
    #         if len(content) ==0:
    #             print("breaking")
    #         else:
    #             msg_recv = content.decode()
    #             print(msg_recv)
    #         if msg_recv == "ok":
    #             print("[INFO] : Connected")
    #             self.communication_state=True
    #             return True
    #         else:
    #             return False
    #     except:
    #         print("[Error] : not able to communicate !")
    #         return False

    def connect(self):
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200)
            if self.ser.is_open:
                print("[INFO] : Connected")
                log_to_console.info(self.logself, "Connected")
                self.communication_state=True
                return True
        except:
            print("[Error] : not able to communicate !")
            log_to_console.error(self.logself, "Unable to connect")
            return False
    
    def disconnect(self):
        self.ser.close()
        self.communication_state=False
        print("[INFO] : Disconnected")

    # def disconnect(self):
    #     my_socket.close()
    #     self.client.close()
    #     self.communication_state=False
    #     print("[INFO] : Disconnected")

    def home_pos_updater(self) -> None:
        self.servo_1_pos = 90
        self.servo_2_pos = 130
        self.servo_3_pos = 130
        self.servo_4_pos = 180
        self.servo_5_pos = 90
        self.servo_6_pos = 100
        self.servo_speed = 50
        self.servo_1_pos_written = 90
        self.servo_2_pos_written = 130
        self.servo_3_pos_written = 130
        self.servo_4_pos_written = 180
        self.servo_5_pos_written = 90
        self.servo_6_pos_written = 100

    def data_diff_checker(self):
        # while True:
        print("running")
        log_to_console.info(self.logself, "data_diff_checker running")
        while self.communication_state:

            if self.servo_1_pos != self.servo_1_pos_written or self.servo_2_pos != self.servo_2_pos_written or self.servo_3_pos != self.servo_3_pos_written:
                self.rx_tx_with_robot(self.servo_1_pos, self.servo_2_pos, self.servo_3_pos, self.servo_4_pos, self.servo_5_pos, self.servo_6_pos, self.servo_speed)
                break

            elif self.servo_4_pos != self.servo_4_pos_written or self.servo_5_pos != self.servo_5_pos_written or self.servo_6_pos != self.servo_6_pos_written:
                self.rx_tx_with_robot(self.servo_1_pos, self.servo_2_pos, self.servo_3_pos, self.servo_4_pos, self.servo_5_pos, self.servo_6_pos, self.servo_speed)
                break

            else:
                print(self.servo_1_pos, self.servo_1_pos_written)
                print(self.servo_2_pos, self.servo_2_pos_written)
                print(self.servo_3_pos, self.servo_3_pos_written)
                print(self.servo_4_pos, self.servo_4_pos_written)
                print(self.servo_5_pos, self.servo_5_pos_written)
                print(self.servo_6_pos, self.servo_6_pos_written)
                print("wrong input")
                log_to_console.warning(self.logself, "Input Provided is Wrong")
                break
        else:
            log_to_console.info(self.logself, "Please connect the controller to the Robotic arm")
            print("please connect the Controller to Robot")

        return
    
    def making_thread_for_jog(self):
        while True:
            while self.communication_state:
                # print("thread started")
                if self.servo_1_pos != self.servo_1_pos_written:
                    self.servo_1_pos_written = self.servo_1_pos
                    self.write_jog_pos(self.servo_1_pos, 1)

                elif self.servo_2_pos != self.servo_2_pos_written:
                    self.servo_2_pos_written = self.servo_2_pos
                    self.write_jog_pos(self.servo_2_pos, 2)

                elif self.servo_3_pos != self.servo_3_pos_written:
                    self.servo_3_pos_written = self.servo_3_pos
                    self.write_jog_pos(self.servo_3_pos, 3)

                elif self.servo_4_pos != self.servo_4_pos_written:
                    self.servo_4_pos_written = self.servo_4_pos
                    self.write_jog_pos(self.servo_4_pos, 4)

                elif self.servo_5_pos != self.servo_5_pos_written:
                    self.servo_5_pos_written = self.servo_5_pos
                    self.write_jog_pos(self.servo_5_pos, 5)

                elif self.servo_6_pos != self.servo_6_pos_written:
                    self.servo_6_pos_written = self.servo_6_pos
                    self.write_jog_pos(self.servo_6_pos, 6)

                # else:
                    # print("No changes")
                    # log_to_console.warning(self.logself, "Input Provided is Wrong")
                time.sleep(0.01)    
            else:
                # log_to_console.info(self.logself, "Please connect the controller to the Robotic arm")
                # print("please connect the Controller to Robot")
                time.sleep(0.8)


    def write_jog_pos(self, position, servo_id):
        execution_type = 2
        while servo_id in self.valid_servo_id:
            try:
                tcp_msg = f"[{execution_type}][{position}][{self.servo_speed}][{servo_id}]"
                print(f"send TCP MSG [{tcp_msg}]")
                log_to_console.info(self.logself, f"Sent frame {tcp_msg}")
                self.ser.write(bytes(tcp_msg, 'utf-8'))
                return
                # content = self.ser.readline()
                # content = str(content, 'UTF-8')
                # print(content)
                # log_to_console.info(self.logself, f"Recived frame {content}")
                # if content == "ok\r\n":
                #     print("writing done")
                #     log_to_console.info(self.logself, f"writing done")
                #     break
                # else:
                #     print("error")
                #     log_to_console.error(self.logself, f"Response Error")
                #     break
            except:
                print("[Error] : ocurred in jog while writing")
                log_to_console.error(self.logself, "Ocurred in jog while writing")
                return
        else:
            print(f"[ERROR] : wrong input servo id {servo_id}")
            log_to_console.error(self.logself, f"wrong input servo id {servo_id}")

    def pose_updater_after_written(self, servo_1_pos, servo_2_pos, servo_3_pos, servo_4_pos, servo_5_pos, servo_6_pos):
        print("updating")
        log_to_console.info(self.logself, f"Position updating after Move Execution")
        self.servo_1_pos_written = servo_1_pos
        self.servo_2_pos_written = servo_2_pos
        self.servo_3_pos_written = servo_3_pos
        self.servo_4_pos_written = servo_4_pos
        self.servo_5_pos_written = servo_5_pos
        self.servo_6_pos_written = servo_6_pos
        print("updated")
        log_to_console.info(self.logself, f"Position Updated")

    def rx_tx_with_robot(self, servo_1_pos, servo_2_pos, servo_3_pos, servo_4_pos, servo_5_pos, servo_6_pos, servo_speed):
        while True:
            try:
                self.pose_updater_after_written(servo_1_pos, servo_2_pos, servo_3_pos, servo_4_pos, servo_5_pos, servo_6_pos)
                msg_format = f"[{servo_1_pos}][{servo_2_pos}][{servo_3_pos}][{servo_4_pos}][{servo_5_pos}][{servo_6_pos}][{servo_speed}]"
                print("writing")
                log_to_console.info(self.logself, f"Writing data frame to robot {msg_format}")
                self.ser.write(bytes(msg_format, 'utf-8'))
                print("written")
                if self.programing_mode:
                    content = self.ser.readline()
                    content = str(content, 'UTF-8')
                    print(content)
                    log_to_console.info(self.logself, f"Recived frame {content}")
                    if content == "ok\r\n":
                        print("writing done")
                        log_to_console.info(self.logself, f"writing done")
                        break
                    else:
                        print("error")
                        log_to_console.error(self.logself, f"Response Error")
                        break
                else:
                    break
            except:
                print("error ocuured while writing")
                log_to_console.error(self.logself, f"Error ocuured while writing rx_tx_with_robot")
                break
    
    def run_recorded_pos(self, index):
        while True:
            try:
                msg_format = f"{self.recorded_pos[index]}"
                print("writing")
                log_to_console.info(self.logself, f"Sending frame to controller .....")
                self.ser.flush()
                self.ser.write(bytes(msg_format, 'utf-8'))
                print("written")
                log_to_console.info(self.logself, f"Frame sent.")
                content = self.ser.readline()
                content = str(content, 'UTF-8')
                print(content)
                log_to_console.info(self.logself, f"Recived frame {content}")
                timeout = 0
                while content != "ok\r\n":
                    if timeout <= 3:
                        time.sleep(1)
                        timeout+=1
                        content = self.ser.readline()
                        content = str(content, 'UTF-8')
                        print(content)
                    else:
                        print("not able to recive msg")
                        return
                        
                if content == "ok\r\n":
                    print("Response True")
                    time.sleep(3)
                    return
                else:
                    print("error occured in running recorded trajectory")
                    log_to_console.error(self.logself, f"Response Error")
                    return

            except:
                print("error ocuured while writing")
                log_to_console.error(self.logself, f"Error ocuured while writing rx_tx_with_robot")
                return
class push_action():
    def __init__(self, app_name, process_name, console_id_name):
        self.action_running=False
        self.app_name=app_name
        self.process_name=process_name

    def start_action(self, event):
        self.action_running = True
        self.perform_action()

    def stop_action(self, event):
        self.action_running = False

    def perform_action(self):
        if self.action_running:
            print(f"Action is running...{self.process_name}")
            self.app_name.after(100, self.perform_action)  # Continue the action if the button is held down  

class App(customtkinter.CTk, robot_controller):
    def __init__(self):
        super().__init__()

        # initializating robot controller
        robot_controller.__init__(self)

        # using log_to_console as log
        log_to_console.__init__(self)


        # configure window
        self.title("Robot Controller")
        self.geometry(f"{1300}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Controller", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Help",command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="About", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_arm = customtkinter.CTkButton(self.sidebar_frame, text="Home ARM", command=self.start_homing)
        self.home_arm.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text=" ", anchor="w", font=customtkinter.CTkFont(size=16))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create robot status and connection button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Robot Status : Ideal")
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.connection_btn = customtkinter.CTkButton(master=self, fg_color="red", text="Disconnected",border_width=2, text_color=("gray10", "#DCE4EE"), command=self.connection_handler)
        self.connection_btn.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, columnspan=2,padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.tabview.add("Teach Mode")
        self.tabview.add("Debug Mode")

        # configuring Teach mode tab grid
        self.tabview.tab("Teach Mode").grid_rowconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabview.tab("Teach Mode").grid_rowconfigure(1, weight=90)  # configure grid of individual tabs
        self.tabview.tab("Teach Mode").grid_rowconfigure(3, weight=5)  # configure grid of individual tabs
        self.tabview.tab("Teach Mode").grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        # adding servo id for Teach mode
        self.seg_button_1 = customtkinter.CTkSegmentedButton( self.tabview.tab("Teach Mode"))
        self.seg_button_1.grid(row=0, column=0, columnspan=12, padx=0, pady=(10, 10), sticky="nsew")

        # slider for jogging the arm 
        self.row_for_slider = 1
        # Servo ID = 1
        self.servo_1 = customtkinter.CTkSlider( self.tabview.tab("Teach Mode"),  orientation="vertical", command=self.servo_1_position_updater)
        self.servo_1.grid(row=self.row_for_slider, column=0, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.servo_1_state = customtkinter.CTkProgressBar( self.tabview.tab("Teach Mode"), orientation="vertical")
        self.servo_1_state.grid(row=self.row_for_slider, column=1, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 2
        self.servo_2 = customtkinter.CTkSlider( self.tabview.tab("Teach Mode"), orientation="vertical", command=self.servo_2_position_updater)
        self.servo_2.grid(row=self.row_for_slider, column=2, pady=(10, 10), sticky="ns")
        self.servo_2_state = customtkinter.CTkProgressBar( self.tabview.tab("Teach Mode"), orientation="vertical")
        self.servo_2_state.grid(row=self.row_for_slider, column=3, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 3
        self.servo_3 = customtkinter.CTkSlider( self.tabview.tab("Teach Mode"), orientation="vertical", command=self.servo_3_position_updater)
        self.servo_3.grid(row=self.row_for_slider, column=4, pady=(10, 10), sticky="ns")
        self.servo_3_state = customtkinter.CTkProgressBar( self.tabview.tab("Teach Mode"), orientation="vertical")
        self.servo_3_state.grid(row=self.row_for_slider, column=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 4
        self.servo_4 = customtkinter.CTkSlider( self.tabview.tab("Teach Mode"), orientation="vertical", command=self.servo_4_position_updater)
        self.servo_4.grid(row=self.row_for_slider, column=6, pady=(10, 10), sticky="ns")
        self.servo_4_state = customtkinter.CTkProgressBar( self.tabview.tab("Teach Mode"), orientation="vertical")
        self.servo_4_state.grid(row=self.row_for_slider, column=7, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 5
        self.servo_5 = customtkinter.CTkSlider( self.tabview.tab("Teach Mode"), orientation="vertical", command=self.servo_5_position_updater)
        self.servo_5.grid(row=self.row_for_slider, column=8, pady=(10, 10), sticky="ns")
        self.servo_5_state = customtkinter.CTkProgressBar( self.tabview.tab("Teach Mode"), orientation="vertical")
        self.servo_5_state.grid(row=self.row_for_slider, column=9, padx=(10, 10), pady=(10, 10), sticky="ns")
        # Servo ID = 6
        self.servo_6 = customtkinter.CTkSlider( self.tabview.tab("Teach Mode"), orientation="vertical", command=self.servo_6_position_updater)
        self.servo_6.grid(row=self.row_for_slider, column=10, pady=(10, 10), sticky="ns")
        self.servo_6_state = customtkinter.CTkProgressBar( self.tabview.tab("Teach Mode"), orientation="vertical")
        self.servo_6_state.grid(row=self.row_for_slider, column=11, padx=(10, 10), pady=(10, 10), sticky="ns")

        self.stick_for_programming=""

        self.record_pos = customtkinter.CTkButton(self.tabview.tab("Teach Mode"), text="Record Pos", command=self.record_pos)
        self.record_pos.grid(row=3, column=0, columnspan=2, pady=(10, 10))

        self.start_execution = customtkinter.CTkButton(self.tabview.tab("Teach Mode"), text="Start Execution", command=self.start_program)
        self.start_execution.grid(row=3, column=5, columnspan=2, pady=(10, 10))

        self.stop_execution = customtkinter.CTkButton(self.tabview.tab("Teach Mode"), text="Stop Execution", command=self.stop_program)
        self.stop_execution.grid(row=3, column=10, columnspan=2, pady=(10, 10))


        self.servo_1_pos_info = customtkinter.CTkEntry(self.tabview.tab("Teach Mode"), placeholder_text="Servo 1 Pos : "+ str(self.servo_1_pos) +" deg")
        self.servo_1_pos_info.grid(row=2, column=0, columnspan=2,  pady=(10, 10), sticky="n")        

        self.servo_2_pos_info = customtkinter.CTkEntry(self.tabview.tab("Teach Mode"), placeholder_text="Servo 2 Pos : "+ str(self.servo_2_pos) +" deg")
        self.servo_2_pos_info.grid(row=2, column=2, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_3_pos_info = customtkinter.CTkEntry(self.tabview.tab("Teach Mode"), placeholder_text="Servo 3 Pos : "+ str(self.servo_3_pos) +" deg")
        self.servo_3_pos_info.grid(row=2, column=4, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_4_pos_info = customtkinter.CTkEntry(self.tabview.tab("Teach Mode"), placeholder_text="Servo 4 Pos : "+ str(self.servo_4_pos) +" deg")
        self.servo_4_pos_info.grid(row=2, column=6, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_5_pos_info = customtkinter.CTkEntry(self.tabview.tab("Teach Mode"), placeholder_text="Servo 5 Pos : "+ str(self.servo_5_pos) +" deg")
        self.servo_5_pos_info.grid(row=2, column=8, columnspan=2,  pady=(10, 10), sticky="n") 

        self.servo_6_pos_info = customtkinter.CTkEntry(self.tabview.tab("Teach Mode"), placeholder_text="Servo 6 Pos : "+ str(self.servo_6_pos) +" deg")
        self.servo_6_pos_info.grid(row=2, column=10, columnspan=2,  pady=(10, 10), sticky="n") 


        # Programming Mode mode tab grid
        self.tabview.tab("Debug Mode").columnconfigure((0), weight=1)
        self.tabview.tab("Debug Mode").rowconfigure(0, weight=0)
        self.tabview.tab("Debug Mode").rowconfigure(1, weight=1)

        self.console_heading = customtkinter.CTkLabel(self.tabview.tab("Debug Mode"), text="[ Debug Console logs ]")
        self.console_heading.grid(row=0, column=0, pady=(5, 5))

        self.console=customtkinter.CTkTextbox(self.tabview.tab("Debug Mode"), font=("font", 15))
        self.console.grid(row=1, column=0, padx=(20,20),sticky="nsew")
        self.console.insert("0.0",f"[INFO] [INIT] [{datetime.now()}] -> API has started.\n")
        self.console.configure(state="disabled")
        self.logself=self



        self.set_initial_parameter()
    
        threading.Thread(target=self.making_thread_for_jog, daemon=True).start()
        

    def set_initial_parameter(self):
        # set default values
        self.sidebar_button_3.configure(state="disabled", text="About")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.seg_button_1.configure(values=["Servo 1", "Servo 2", "Servo 3", "Servo 4", "Servo 5", "Servo 6"])
        self.seg_button_1.set("Servo 1")

        self.entry.configure(state="disabled")
        self.servo_1_pos_info.configure(state="disabled")
        self.servo_2_pos_info.configure(state="disabled")
        self.servo_3_pos_info.configure(state="disabled")
        self.servo_4_pos_info.configure(state="disabled")
        self.servo_5_pos_info.configure(state="disabled")
        self.servo_6_pos_info.configure(state="disabled")
        self.home_pos_updater_for_slider_info()

    def home_pos_updater_for_slider_info(self):
        self.servo_1_state.set(self.translate_slider(self.servo_1_pos, 0, 180, 0, 1))
        self.servo_2_state.set(self.translate_slider(self.servo_2_pos, 0, 180, 0, 1))
        self.servo_3_state.set(self.translate_slider(self.servo_3_pos, 0, 180, 0, 1))
        self.servo_4_state.set(self.translate_slider(self.servo_4_pos, 0, 180, 0, 1))
        self.servo_5_state.set(self.translate_slider(self.servo_5_pos, 0, 180, 0, 1))
        self.servo_6_state.set(self.translate_slider(self.servo_6_pos, 0, 180, 0, 1))

        self.servo_1.set(self.translate_slider(self.servo_1_pos, 0, 180, 0, 1))
        self.servo_2.set(self.translate_slider(self.servo_2_pos, 0, 180, 0, 1))
        self.servo_3.set(self.translate_slider(self.servo_3_pos, 0, 180, 0, 1))
        self.servo_4.set(self.translate_slider(self.servo_4_pos, 0, 180, 0, 1))
        self.servo_5.set(self.translate_slider(self.servo_5_pos, 0, 180, 0, 1))
        self.servo_6.set(self.translate_slider(self.servo_6_pos, 0, 180, 0, 1))

    def servo_1_position_updater(self, value):
        self.servo_1_state.set(value) 
        slider_val=self.translate(value, 1, 100, 1, 180)
        self.servo_1_pos=slider_val
        self.seg_button_1.set("Servo 1")
        # threading.Thread(target=self.write_jog_pos, args=(self.servo_1_pos, 1)).start()
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
        value=self.translate(value, 1, 100, 70, 130)
        if value < 70:
            self.servo_6_pos = 70
        self.servo_6_pos = value
        self.seg_button_1.set("Servo 6")
        self.position_entry_updater()


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

    def start_homing(self):
        threading.Thread(target= self.home_arm_request, daemon=True).start()
        # self.home_pos_updater_for_slider_info()

    def home_arm_request(self):
        print( "Homing called")
        try:
            log_to_console.info(self, "Homing called")
            msg_format = "[1]"
            self.ser.write(bytes(msg_format, 'utf-8'))
            log_to_console.info(self, "Homing called and has been executed")
            content = self.ser.readline()
            content = str(content, 'UTF-8')
            print(content)
            log_to_console.info(self.logself, f"Recived frame {content}")
            if content == "ok\r\n":
                print("writing done")
                log_to_console.info(self.logself, f"writing done")
                self.home_pos_updater()
                self.home_pos_updater_for_slider_info()
                
            else:
                print("error")
                log_to_console.error(self.logself, f"Response Error")
        except:
            log_to_console.error(self, "Not able to home")


    def record_pos(self):
        log_to_console.info(self, f"Recorded Cordinates with frame : [4][{self.servo_1_pos}][{self.servo_2_pos}][{self.servo_3_pos}][{self.servo_4_pos}][{self.servo_5_pos}][{self.servo_6_pos}][{self.servo_speed}]")
        self.recorded_pos.append(f"[4][{self.servo_1_pos}][{self.servo_2_pos}][{self.servo_3_pos}][{self.servo_4_pos}][{self.servo_5_pos}][{self.servo_6_pos}][{self.servo_speed}]")
        print(len(self.recorded_pos))

    def execute_(self):
        no_of_cycle = 0
        while no_of_cycle < len(self.recorded_pos):
            print(no_of_cycle, len(self.recorded_pos))
            self.run_recorded_pos(no_of_cycle)
            print("executing", self.recorded_pos[no_of_cycle])
            log_to_console.info(self, f"executing{self.recorded_pos[no_of_cycle]}")
            print(no_of_cycle)
            no_of_cycle+=1
            print(no_of_cycle)
        print("done")
        log_to_console.info(self, "Execution Done")

    def start_program(self):
        print("starting program")
        log_to_console.info(self, "Starting Execution program")
        if (len(self.recorded_pos)) == 0:
            print("please record the trajectory")
            log_to_console.error(self, "please record the trajectory")
            return
        t1 = threading.Thread(target=self.execute_)
        t1.start()
        # self.execute_()

    def stop_program(self):
        self.recorded_pos.clear()
        log_to_console.info(self, "Execution has been stoped and data has been cleared")

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
        calculated_value = int(rightMin + (valueScaled * rightSpan))
        if calculated_value <=0:
            calculated_value=1

        return calculated_value

    def translate_slider(self, value, leftMin, leftMax, rightMin, rightMax):

        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        calculated_value = float(rightMin + (valueScaled * rightSpan))

        return calculated_value
    
    def connection_handler(self):
        print("connect to robot called")
        if self.communication_state == 0:
            log_to_console.info(self, "Connect to robot is requested")
            if self.connect():
                self.connection_btn.configure(fg_color="green",text="Connected")
                log_to_console.info(self, "Connect to robot is requested")
            else:
                log_to_console.error(self, "Connect to robot is faild")

        elif self.communication_state == 1:
            self.connection_btn.configure(fg_color="red", text="Disconnected")
            self.disconnect()
            log_to_console.warning(self, "Disconnect to robot is requested")
    def print_(self):    
        print("msg")
        time.sleep(1)

class log_to_console(App):
    def __init__(self):
        pass

    def info(self, msg):
        time_stamp = datetime.now()
        self.console.configure(state="normal")
        self.console.insert("insert",f"[INFO]    : [{time_stamp}] -> [ {msg} ]\n")
        self.console.configure(state="disabled")

    def warning(self, msg):
        time_stamp = datetime.now()
        self.console.configure(state="normal")
        self.console.insert("insert",f"[WARN]    : [{time_stamp}] -> [ {msg} ]\n")
        self.console.configure(state="disabled")

    def error(self, msg):
        time_stamp = datetime.now()
        self.console.configure(state="normal")
        self.console.insert("insert",f"[ERROR] : [{time_stamp}] -> [ {msg} ]\n")
        self.console.configure(state="disabled")


if __name__ == "__main__":
    try:
        app = App()        

        app.mainloop()
        
    except KeyboardInterrupt:
        print("keyboard interrupt")
