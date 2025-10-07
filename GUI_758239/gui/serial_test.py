import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import messagebox
from ttkbootstrap.widgets import Meter
import tkinter as tk
import serial
import serial.tools.list_ports
import threading
import array as array
import time

class SerialGUI:
    bauds = ["9600","19200","38400", "57600", "115200"]

    def __init__(self, master):
        self.master = master
        master.title("Test Fixture 758239")

        self.serial_port = None
        self.running = False
        self.step = 1
        self.entry_var_boxstep = tk.StringVar(value=1)
        self.entry_var_boxA0 = tk.StringVar(value=0)
        self.entry_var_boxA1 = tk.StringVar(value=0)
        self.entry_var_boxA2 = tk.StringVar(value=0)
        self.entry_var_boxA3 = tk.StringVar(value=0)
        self.entry_var_boxA4 = tk.StringVar(value=0)
        self.entry_var_boxA5 = tk.StringVar(value=0)

        self.entry_var_boxD2 = tk.StringVar(value="***")
        self.entry_var_boxD3 = tk.StringVar(value="***")
        self.entry_var_boxD4 = tk.StringVar(value="***")
        self.entry_var_boxD48 = tk.StringVar(value="***")
        self.entry_var_boxD53 = tk.StringVar(value="***")

        # Frame chọn COM và Baudrate ------------------------------------------------------------------------
        frame_top = tb.Frame(master)
        frame_top.pack(padx=10, pady=5)

        tb.Label(frame_top, text="COM Port:").grid(column=0, row=0)
        self.combo_port = tb.Combobox(frame_top, values=self.get_serial_ports(), width=10)
        self.combo_port.grid(column=1, row=0, padx=5)
        self.combo_port.set("COM1")

        tb.Label(frame_top, text="Baudrate:").grid(column=2, row=0)
        self.combo_baud = tb.Combobox(frame_top, values=SerialGUI.bauds, width=10)
        self.combo_baud.grid(column=3, row=0, padx=5)
        self.combo_baud.set("115200")

        self.btn_connect = tb.Button(frame_top, text="Connect", width=12, command=self.toggle_connection, bootstyle=(INFO, OUTLINE))
        self.btn_connect.grid(column=4, row=0, padx=5)

        self.btn_refresh = tb.Button(frame_top, text="Refresh", width=12, command=self.refresh_combo_port, bootstyle=(INFO, OUTLINE))
        self.btn_refresh.grid(column=5, row=0, padx=5)

        # Frame button control test  --------------------------------------------------------------------------
        frame_top_2 = tb.Frame(master)
        frame_top_2.pack(padx=10, pady=5)

        self.btn_start = tb.Button(frame_top_2, text="Start Test", command=self.btn_start_test_method, bootstyle=(SUCCESS, OUTLINE))
        self.btn_start.grid(column=1, row=0, padx=5)

        self.btn_run_step = tb.Button(frame_top_2, text="Run Step", command=self.btn_run_step_method, bootstyle=(SUCCESS, OUTLINE))
        self.btn_run_step.grid(column=2, row=0, padx=5)

        self.boxstep = tb.Spinbox(frame_top_2, from_=1, to=8, increment=1, textvariable=self.entry_var_boxstep, style="primary", width=7, command=self.spinbox_change_step_method)
        self.boxstep.grid(column=3, row=0, padx=5)

        self.btn_stop = tb.Button(frame_top_2, text="Stop Test", command=self.btn_stop_test_method, bootstyle=(DANGER, OUTLINE))
        self.btn_stop.grid(column=4, row=0, padx=5)

        self.btn_auto = tb.Button(frame_top_2, text="Auto Test", command=self.btn_auto_test_method, bootstyle=(SUCCESS, OUTLINE))
        self.btn_auto.grid(column=5, row=0, padx=5)

        # frame value analog  --------------------------------------------------------------------------
        frame_mid = tb.Frame(master)
        frame_mid.pack(padx=10, pady=10)

        tb.Label(frame_mid, text="ADC0 (J13-14):").grid(column=0, row=0, padx=10)
        self.boxA0 = tb.Entry(frame_mid, textvariable=self.entry_var_boxA0, state=READONLY, style="primary", width=10)
        self.boxA0.grid(column=0, row=1, padx=10)

        tb.Label(frame_mid, text="ADC1 (J13-13):").grid(column=1, row=0, padx=10)
        self.boxA1 = tb.Entry(frame_mid, textvariable=self.entry_var_boxA1, state=READONLY, style="primary", width=10)
        self.boxA1.grid(column=1, row=1, padx=10)

        tb.Label(frame_mid, text="ADC2 (J13-12):").grid(column=2, row=0, padx=10)
        self.boxA2 = tb.Entry(frame_mid, textvariable=self.entry_var_boxA2, state=READONLY, style="primary", width=10)
        self.boxA2.grid(column=2, row=1, padx=10)

        tb.Label(frame_mid, text="ADC3 (J13-11):").grid(column=3, row=0, padx=10)
        self.boxA3 = tb.Entry(frame_mid, textvariable=self.entry_var_boxA3, state=READONLY, style="primary", width=10)
        self.boxA3.grid(column=3, row=1, padx=10)

        tb.Label(frame_mid, text="ADC4 (J13-6):").grid(column=4, row=0, padx=10)
        self.boxA4 = tb.Entry(frame_mid, textvariable=self.entry_var_boxA4, state=READONLY, style="primary", width=10)
        self.boxA4.grid(column=4, row=1, padx=10)

        tb.Label(frame_mid, text="ADC5 (J13-4):").grid(column=5, row=0, padx=10)
        self.boxA5 = tb.Entry(frame_mid, textvariable=self.entry_var_boxA5, state=READONLY, style="primary", width=10)
        self.boxA5.grid(column=5, row=1, padx=10)

        # frame value digital  --------------------------------------------------------------------------
        frame_mid = tb.Frame(master)
        frame_mid.pack(padx=10, pady=10)

        tb.Label(frame_mid, text="D2 (J2-1):").grid(column=0, row=0, padx=10)
        self.boxD2 = tb.Entry(frame_mid, textvariable=self.entry_var_boxD2, state=READONLY, style="primary", width=10)
        self.boxD2.grid(column=0, row=1, padx=10)

        tb.Label(frame_mid, text="D3 (J2-4):").grid(column=1, row=0, padx=10)
        self.boxD3 = tb.Entry(frame_mid, textvariable=self.entry_var_boxD3, state=READONLY, style="primary", width=10)
        self.boxD3.grid(column=1, row=1, padx=10)

        tb.Label(frame_mid, text="D4 (J2-5):").grid(column=2, row=0, padx=10)
        self.boxD4 = tb.Entry(frame_mid, textvariable=self.entry_var_boxD4, state=READONLY, style="primary", width=10)
        self.boxD4.grid(column=2, row=1, padx=10)

        tb.Label(frame_mid, text="D48 (J13-10):").grid(column=3, row=0, padx=10)
        self.boxD48 = tb.Entry(frame_mid, textvariable=self.entry_var_boxD48, state=READONLY, style="primary", width=10)
        self.boxD48.grid(column=3, row=1, padx=10)

        tb.Label(frame_mid, text="D53 (J13-5):").grid(column=4, row=0, padx=10)
        self.boxD53 = tb.Entry(frame_mid, textvariable=self.entry_var_boxD53, state=READONLY, style="primary", width=10)
        self.boxD53.grid(column=4, row=1, padx=10)

        # Frame meter + serial log  -----------------------------------------------------------------------
        main_frame = tb.Frame(master)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        center_frame = tb.Frame(main_frame)
        center_frame.pack(anchor='center')

        # ===== Left Frame =====
        left_frame = tb.Frame(center_frame)
        left_frame.grid(row=0, column=0, sticky="nsw", padx=10)

        # Tạo Meter
        self.meter = Meter(
            left_frame,
            metersize=200,     # size meter (pixel)
            amounttotal=100,       
            amountused=0,         
            bootstyle="info",   
            subtext="Progress Test",       
            textfont=("Helvetica", 16, "bold")
        )
        self.meter.pack()

        # ===== Right Frame =====
        right_frame = tb.Frame(center_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        # Text hiển thị dữ liệu nhận được
        self.text_area = ScrolledText(right_frame, height=13, width=65, autohide=True, bootstyle=SECONDARY)
        self.text_area.grid(column=0, row=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.text_area.text.config(state=tb.DISABLED)
        self.text_area.text.tag_config("redline", foreground="red")
        self.text_area.text.tag_config("greenline", foreground="green")

        # entry and button
        self.entry_send = tb.Entry(right_frame, width=40)
        self.entry_send.grid(column=0, row=1)
        self.btn_send = tb.Button(right_frame, text="Send", command=self.btn_send_data_method, bootstyle=(SUCCESS, OUTLINE))
        self.btn_send.grid(column=1, row=1, padx=5)
        self.btn_clear = tb.Button(right_frame, text="Clear", command=self.btn_clear_screen_method, bootstyle=DANGER)
        self.btn_clear.grid(column=2, row=1, padx=5)
        # Expand right_frame để chiếm phần còn lại
        main_frame.columnconfigure(1, weight=1)

        self.array_boxs = [self.boxA0, self.boxA1, self.boxA2, self.boxA3, self.boxA4, self.boxA5]
        self.array_entry_boxs = [self.entry_var_boxA0, self.entry_var_boxA1, self.entry_var_boxA2, self.entry_var_boxA3, self.entry_var_boxA4, self.entry_var_boxA5]
        self.array_Dboxs = [self.boxD2, self.boxD3, self.boxD4, self.boxD48, self.boxD53]
        self.array_entry_Dboxs = [self.entry_var_boxD2, self.entry_var_boxD3, self.entry_var_boxD4, self.entry_var_boxD48, self.entry_var_boxD53]
        self.disabled_components()

    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def refresh_combo_port(self):
        ports = self.get_serial_ports()
        self.combo_port.configure(values=ports)

    def disabled_components(self):
        self.btn_send.configure(state=DISABLED)
        self.entry_send.configure(state=DISABLED)
        self.btn_start.configure(state=DISABLED)
        self.btn_stop.configure(state=DISABLED)
        self.btn_auto.configure(state=DISABLED)
        self.btn_run_step.configure(state=DISABLED)
        self.boxstep.configure(state=DISABLED)

    def active_components(self):
        self.btn_send.configure(state=ACTIVE)
        self.entry_send.configure(state=ACTIVE)
        self.set_meter_value(0)
        self.btn_start.configure(state=ACTIVE)
        self.btn_stop.configure(state=ACTIVE)
        self.btn_auto.configure(state=ACTIVE)
        self.btn_run_step.configure(state=ACTIVE)
        self.boxstep.configure(state=ACTIVE)

    def toggle_connection(self):
        time.sleep(0.5)  # Delay to ensure the UI is responsive
        if self.serial_port and self.serial_port.is_open:
            self.on_disconnect()
            self.disabled_components()
            self.reset_gui_boxsEntry()
            self.btn_connect.config(text="Connect")
            self.text_area.text.config(state=tb.NORMAL)
            self.text_area.text.insert(tb.END, "Disconnected\n")
            self.text_area.text.config(state=tb.DISABLED)
            self.meter.configure(amountused=0, bootstyle="info", subtext="Progress Test")
            self.running = False
            self.serial_port.close()
        else:
            try:
                port = self.combo_port.get()
                baud = int(self.combo_baud.get())
                self.serial_port = serial.Serial(port, baud, timeout=0.1)
                self.running = True
                threading.Thread(target=self.read_serial, daemon=True).start()
                self.btn_connect.config(text="Disconnect")
                self.text_area.text.config(state=tb.NORMAL)
                self.text_area.text.insert(tb.END, f"Connected to {port} at {baud} baud\n")
                self.text_area.text.config(state=tb.DISABLED)
                self.active_components()
                self.btn_run_step.configure(state=DISABLED)
                self.boxstep.configure(state=DISABLED)
            except Exception as e:
                messagebox.showerror("Connection Error", str(e))

    def read_serial(self):
        while self.running and self.serial_port.is_open:
            try:
                data = self.serial_port.readline().decode('utf-8', errors='ignore')
                if data:
                    data_splits = data.split("-")
                    if data_splits[0].strip() == "STOP":
                        self.insert_text_area("[System Log] Test stopped by user!\n", redline=True)
                        continue

                    if(data_splits[0] == "S" or data_splits[0] == "E"):
                        self.handle_meter_step(data_splits)
                        continue

                    if(data_splits[0] == "P" or data_splits[0] == "F"):
                        if data_splits[1] == "1":
                            self.handle_step_1(data_splits)
                        elif data_splits[1] == "2":
                            self.handle_step_2(data_splits)
                        elif data_splits[1] == "3":
                            self.handle_step_3(data_splits)
                        elif data_splits[1] == "4":
                            self.handle_step_4(data_splits)
                        elif data_splits[1] == "5":
                            self.handle_step_5(data_splits)
                        elif data_splits[1] == "6":
                            self.handle_step_6(data_splits)
                        elif data_splits[1] == "7":
                            self.handle_step_7(data_splits)
                        elif data_splits[1] == "8":
                            self.handle_step_8(data_splits)
                        continue
                            
                    # Log Results after test all steps
                    if(data_splits[0].strip() == "PASS"):
                        self.meter.configure(bootstyle="success", subtext="Test Passed")
                        self.insert_text_area(data, greenline=True)
                        continue
                    if(data_splits[0] == "FAIL"):
                        self.meter.configure(bootstyle="danger", subtext="Test Failed")
                        for i in range(1, len(data_splits)):
                            if i == 0: continue
                            self.insert_text_area("[System Log] Fail step " + str(data_splits[i].strip())+ "\n", redline=True)
                        continue

                    self.insert_text_area(data)
            except Exception as e:
                break

    def insert_text_area(self, data, greenline = False, redline = False):
        self.text_area.text.config(state=tb.NORMAL)
        if redline:
            self.text_area.text.insert(tb.END, data, "redline")
        elif greenline:
            self.text_area.text.insert(tb.END, data, "greenline")
        else:
            self.text_area.text.insert(tb.END, data)
        self.text_area.text.see(tb.END)
        self.text_area.text.config(state=tb.DISABLED)

    def handle_meter_step(self, data):
        # reset value meter when receive "S-1-0" or "E-1-0"
        step = int(data[1])
        if data[0] == "S" and step == 1 and data[2].strip() == "0":
            self.set_meter_value(0)

        if data[0] == "S":
            self.insert_text_area("[System Log] Start Step " + str(step) + "\n")

        if data[0] == "E":    
            if step == 8 :
                self.set_meter_value(100)
                time.sleep(1)
            else:
                value = (100/8) * step
                self.set_meter_value(value)
            self.insert_text_area("[System Log] End Step " + str(step) + "\n")
            self.insert_text_area("_______________________________________________\n")
    
    # Handlers for each step
    # type-step-lognumber-value
    def handle_step_1(self, data):
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] Active relay RY1 and apply 0v for J1-4/J1-6 success!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] Active relay RY1 and apply 0v for J1-4/J1-6 fail!\n", redline=True)
        if data[2] == "2" and data[3] is not None:
            self.set_value_digital(data, "D48 (J13-10)", 3)
        if data[2] == "3" and data[3] is not None:
            self.set_value_digital(data, "D53 (J13-5)", 4)

    def handle_step_2(self, data):
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] Active relay RY6 and Turn on PSW1 success!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] Active relay RY6 and Turn on PSW1 fail!\n", redline=True)
    
    def handle_step_3(self, data):
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] Active relay RY3 and apply 24v for J43/J44 success!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] Active relay RY3 and apply 24v for J43/J44 fail!\n", redline=True)
        if data[2] == "2" and data[3] is not None:
            self.set_value_analog(data, 1, "ADC1 (J13-13)", expect_value=0)
        if data[2] == "3" and data[3] is not None:
            self.set_value_analog(data, 2, "ADC2 (J13-12)", expect_value=0)
        if data[2] == "4" and data[3] is not None:
            self.set_value_analog(data, 4, "ADC4 (J13-6)", expect_value=0)
    
    def handle_step_4(self, data):
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] Active relay RY5 and apply 24v for J41-2/J42-2 success!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] Active relay RY5 and apply 24v for J41-2/J42-2 fail!\n", redline=True)
        if data[2] == "2" and data[3] is not None:
            self.set_value_analog(data, 3, "ADC3 (J13-11)", expect_value=0)

    def handle_step_5(self, data):
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] Active relay RY4 and apply 24v for J37-5/J38-5 success!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] Active relay RY4 and apply 24v for J37-5/J38-5 fail!\n", redline=True)
        if data[2] == "2" and data[3] is not None:
            self.set_value_digital(data, "D2 (J2-1)", 0)
        if data[2] == "3" and data[3] is not None:
            self.set_value_digital(data, "D4 (J2-5)", 2)

    def handle_step_6(self, data):
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] Active relay RY2 and apply 24v for J40-6/J40-4 success!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] Active relay RY2 and apply 24v for J40-6/J40-4 fail!\n", redline=True)
        if data[2] == "2" and data[3] is not None:
            self.set_value_analog(data, 0, "ADC0 (J13-14)", expect_value=0)

    def handle_step_7(self, data):
        R1 = 10000
        R2 = 1200
        Vi = 5
        Vo = Vi * (R2 / (R1 + R2))  # expected voltage ~0.545V
        Vo = round(Vo, 3)
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] Active relay RY7 and apply 0v for J13-8 success!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] Active relay RY7 and apply 0v for J13-8 fail!\n", redline=True)
        if data[2] == "2" and data[3] is not None:
            self.set_value_analog(data, 5, "ADC5 (J13-4)", expect_value=Vo)

    def handle_step_8(self, data):
        if data[2].strip() == "1":
            if data[0] == "P":
                self.insert_text_area("---[Pass] RY4 is active!\n", greenline=True)
            else:
                self.insert_text_area("---[Fail] RY4 is not active!!\n", redline=True)
        if data[2] == "2" and data[3] is not None:
            self.set_value_digital(data, "D3 (J2-4)", 1)

    def set_meter_value(self, value):
        self.meter.configure(amountused=value)

    def set_value_analog(self, data, number, name, expect_value=0):
        # number 0 is A0 (J13-14)
        # number 1 is A1 (J13-13)
        # number 2 is A2 (J13-12)
        # number 3 is A3 (J13-11)
        # number 4 is A4 (J13-6)
        # number 5 is A5 (J13-5)
        value = data[3].strip()
        self.array_entry_boxs[number].set(value)
        R1 = 10000
        R2 = 1200
        real_voltage = float(value) * (R1 + R2) / R2 / 1023 * 5
        real_voltage = round(real_voltage, 3)
        if(data[0] == "P"):
            self.insert_text_area("---[Pass] Value analog " + name + ": " + str(value) + "V (expect : " + str(expect_value) + "V)\n", greenline=True)
            self.array_boxs[number].configure(bootstyle="success")
        else:
            self.insert_text_area("---[Fail] Value analog " + name + ": " + str(value) + "V (expect : " + str(expect_value) + "V)\n", redline=True)
            self.array_boxs[number].configure(bootstyle="danger")

    def set_value_digital(self, data, name, number):
        # number 0 is D2 (J2-1)
        # number 1 is D3 (J2-4)
        # number 2 is D4 (J2-5)
        # number 3 is D48 (J13-10)
        # number 4 is D53 (J13-5)
        value = data[3]
        self.array_entry_Dboxs[number].set(value)
        if data[0] == "P":
            self.insert_text_area("---[Pass] Value digital " + name + ": Low (expect : Low)\n", greenline=True)
            self.array_Dboxs[number].configure(bootstyle="success")
        else:
            self.insert_text_area("---[Fail] Value digital " + name + ": High (expect : Low)\n", redline=True)
            self.array_boxs[number].configure(bootstyle="danger")

    def btn_send_data_method(self):
        if self.serial_port and self.serial_port.is_open:
            msg = self.entry_send.get()
            if msg:
                self.serial_port.write(msg.encode('utf-8')) # write message on text area
                self.entry_send.delete(0, tb.END) # delete textbox send

    def btn_clear_screen_method(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure to clear all screen?")
        if confirm:
            self.text_area.text.config(state=tb.NORMAL) # bật lại chế độ chỉnh sửa
            self.text_area.text.delete('1.0', tb.END) # xóa từ dòng 1, kí tự 0 tới kết thúc
            self.text_area.text.config(state=tb.DISABLED) # tắt chỉnh sửa text area

    def btn_start_test_method(self):
        if self.running and self.serial_port.is_open:
            msg = "start\n"
            self.serial_port.write(msg.encode('utf-8'))
            self.btn_start.configure(state=DISABLED)
            self.btn_auto.configure(state=DISABLED)
            self.btn_run_step.configure(state=ACTIVE)
            self.boxstep.configure(state=ACTIVE)
            self.reset_gui_boxsEntry()
            self.meter.configure(subtext="Starting Test...", bootstyle="info")

    def btn_run_step_method(self):
        if self.running and self.serial_port.is_open:
            msg = "run-" + str(self.step) + "\n"
            self.serial_port.write(msg.encode('utf-8'))
            self.entry_var_boxstep.set(str(self.step))
            self.btn_start.configure(state=DISABLED)
            self.btn_auto.configure(state=DISABLED)

    def spinbox_change_step_method(self):
        self.step = int(self.entry_var_boxstep.get())

    def btn_stop_test_method(self):
        if self.running and self.serial_port.is_open:
            msg = "stop\n"
            self.serial_port.write(msg.encode('utf-8'))
            self.btn_start.configure(state=ACTIVE)
            self.btn_auto.configure(state=ACTIVE)
            self.btn_run_step.configure(state=DISABLED)
            self.boxstep.configure(state=DISABLED)

    def btn_auto_test_method(self):
        if self.running and self.serial_port.is_open:
            msg = "auto\n"
            self.serial_port.write(msg.encode('utf-8'))
            self.btn_start.configure(state=DISABLED)
            self.btn_auto.configure(state=DISABLED)
            self.btn_run_step.configure(state=DISABLED)
            self.boxstep.configure(state=DISABLED)
            self.reset_gui_boxsEntry()
            self.meter.configure(subtext="Starting Auto Test...", bootstyle="info")

    def reset_gui_boxsEntry(self):
        for entry_var in self.array_entry_boxs:
            entry_var.set(0)
        for box in self.array_boxs:
            box.configure(bootstyle="primary")
        for entry_varD in self.array_entry_Dboxs:
            entry_varD.set("***")
        for boxD in self.array_Dboxs:
            boxD.configure(bootstyle="primary")
        self.text_area.text.config(state=tb.NORMAL)
        self.text_area.text.delete('1.0', tb.END)
        self.text_area.text.config(state=tb.DISABLED)

    def on_disconnect(self):
        isExit = False
        count = 0
        if self.running and self.serial_port.is_open:
            msg = "stop\n"
            self.serial_port.write(msg.encode('utf-8'))

    def on_close(self):
        isExit = False
        if self.running and self.serial_port.is_open:
            msg = "stop program\n"
            self.serial_port.write(msg.encode('utf-8'))
        self.master.destroy()

