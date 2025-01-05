# Importing necessary libraries and modules
import getpath
from math import *
import statistics

# Define the CIMS class
class CIMS:
    # Class variables to store input, line number, and output
    INPUT = []
    LINE = None
    OUTPUT = []
    SUM = 0
    INDEX = 0
    VAR = {}
    
    # Define the __init__ method
    def __init__(self, input):
        # Initialize the CIMS object with input string and line number
        self.INPUT = input
    
    # Define the equ method for processing mathematical equations
    def equ(self, equation):
        # Function to add values
        def sum(number):
            self.SUM += number
            
            return self.SUM
        
        # Function to find the average value (mean)
        def mean(numbers):
            return statistics.mean(numbers)
        
        # Function to find the middle value (median)
        def med(numbers):                
            return statistics.median(numbers)
        
        # Function to find the value that appears the most (mode)
        def mode(numbers):
            return statistics.mode(numbers)
        
        # Function to use the value of a certain variable
        def var(key):
            if key.startswith("&"):
                key = key.replace("&", "")
                
                if key in self.VAR.keys():
                    return self.VAR[key]
            else:
                return f"Exception [line {self.LINE}]: The variable {key.replace("&", "")} is undefined"
        
        # Function to validate equations
        def is_valid(equation):
            # List of valid mathematical operators and functions
            EQU = ["+", "-", "*", "/", "%", "**", "abs", "round", "pow", "sin", "cos", "tan", 
                   "asin", "acos", "atan", "sqrt", "cbrt", "log", "exp", "comb", "fact", 
                   "pi", "euler", "tau", "phi", "sum", "var", "mean", "med", "mode"]
            
            # Replace parentheses with spaces and split the equation into tokens
            tokens = equation.replace("{", " ").replace("}", " ").replace("(", " ").replace(")", " ").replace("\"", "").replace("&", "").replace("IDX", "self.INDEX").split(" ")
            tokens = list(filter(None, tokens))  # Remove any empty tokens from the list
            contain = False
            
            # Check if any of the tokens match the valid operators/functions
            for index in range(len(tokens)):
                try:
                    for operator in EQU:
                        # If the token matches an operator or is a valid integer/float, set contain to True
                        if operator == tokens[index]:
                            contain = True
                        elif tokens[index] in self.VAR:                            
                            contain = True
                        elif isinstance(int(tokens[index]), int):
                            contain = True
                        elif isinstance(float(tokens[index]), float):
                            contain = True
                        else:
                            contain = False
                except Exception:
                    # Continue to the next token if an exception occurs
                    continue
            
            return contain
        
        # Evaluate the mathematical equation provided as a string
        try:
            if is_valid(equation):
                equation = equation.replace("IDX", "self.INDEX").replace("{", "(\"").replace("}", "\")")
                
                if equation == "phi":
                    result = str(1.61803398875)  # Return the value of the golden ratio (phi)
                elif equation == "euler":
                    result = str(e)  # Return the value of Euler's number (e)
                elif equation.startswith("fact"):
                    # Evaluate the factorial function if present
                    result = str(eval(equation.replace("fact", "factorial")))
                elif equation.startswith("sum") or equation.startswith("var"):
                    # Evaluate the sum or var function
                    result = str(eval(equation))
                elif equation.startswith("mean") or equation.startswith("med") or equation.startswith("mode"):
                    # Evaluate the mean, med, or mode function
                    result = str(eval(equation))
                else:
                    # Evaluate the mathematical equation using eval
                    result = str(eval(equation))
            else:
                return f"Exception [line {self.LINE}]: The argument '{equation.replace("\"", "")}' is undefined,\ntype '$command help' to read the manual"
        except Exception as e:
            print(e)
            # Handle exceptions if they occur
            return f"Exception [line {self.LINE}]: The argument '{equation.replace("\"", "")}' is undefined,\ntype '$command help' to read the manual"
        
        return result

    # Define a run method to run the CIMS interpreter
    def run(self):
        self.OUTPUT = []
        
        # Define a method as a container for its syntax
        def container(scripts):
            # Split the scripts by semicolon
            scripts = scripts.split(";")
            
            for script in scripts:
                # Strip whitespace and process each script
                syntax(script.strip())
        
        # Function to change data type        
        def mutation(type, value):
            if type == "int":  # change the int data type to a usable integer data type
                return int(float(value))
            elif type == "float":  # change the float data type to a usable float data type
                return float(value)
            elif type == "arrint":  # change the arrint data type to a usable integer list data type
                array = value.split(", ")
                
                return [int(float(item)) for item in array]
            elif type == "arrfloat":  # change the arrfloat data type to a usable float list data type
                array = value.split(", ")
                
                return [float(item) for item in array]
            elif type == "arrstr":  # change the arrstr data type to a usable string list data type
                array = value.split(", ")
                
                return [item.replace("\"", "") for item in array]
            else:
                # Handle invalid data type
                self.OUTPUT.append(f"Exception [line: {self.LINE}]: Data type {type} is invalid")
        
        try:
            # Iterate over each line in the input
            for index, line in enumerate(self.INPUT.splitlines()):
                self.LINE = index + 1

                # Define a method to execute the syntax
                def syntax(line):
                    # Process the input string and execute corresponding actions
                    if line.startswith("$script"):
                        # If input is a script command, process the script
                        script = line.replace("$script", "").strip()
                    
                        if script.startswith("equ(") and script.endswith(")"):
                            # Evaluate mathematical equation
                            self.OUTPUT.append(self.equ(script[4:-1]))
                        elif script.startswith("\"") and script.endswith("\""):
                            if script[0] != "\"" or script[-1] != "\"":
                                # Handle punctuation errors
                                self.OUTPUT.append(f"Exception [line {self.LINE}]: {line}\nPunctuation error, (\"...\") is not used")
                            else:
                                # Handle string literals
                                self.OUTPUT.append(script[1:-1])
                        elif script.startswith("ctr(") and script.endswith(")"):
                            # If input is a container command, process the container
                            script = line[7:].strip()
                            script = script[4:-1]

                            # Execute the scripts
                            container(script)
                        elif script.startswith("form(") and script.endswith(")"):
                            # If input is a format command, process the format
                            script = script[5:-1]

                            if script[0] != "\"" or script[-1] != "\"":
                                # Handle punctuation errors
                                self.OUTPUT.append(f"Exception [line {self.LINE}]: {line}\nPunctuation error, (\"...\") is not used")
                            else:
                                script = script[1:-1].replace("%IDX", f"{self.INDEX}").replace("%SUM", f"{self.SUM}")
                                script = script.replace("%VARK", f"{list(self.VAR.keys())}").replace("%VARV", f"{list(self.VAR.values())}")
                                script = script.replace("%VAR", f"{self.VAR}")
                                
                                self.OUTPUT.append(script)
                        else:
                            # Handle unknown script errors
                            self.OUTPUT.append(f"Exception [line {self.LINE}]: {line}\nUnknown script error, type '$command help' to read the manual")
                    elif line.startswith("$ignore") or line == "":
                        # Ignore the input if it starts with $ignore or is empty
                        try: 
                            index -= 1
                            
                            pass
                        except Exception:
                            pass
                    elif line.startswith("$command"):
                        # Execute command if input starts with $command
                        command = line.replace("$command", "").strip()
                        
                        if command == "help":
                            # Provide help content from a binary file
                            with open(getpath.base("bin/help.bin"), "rb") as file:
                                content = file.read().decode("utf-8")
                                
                                self.OUTPUT.append(content)
                        elif command == "clearall":
                            # Clear all output
                            self.OUTPUT = self.OUTPUT[(len(self.OUTPUT) - 1):]
                        elif "popvar" in command:
                            command = command.replace("popvar", "").strip()
                            
                            del self.VAR[command]
                        elif command == "resetsum":
                            # Reset the SUM value
                            self.SUM = 0
                        elif command == "resetidx":
                            # Reset the INDEX value
                            self.INDEX = 0
                        elif command == "resetvar":
                            # Reset the VAR value
                            self.VAR = {}
                        else:
                            # Handle unrecognized command error
                            self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line}\nUnrecognized command error, type '$command help' to read the manual")
                    elif line.startswith("$var"):
                        # Execute variable creation if it starts with $var
                        script = line.replace("$var", "").strip()
                        script = script.split(" ")
                        
                        if script[2] == "int" and isinstance(script[0], str) and isinstance(int(float(script[3])), int) and len(script) == 4:
                            # Processing if the variable data type is int
                            self.VAR.update({script[0] : mutation(script[2], script[3])})
                        elif script[2] == "float" and isinstance(script[0], str) and isinstance(float(script[3]), float) and len(script) == 4:
                            # Processing if the variable data type is float
                            self.VAR.update({script[0] : mutation(script[2], script[3])})
                        elif script[2] == "str" and len(script) >= 4:
                            # Processing if the variable data type is str
                            string = " ".join(script[3:]).strip()
                            
                            if string.startswith("\"") and string.endswith("\""):
                                string = string.replace("\"", "")
                                
                                self.VAR.update({script[0] : string})
                            else:
                                # Handle punctuation errors
                                self.OUTPUT.append(f"Exception [line {self.LINE}]: {line}\nPunctuation error, (\"...\") is not used")
                        elif script[2].startswith("arr") and len(script) >= 4:
                            # Processing if the variable data type is arr (arrint, arrfloat, arrstr)
                            string = " ".join(script[3:]).strip()
                            
                            if string.startswith("[") and string.endswith("]"):
                                string = string.replace("[", "").replace("]", "")
                                
                                self.VAR.update({script[0] : mutation(script[2], string)})
                        else:
                            # Handle invalid data type
                            self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line}\nInvalid data type, type '$command help' to read the manual")
                    else:
                        # Handle unknown syntax errors
                        self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line.replace("&", "").replace("{", "").replace("}", "").replace("self.", "")}\nUnknown syntax error, type '$command help' to read the manual")
                
                if line.startswith("$loop"):
                    # Parse the loop syntax
                    loop_parts = line.split(" (")
                    loop_command = loop_parts[0].strip()
                    syntax_parts = loop_parts[1].split(") ")
                    syntax_command = syntax_parts[0].strip()
                    condition = syntax_parts[1].strip()
                    
                    if loop_command == "$loop" and condition.endswith("times"):
                        # Get the number of times to loop
                        condition = condition.split(" ")
                        
                        for index in range(int(condition[0])):
                            # Execute the syntax command within the loop
                            container(syntax_command)
                            
                            self.INDEX += 1
                    elif loop_command == "$loop" and (condition.startswith("until(") and condition.endswith(")")):
                        if ("equ(sum(" in syntax_command) or ("equ(var{" in syntax_command):
                            # Get the condition of the loop
                            condition = condition[5:].strip().replace("SUM", "self.SUM").replace("IDX", "self.INDEX")
                            
                            while (True):
                                if eval(condition):
                                    break
                                else:
                                    # Execute the syntax command within the loop
                                    container(syntax_command)
                                    
                                    self.INDEX += 1
                        else:
                            # Handle unknown script errors
                            self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line.replace("&", "").replace("{", "").replace("}", "").replace("self.", "")}\nUnknown script error, type '$command help' to read the manual")
                    else:
                        # Handle unknown script errors
                        self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line.replace("&", "").replace("{", "").replace("}", "").replace("self.", "")}\nUnknown script error, type '$command help' to read the manual")
                else:
                    # Process the line if it's not a loop command
                    syntax(line)
        except Exception:
            # Handle unknown script errors
            self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line.replace("&", "").replace("{", "").replace("}", "").replace("self.", "")}\nUnknown script error, type '$command help' to read the manual")
    
    # Define a call method to return the output value
    def call(self):
        # Return the output of the executed script or command
        return "\n".join(self.OUTPUT)
