
# This is your code, you can name it what you want as long as you change the Run class
# to use the name you have chosen
class FunctionalityClass:
    def __init__(self):
        pass

    # This is the function that will be called when the module is used, you can name it
    # what you want, just make sure to change the Run class to use the name you have chosen
    # you can also have multiple functions in the class, just as long as you eventually
    # return a value from the ReturnResponse function
    def example_function(self, data):
        data = int(data)
        data += 1
        print("Example Function has been called, returning: " + str(data))
        return data


# The run class is the class that will be called when the module is loaded, it must be 
# called Run and have the following functions:
    #
    # ReturnDescription: This function should return a string that describes what the module
    # does and what inputs and outputs it has
    #
    # ReturnFunctionality: This function should return the functionality class that contains
    # the functions that will be called when the module is used
    #
    # ReturnResponse: This function should take the inputs that the module needs and return the
    # output that the module produces, this can technically do anything, you dont even need
    # to use the functionality class, but it is recommended. I also recommend that you put
    # notes to PEA in the return response;
    # for example: "this is the weather in truro {weather} returned from the weather module"
    # This is so that PEA can understand what the response is and where it came from, it
    # sometimes needs some help, bless it.
class Run():

    def __init__(self):
        print("Example has been loaded")
        self.functionality = FunctionalityClass()
        
    def ReturnDescription(self):
        return "This is an example module, it doesn't do anything useful, it has a single int input"
    
    def ReturnScenario(self):
        response = "This module should be used when the user asks something similar to:"
        response += "\n\t\t- What is 5 + 1?"
        response += "\n\t\t- Can you run the example function?"
        return response
    
    def ReturnFunctionality(self):
        return self.functionality
    
    def ReturnResponse(self, value):
        functionResponse = self.functionality.example_function(value)
        peaNote = "PEA here is the response from the example funtion: "
        response = peaNote + str(functionResponse)
        return response

