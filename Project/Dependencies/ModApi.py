import os


class ModApi():

    def __init__(self):
        self.modules = {}
        self.load_modules()

    def load_modules(self):
        for item in os.listdir("Project/Dependencies/Modules"):
            if item.endswith(".py"):
                print(item)
                module = __import__(f"Dependencies.Modules.{item[:-3]}", fromlist=['Run'])
                runClass = getattr(module, "Run")
                self.modules[item[:-3]] = [None, None, None]
                self.modules[item[:-3]][0] = runClass()
                self.modules[item[:-3]][1] = self.modules[item[:-3]][0].ReturnDescription()
                self.modules[item[:-3]][2] = self.modules[item[:-3]][0].ReturnScenario()

    def get_module(self, name):
        return self.modules[name][0]
    
    def RunResponse(self, name, invars):
        if len(invars) == 1:
            output = self.modules[name][0].ReturnResponse(invars[0])
        elif len(invars) == 2:
            output = self.modules[name][0].ReturnResponse(invars[0], invars[1])
        elif len(invars) == 3:
            output = self.modules[name][0].ReturnResponse(invars[0], invars[1], invars[2])
        elif len(invars) == 4:
            output = self.modules[name][0].ReturnResponse(invars[0], invars[1], invars[2], invars[3])
        elif len(invars) == 5:
            output = self.modules[name][0].ReturnResponse(invars[0], invars[1], invars[2], invars[3], invars[4])
        elif len(invars) == 6:
            output = self.modules[name][0].ReturnResponse(invars[0], invars[1], invars[2], invars[3], invars[4], invars[5])
        return "system response" + str(output)


if __name__ == "__main__":
    api = ModApi()
    print(api.modules)
    print(api.modules["Example"][1])
    print(api.modules["Example"][0].ReturnResponse(5))

