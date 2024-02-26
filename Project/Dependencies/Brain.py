from gpt4all import GPT4All


class Processing():

    def __init__(self, inQueue, outQueue, emotionList, modelLocation, modApi, gpuEnabled=False):
        """AI GPT System to process user input and generate a response

        Args:
            inQueue (queue): user input queue
            outQueue (queue): response output queue
            emotionList (list): list of emotions
            gpuEnabled (bool, optional): If the AI should use the GPU. Defaults to False.
            modelLocation (string): The location of the GPT model.
        """
        self.emotionNames = []
        for emotion in emotionList:
            self.emotionNames.append(emotion.name)
        
        if gpuEnabled is False:
            self.model = GPT4All(modelLocation)
        else:
            self.model = GPT4All(modelLocation, device='gpu')
        self.scenario = ""
        scenarioFile = open("Project/Dependencies/Scenario.txt", "r")
        for line in scenarioFile:
            if "£Emotions£" in line:
                line = line.replace("£Emotions£", str(self.emotionNames))
            if "£Modules£" in line:
                modulesList = "\n"
                for module in modApi.modules:
                    modulesList += ("\t Module Name: " + module + "\n\t\t Description: " + modApi.modules[module][1] + "\n\t\t Usecase: " + modApi.modules[module][2] + "\n\t\t When it should not be used:" + modApi.modules[module][3] + "\n")
                line = line.replace("£Modules£", str(modulesList))
            self.scenario = self.scenario + line
        print(self.scenario)
        scenarioFile.close()
        self.readQueue = inQueue
        self.writeQueue = outQueue
        self.emotionList = emotionList
        self.gpuEnabled = gpuEnabled
        self.modelLocation = modelLocation

    def ProcessInput(self):
        print("Processing Started")
        """Takes the user input and processes it to find a response

        Args:
            input (string): What the user has said
        """
        with self.model.chat_session(system_prompt=self.scenario):
            while True:
                if self.readQueue.empty() is False:
                    userInput = self.readQueue.get()
                    print("Thinking...")
                    response = self.model.generate(prompt=userInput, temp=1)

                    self.writeQueue.put(response)
                    print("Done Thinking")
