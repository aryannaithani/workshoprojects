import tkinter as tk
from tkinter import ttk, scrolledtext
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("800x500")
        self.root.minsize(600, 400)
        
        # Variables
        self.current_input = ""
        self.history = []
        self.is_dark_mode = False
        
        # Define colors for themes
        self.light_theme = {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "button_bg": "#e1e1e1",
            "button_fg": "#000000",
            "display_bg": "#ffffff",
            "display_fg": "#000000",
            "op_button_bg": "#d0d0ff",
            "sci_button_bg": "#ffe0d0",
            "highlight_bg": "#90caf9"
        }
        
        self.dark_theme = {
            "bg": "#2d2d2d",
            "fg": "#ffffff",
            "button_bg": "#3d3d3d",
            "button_fg": "#ffffff",
            "display_bg": "#1e1e1e",
            "display_fg": "#ffffff",
            "op_button_bg": "#4040aa",
            "sci_button_bg": "#aa4040",
            "highlight_bg": "#0d47a1"
        }
        
        self.current_theme = self.light_theme
        
        # Create main frames
        self.create_frames()
        self.create_display()
        self.create_buttons()
        self.create_history_panel()
        self.create_theme_toggle()
        
        # Set up key bindings
        self.setup_keyboard_bindings()
    
    def create_frames(self):
        # Main container with two columns
        self.main_container = tk.Frame(self.root, bg=self.current_theme["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for calculator
        self.calculator_frame = tk.Frame(self.main_container, bg=self.current_theme["bg"])
        self.calculator_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right frame for history
        self.history_frame = tk.Frame(self.main_container, bg=self.current_theme["bg"], width=200)
        self.history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Display frame
        self.display_frame = tk.Frame(self.calculator_frame, bg=self.current_theme["bg"])
        self.display_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.calculator_frame, bg=self.current_theme["bg"])
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_display(self):
        # Input display
        self.display = tk.Entry(
            self.display_frame, 
            font=("Arial", 24),
            bd=10,
            justify=tk.RIGHT,
            bg=self.current_theme["display_bg"],
            fg=self.current_theme["display_fg"]
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.insert(0, "0")
        self.display.config(state="readonly")
    
    def create_buttons(self):
        # Create grid for calculator buttons
        self.buttons_frame.columnconfigure(tuple(range(5)), weight=1)
        self.buttons_frame.rowconfigure(tuple(range(7)), weight=1)
        
        # Scientific buttons (first row)
        sci_buttons = [
            ("sin", lambda: self.add_scientific_function("sin(")),
            ("cos", lambda: self.add_scientific_function("cos(")),
            ("tan", lambda: self.add_scientific_function("tan(")),
            ("log", lambda: self.add_scientific_function("log(")),
            ("ln", lambda: self.add_scientific_function("ln("))
        ]
        
        for col, (text, command) in enumerate(sci_buttons):
            self.create_button(text, command, 0, col, is_science=True)
        
        # More scientific buttons (second row)
        sci_buttons2 = [
            ("√", lambda: self.add_scientific_function("sqrt(")),
            ("^", lambda: self.add_operator("^")),
            ("π", lambda: self.add_constant(math.pi)),
            ("e", lambda: self.add_constant(math.e)),
            ("!", lambda: self.add_operator("!"))
        ]
        
        for col, (text, command) in enumerate(sci_buttons2):
            self.create_button(text, command, 1, col, is_science=True)
        
        # Parentheses and clear buttons (third row)
        special_buttons = [
            ("(", lambda: self.add_to_input("(")),
            (")", lambda: self.add_to_input(")")),
            ("C", self.clear_last),
            ("AC", self.clear_all),
            ("÷", lambda: self.add_operator("/"))
        ]
        
        for col, (text, command) in enumerate(special_buttons):
            is_op = text in "÷"
            self.create_button(text, command, 2, col, is_operation=is_op)
        
        # Numbers and operations
        buttons = [
            ("7", lambda: self.add_to_input("7")),
            ("8", lambda: self.add_to_input("8")),
            ("9", lambda: self.add_to_input("9")),
            ("×", lambda: self.add_operator("*")),
            
            ("4", lambda: self.add_to_input("4")),
            ("5", lambda: self.add_to_input("5")),
            ("6", lambda: self.add_to_input("6")),
            ("-", lambda: self.add_operator("-")),
            
            ("1", lambda: self.add_to_input("1")),
            ("2", lambda: self.add_to_input("2")),
            ("3", lambda: self.add_to_input("3")),
            ("+", lambda: self.add_operator("+"))
        ]
        
        row, col = 3, 0
        for text, command in buttons:
            is_op = text in "×-+"
            self.create_button(text, command, row, col, is_operation=is_op)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Last row
        self.create_button("0", lambda: self.add_to_input("0"), 6, 0, colspan=2)
        self.create_button(".", lambda: self.add_to_input("."), 6, 2)
        self.create_button("=", self.calculate, 6, 3, is_operation=True)
        
        # Put division and multiplication in column 4
        self.create_button("DEL", self.delete_last, 3, 4)
        self.create_button("1/x", lambda: self.add_scientific_function("1/("), 4, 4, is_science=True)
        self.create_button("x²", lambda: self.add_scientific_function("sqr("), 5, 4, is_science=True)
        self.create_button("Ans", self.use_last_answer, 6, 4)
    
    def create_button(self, text, command, row, column, colspan=1, rowspan=1, is_operation=False, is_science=False):
        if is_operation:
            bg_color = self.current_theme["op_button_bg"]
        elif is_science:
            bg_color = self.current_theme["sci_button_bg"]
        else:
            bg_color = self.current_theme["button_bg"]
            
        button = tk.Button(
            self.buttons_frame,
            text=text,
            font=("Arial", 12, "bold"),
            bd=3,
            relief=tk.RAISED,
            bg=bg_color,
            fg=self.current_theme["button_fg"],
            command=command
        )
        button.grid(row=row, column=column, columnspan=colspan, rowspan=rowspan, 
                   sticky="nsew", padx=2, pady=2)
    
    def create_history_panel(self):
        # Add a label
        history_label = tk.Label(
            self.history_frame,
            text="Calculation History",
            font=("Arial", 12, "bold"),
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        history_label.pack(pady=(0, 5))
        
        # Create scrolled text widget for history
        self.history_display = scrolledtext.ScrolledText(
            self.history_frame,
            width=25,
            height=15,
            font=("Arial", 10),
            bg=self.current_theme["display_bg"],
            fg=self.current_theme["display_fg"],
            wrap=tk.WORD
        )
        self.history_display.pack(fill=tk.BOTH, expand=True)
        self.history_display.config(state=tk.DISABLED)
        
        # Bind click event on history items
        self.history_display.tag_config("clickable", foreground="blue", underline=1)
        self.history_display.bind("<Button-1>", self.history_clicked)
    
    def create_theme_toggle(self):
        # Create a frame for the toggle
        toggle_frame = tk.Frame(self.calculator_frame, bg=self.current_theme["bg"])
        toggle_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Add a label
        theme_label = tk.Label(
            toggle_frame,
            text="Theme:",
            font=("Arial", 10),
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        theme_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create the toggle button
        self.theme_button = tk.Button(
            toggle_frame,
            text="Switch to Dark Mode",
            font=("Arial", 10),
            command=self.toggle_theme,
            bg=self.current_theme["button_bg"],
            fg=self.current_theme["button_fg"]
        )
        self.theme_button.pack(side=tk.LEFT)
    
    def setup_keyboard_bindings(self):
        # Number keys
        for num in range(10):
            self.root.bind(str(num), lambda event, digit=num: self.add_to_input(str(digit)))
        
        # Operation keys
        self.root.bind("+", lambda event: self.add_operator("+"))
        self.root.bind("-", lambda event: self.add_operator("-"))
        self.root.bind("*", lambda event: self.add_operator("*"))
        self.root.bind("/", lambda event: self.add_operator("/"))
        self.root.bind("^", lambda event: self.add_operator("^"))
        self.root.bind(".", lambda event: self.add_to_input("."))
        
        # Parentheses
        self.root.bind("(", lambda event: self.add_to_input("("))
        self.root.bind(")", lambda event: self.add_to_input(")"))
        
        # Calculate
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<KP_Enter>", lambda event: self.calculate())
        
        # Clear and delete
        self.root.bind("<BackSpace>", lambda event: self.delete_last())
        self.root.bind("<Delete>", lambda event: self.clear_all())
    
    def add_to_input(self, char):
        if self.current_input == "0" and char in "0123456789":
            self.current_input = char
        else:
            self.current_input += char
        self.update_display()
    
    def add_operator(self, op):
        if self.current_input and self.current_input[-1] not in "+-*/^(":
            self.current_input += op
            self.update_display()
    
    def add_scientific_function(self, func):
        self.current_input += func
        self.update_display()
    
    def add_constant(self, value):
        if self.current_input and self.current_input[-1].isdigit():
            self.current_input += "*" + str(value)
        else:
            self.current_input += str(value)
        self.update_display()
    
    def clear_last(self):
        self.current_input = ""
        self.update_display()
    
    def clear_all(self):
        self.clear_last()
    
    def delete_last(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
            self.update_display()
    
    def use_last_answer(self):
        if len(self.history) > 0:
            last_result = self.history[-1].split(" = ")[1]
            if self.current_input and self.current_input[-1].isdigit():
                self.current_input += "*" + last_result
            else:
                self.current_input += last_result
            self.update_display()
    
    def update_display(self):
        self.display.config(state=tk.NORMAL)
        self.display.delete(0, tk.END)
        display_text = self.current_input if self.current_input else "0"
        self.display.insert(0, display_text)
        self.display.config(state="readonly")
    
    def calculate(self):
        if not self.current_input:
            return
        
        # Store the expression
        expression = self.current_input
        
        try:
            # Handle special functions and operations
            expr = expression.replace("^", "**")
            expr = expr.replace("sqrt(", "math.sqrt(")
            expr = expr.replace("sin(", "math.sin(")
            expr = expr.replace("cos(", "math.cos(")
            expr = expr.replace("tan(", "math.tan(")
            expr = expr.replace("log(", "math.log10(")
            expr = expr.replace("ln(", "math.log(")
            expr = expr.replace("sqr(", "((")
            expr = expr.replace("π", str(math.pi))
            expr = expr.replace("e", str(math.e))
            
            # Handle factorial
            if "!" in expr:
                parts = expr.split("!")
                num_str = parts[0]
                # Find the last number or expression
                i = len(num_str) - 1
                while i >= 0 and (num_str[i].isdigit() or num_str[i] == '.'):
                    i -= 1
                i += 1
                num = float(num_str[i:])
                if num.is_integer() and num >= 0:
                    result = math.factorial(int(num))
                    expr = num_str[:i] + str(result) + "".join(parts[1:])
            
            # Calculate the result
            result = eval(expr)
            
            # Format the result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Update display with result
            self.current_input = str(result)
            self.update_display()
            
            # Add to history
            history_entry = f"{expression} = {result}"
            self.history.append(history_entry)
            
            # Update history display
            self.update_history_display()
            
        except Exception as e:
            self.current_input = "Error"
            self.update_display()
    
    def update_history_display(self):
        self.history_display.config(state=tk.NORMAL)
        self.history_display.delete(1.0, tk.END)
        
        # Limit history to the most recent 20 entries
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        for entry in self.history:
            self.history_display.insert(tk.END, entry + "\n", "clickable")
        
        self.history_display.config(state=tk.DISABLED)
        self.history_display.see(tk.END)  # Scroll to the bottom
    
    def history_clicked(self, event):
        # Get the index of the click
        index = self.history_display.index(f"@{event.x},{event.y}")
        line = int(float(index))
        
        # Find the corresponding history entry if it exists
        if 0 <= line - 1 < len(self.history):
            entry = self.history[line - 1]
            parts = entry.split(" = ")
            if len(parts) == 2:
                expression = parts[0]
                self.current_input = expression
                self.update_display()
    
    def toggle_theme(self):
        # Switch between light and dark mode
        self.is_dark_mode = not self.is_dark_mode
        self.current_theme = self.dark_theme if self.is_dark_mode else self.light_theme
        
        # Update button text
        if self.is_dark_mode:
            self.theme_button.config(text="Switch to Light Mode")
        else:
            self.theme_button.config(text="Switch to Dark Mode")
        
        # Update all UI elements with the new theme
        self.update_theme()
    
    def update_theme(self):
        # Update main container
        self.main_container.config(bg=self.current_theme["bg"])
        self.calculator_frame.config(bg=self.current_theme["bg"])
        self.history_frame.config(bg=self.current_theme["bg"])
        self.display_frame.config(bg=self.current_theme["bg"])
        self.buttons_frame.config(bg=self.current_theme["bg"])
        
        # Update display
        self.display.config(
            bg=self.current_theme["display_bg"],
            fg=self.current_theme["display_fg"]
        )
        
        # Update buttons
        for widget in self.buttons_frame.winfo_children():
            if isinstance(widget, tk.Button):
                # Determine button type (operation, science, or normal)
                text = widget["text"]
                if text in "+-×÷=":
                    bg_color = self.current_theme["op_button_bg"]
                elif text in ["sin", "cos", "tan", "log", "ln", "√", "^", "π", "e", "!", "x²", "1/x"]:
                    bg_color = self.current_theme["sci_button_bg"]
                else:
                    bg_color = self.current_theme["button_bg"]
                
                widget.config(
                    bg=bg_color,
                    fg=self.current_theme["button_fg"]
                )
        
        # Update history panel
        for widget in self.history_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(
                    bg=self.current_theme["bg"],
                    fg=self.current_theme["fg"]
                )
        
        self.history_display.config(
            bg=self.current_theme["display_bg"],
            fg=self.current_theme["display_fg"]
        )
        
        # Update theme toggle button
        self.theme_button.config(
            bg=self.current_theme["button_bg"],
            fg=self.current_theme["button_fg"]
        )

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()