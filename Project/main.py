from Dependencies.ConfigWrapper import Config
from Dependencies.Mouth import TTS
from Dependencies.Face import FaceDisplay
from Dependencies.Ears import SoundDevice
from Dependencies.Brain import Processing
from Dependencies.ModApi import ModApi
from queue import Queue
from threading import Thread
import pynput.keyboard
import sys
import time

# This line will complain which is why its quarantined, basically ALSA throws a
# warning when the speech_recognition library is used, it doesn't affect the
# program but it's annoying, but importing sounddevice will fix this as
# sounddevice handles the ALSA like the little baby it is and tells it to shut up
import sounddevice as sd


# Function to be called when a key is pressed, used to exit the program when escape is pressed
def OnPress(key):
    """Function to be called when a key is pressed, used to exit the program when escape is pressed

    Args:
        key (pynput.keyboard.Key): The key that was pressed
    """
    if key == pynput.keyboard.Key.esc:
        print("Exiting...")
        exitQueue.put(True)


# Function to check if the user is speaking, run in a separate thread to the main program
def speakingCheckThread(speakingThreshold=70):
    """Function to check if the user is speaking, run in a separate thread to the main program

    Args:
        speakingThreshold (int, optional): The sound level threshold for the user speaking. Defaults to 70.
    """
    lastSpeaking = True

    # Sound Device Setup
    soundDevice = SoundDevice()

    while True:

        soundLevelOutput = soundDevice.SoundLevel()
        # print(soundLevelOutput)

        if lastSpeaking is False and soundLevelOutput > 68:
            lastSpeaking = True
            emotionQueue.put([faceDisplay.currentEmotion, True])
            sleepQueue.put([False, False])

        elif lastSpeaking is True and soundLevelOutput < 68:
            lastSpeaking = False
            emotionQueue.put([faceDisplay.currentEmotion, False])
            sleepQueue.put([True, True])


# Function to check if the user is inactive, run in a separate thread to the main program
def sleepCheckThread(cooldown=30):
    """Makes the robot go to sleep if the user is inactive for a certain amount of time, just looks kinda cute

    Args:
        cooldown (int, optional): The amount of time the user must be inactive for before the robot goes to sleep. Defaults to 30.
    """
    startTime = time.time()
    while True:
        # Sleep queue is a list with two bools in it:
        # The first is if any activity has been detected in which case it restarts the timer
        # The second is if the user can sleep
        if sleepQueue.empty() is False:
            sleepData = sleepQueue.get()

            if sleepData[0] is True:
                startTime = time.time()

            if sleepData[1] is False:
                canSleep = False
            elif sleepData[1] is True:
                canSleep = True

        else:
            if time.time() - startTime > 30 and canSleep is True:
                emotionQueue.put(["asleep", False])
                sleepQueue.put([False, False])
        
        # Sleep for a second to reduce CPU usage
        time.sleep(1)


# Load config settings
config = Config("Project/Dependencies/config.ini")
affectiveMode = config.get_boolean("General", "affectiveMode")
speak = config.get_boolean("TTS", "speak")
sleep = config.get_boolean("Sleep", "enabled")
stt = config.get_boolean("STT", "enabled")
cooldown = config.get_int("Sleep", "cooldown")
speakingThreshold = config.get_int("Face", "speakingThreshold")
gpuEnabled = config.get_boolean("AI", "gpuEnabled")
modelLocation = config.get("AI", "modelLocation")
xOffset = config.get_int("Face", "xOffset")
yOffset = config.get_int("Face", "yOffset")

# Queue setup for talking between threads
exitQueue = Queue()
speechTextQueue = Queue()
emotionQueue = Queue()
sleepQueue = Queue()
brainInputQueue = Queue()
brainOutputQueue = Queue()

# Devices Setup
tts = TTS(speak, affectiveMode, ".")
faceDisplay = FaceDisplay("Project/Dependencies/Faces", affectiveMode, xOffset, yOffset)
soundDeviceMain = SoundDevice(speechTextQueue, sleepQueue)
modApi = ModApi()
processor = Processing(brainInputQueue, brainOutputQueue, faceDisplay.emotions, modelLocation, modApi, gpuEnabled)


# The exit functionality including the listener
listener = pynput.keyboard.Listener(on_press=OnPress)
listener.start()

# Brain Setup
processorThread = Thread(target=processor.ProcessInput)
processorThread.start()

# If speech to text is enabled, create a thread to check for speech
if stt is True:
    print("STT Enabled")
    speechTextThread = Thread(target=soundDeviceMain.SpeechToText)
    speechTextThread.start()

# If speech to text is disabled, create a thread to check for console input
else:
    print("STT Disabled")
    consoleListenThread = Thread(target=soundDeviceMain.ConsoleListen)
    consoleListenThread.start()

# If affective mode is enabled, set the face to use emotion and setup the 
# emotion queue
if affectiveMode is True:
    faceDisplay.UpdateFace("normal", False)

    # Create a queue for communication between threads
    emotionQueue.put(["normal", False])

# If speaking is enabled, create a thread to check if the robot is speaking
if speak is True:
    # Create a thread to check if the user is speaking
    speakingThread = Thread(target=speakingCheckThread, args=())
    speakingThread.start()

# If sleep is enabled, create a thread to check if the user is inactive
if sleep is True:
    # Create a thread to check if the user is inactive
    sleepThread = Thread(target=sleepCheckThread, args=(cooldown,))
    sleepQueue.put([True, True])
    sleepThread.start()

# Main loop
while True:

    if speechTextQueue.empty() is False:
        userInput = speechTextQueue.get()
        emotionQueue.put(["thinking", False])
        brainInputQueue.put(userInput)

    if brainOutputQueue.empty() is False:
        response = brainOutputQueue.get()
        print("PEA: " + response)

        if "$system$" in response:
            response = response.split("\n")[0]
            response = response.replace("$system$", "")
            moduleName = ""
            for mod in modApi.modules:
                if mod in response:
                    moduleName = mod
            if moduleName == "":
                print("Module not found")
                brainInputQueue.put("System could not find a module with that name, please try again with a different module name, and remember to use the format: '$system$ *modulename* ~var1 ~var2 ~var3'.")
            else:
                variableSplit = response.split("~")
                invars = []
                variableSplit.pop(0)
                for var in variableSplit:
                    if var != "":
                        invars.append(var)
                print("Module: " + moduleName)
                print("Input: " + str(invars))
                moduleResponse = modApi.RunResponse(moduleName, invars)

                brainInputQueue.put(moduleResponse)

        else:
            response = response.replace("$user$", "")
            responseBroken = response.split("*")
            if len(responseBroken) > 1:
                emotionQueue.queue.clear()
                emotionQueue.put([responseBroken[1], False])
                faceDisplay.currentEmotion = responseBroken[1]
                response = responseBroken[0] + responseBroken[2]
            else:
                emotionQueue.queue.clear()
                emotionQueue.put(["normal", False])
                faceDisplay.currentEmotion = "normal"

            print("Output: " + response)

            ttsThread = Thread(target=tts.ProduceVoice, args=(response,))
            ttsThread.start()
            # tts.ProduceVoice(response)

    if emotionQueue.empty() is False:
        emotion = emotionQueue.get()
        faceDisplay.UpdateFace(emotion[0], emotion[1])
        faceDisplay.currentEmotion = emotion[0]

    # Check if the user has pressed escape
    if exitQueue.empty() is False:
        # If they have, exit the program
        if exitQueue.get() is True:
            faceDisplay.root.destroy()
            sys.exit(0)

    if affectiveMode is True:
        faceDisplay.Refresh()
