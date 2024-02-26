from gtts import gTTS
from playsound import playsound
import subprocess
import os


class TTS():
    """This is a class to handle the text to speech functionality of the project.

        Args:
            speak (_bool_): Enable or disable the voice function (playing the MP3s)
            affectiveMode (_bool_): Enable or disable the affective mode (Swapping between piper and gtts)

        Functions:
            ProduceVoice : This function takes a string and converts it to an MP3 file. It then plays the MP3 file.
            ActiveCheck : This function prints out the current settings of the TTS object.
    """

    def __init__(self, speak, affectiveMode, tempPath):
        self.text = ""
        self.speak = speak
        self.mode = affectiveMode
        self.tempPath = tempPath

    def ProduceVoice(self, textInput):
        """This function takes a string and converts it to an MP3 file. It then plays the MP3 file.

        Args:
            textInput (_string_): The text to be converted to speech.
        """
       
        self.outPath = self.tempPath + "/output.wav"
        print(self.outPath)
        self.text = textInput

        # Modify the text to remove any characters that may cause issues
        self.text = self.text.replace("'", "")
        self.text = self.text.replace("|", "")
        self.text = self.text.replace(";", "")
        self.text = self.text.replace("(", "")
        self.text = self.text.replace(")", "")
        self.text = self.text.strip()

        if os.path.exists(self.outPath):
            os.remove(self.outPath)

        if self.mode is True:
            # Use the piper library to create the audio file
            print("Starting piper")
            subprocess.call(("echo {} | piper --model Project/Dependencies/en_GB-alba-medium.onnx --output_file {}".format(self.text, self.outPath)), shell=True, timeout=None)
            # print(output)

        else:
            # Use the gtts library to create the audio file
            self.gtts = gTTS(self.text, lang='en')
            self.gtts.save(self.outPath)

        if self.speak is True:
            while not os.path.exists(self.outPath):
                # print("Waiting for file to be created")
                pass
            playsound(self.outPath)

    def PlayVoiceFile(self, file):
        """This function plays a pre-existing wav file.
        """
        playsound(file)

    def ActiveCheck(self):
        """This function prints out the current settings of the TTS object. To determine if the wrapper is correctly configured.
        """
        print("TTSwrapper is active with affective mode {} and speak mode {}".format(self.mode, self.speak))

