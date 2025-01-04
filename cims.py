# Importing necessary libraries and modules
import getpath
from math import *

# Define the CIMS class
class CIMS:
    # Class variables to store input, line number, and output
    INPUT = []
    LINE = None
    OUTPUT = []
    SUM = 0
    
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
        
        # Function to validate equations
        def is_valid(equation):
            # List of valid mathematical operators and functions
            EQU = ["+", "-", "*", "/", "%", "**", "abs", "round", "pow", "sin", "cos", "tan", 
                   "asin", "acos", "atan", "sqrt", "cbrt", "log", "exp", "comb", "fact", 
                   "pi", "euler", "tau", "phi", "sum"]
            
            # Replace parentheses with spaces and split the equation into tokens
            tokens = equation.replace("(", " ").replace(")", " ").split(" ")
            tokens = list(filter(None, tokens))  # Remove any empty tokens from the list
            contain = False
            
            # Check if any of the tokens match the valid operators/functions
            for index in range(len(tokens)):
                try:
                    for operator in EQU:
                        # If the token matches an operator or is a valid integer/float, set contain to True
                        if operator == tokens[index]:
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
                if equation == "phi":
                    result = str(1.61803398875)  # Return the value of the golden ratio (phi)
                elif equation == "euler":
                    result = str(e)  # Return the value of Euler's number (e)
                elif equation.startswith("fact"):
                    # Evaluate the factorial function if present
                    result = str(eval(equation.replace("fact", "factorial")))
                elif equation.startswith("sum"):
                    result = str(eval(equation))
                else:
                    # Evaluate the mathematical equation using eval
                    result = str(eval(equation))
            else:
                return f"Exception [line {self.LINE}]: The argument '{equation}' is undefined\n"
        except Exception:
            # Handle exceptions if they occur
            return f"Exception [line {self.LINE}]: The argument '{equation}' is undefined\n"
        
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
                        elif (script.startswith("\"") or script.startswith("'")) and (script.endswith("\"") or script.endswith("'")):
                            # Handle string literals
                            self.OUTPUT.append(script[1:-1])
                        elif script.startswith("ctr(") and script.endswith(")"):
                            # If input is a container command, process the container
                            script = line[7:].strip()
                            script = script[4:-1]

                            # Execute the scripts
                            container(script)
                        else:
                            # Handle unknown script errors
                            self.OUTPUT.append(f"Exception [line {self.LINE}]: Unknown script error, type '$command help' to read the manual\n")
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
                        elif command == "resetsum":
                            # Reset the SUM value
                            self.SUM = 0
                        else:
                            # Handle unrecognized command error
                            self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line}\nUnrecognized command error, type '$command help' to read the manual\n")
                    else:
                        # Handle unknown syntax errors
                        self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line}\nUnknown syntax error, type '$command help' to read the manual\n")
                
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
                    elif loop_command == "$loop" and (condition.startswith("until(") and condition.endswith(")")):
                        if "equ(sum(" in syntax_command:
                            # Get the condition of the loop
                            condition = condition[5:].strip().replace("sum", "sum".upper()).replace("SUM", "self.SUM")
                            
                            while (True):
                                if eval(condition):
                                    break
                                else:
                                    # Execute the syntax command within the loop
                                    container(syntax_command)
                        else:
                            # Handle unknown script errors
                            self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line}\nUnknown script error, type '$command help' to read the manual\n")
                    else:
                        # Handle unknown script errors
                        self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line}\nUnknown script error, type '$command help' to read the manual\n")
                else:
                    # Process the line if it's not a loop command
                    syntax(line)
        except Exception:
            # Handle unknown script errors
            self.OUTPUT.append(f"Exception [line: {self.LINE}]: {line}\nUnknown script error, type '$command help' to read the manual\n")
    
    # Define a call method to return the output value
    def call(self):
        # Return the output of the executed script or command
        return "\n".join(self.OUTPUT)
