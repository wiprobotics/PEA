import subprocess
import time
import speech_recognition as sr


# Sound Device Class
class SoundDevice():
    """Class for interacting with the sound device(s) on linux

    Args:
        speechTextQueue (Queue, optional): Queue for the speech to text output. Defaults to None.
        sleepQueue (Queue, optional): Queue for the sleep state. Defaults to None.

    Functions:
        GetSinks: Gets all sinks and monitors
        CheckSinkState: Checks if sink is running or not
        PlaySound: Plays a sound through the default sink
        SoundLevel: Gets the sound level of the sink monitor, designed to be 
        polled continuously to get a live sound level
        Listen: Listens to the microphone and returns the audio
    """

    def __init__(self, speechTextQueue=None, sleepQueue=None):
        self.sinkNames, self.sinkMonitors = self.GetSinks()
        self.listenRecording = False
        self.speechTextQueue = speechTextQueue
        self.sleepQueue = sleepQueue

    def GetSinks(self, debug=False):
        """Gets all sinks and monitors

        Args:
            debug (bool, optional): Enable to print debug messages. Defaults to False.

        Returns:
            list: List of sink names
            list: List of monitor names
        """
        # Get sinks
        sinks = subprocess.check_output("pacmd list-sinks | grep -e 'name:'", shell=True).decode("utf-8").split('\n')
        sinkNames = []
        sinkMonitors = []
        for sink in sinks:
            if "name:" in sink:
                sinkNames.append(sink.split('name: ')[1])
                sinkMonitors.append(sink.split('name: ')[1].replace("<", "").replace(">", "") + ".monitor")

        if debug:
            print("Sinks:", sinkNames)

        return sinkNames, sinkMonitors

    def CheckSinkState(self, debug=False):
        """Checks if sink is running or not

        Args:
            debug (bool, optional): Enable to print debug messages. Defaults to False.

        Returns:
            bool: True if sink is running, False if not
        """

        # Check if sink is running
        sinkRunning = subprocess.check_output("pacmd list-sinks | grep -e 'state:'", shell=True).decode("utf-8").split('\n')
        state = sinkRunning[0].split('state: ')[1]

        if debug:
            print("State:", state)

        if state == "RUNNING":
            return True
        else:
            return False

    def PlaySound(self, soundPath):
        """Plays a sound through the default sink - note that the playsound library is probably a better option for this

        Args:
            soundPath (string): Path to the sound file
        """

        subprocess.run("pactl play-sample {} 0".format(soundPath), shell=True)

    def SoundLevel(self, debug=False, sinkMonitor=None):
        """Gets the sound level of the sink monitor, designed to be polled continuously to get a live sound level

        Args:
            debug (bool, optional): Enable to print debug messages. Defaults to False.
            sinkMonitor (string, optional): The sink monitor to use. Defaults to the first sink monitor in the list from GetSinks().

        Returns:
            float: The sound level in decibels (I think, just a value between 1 and 100 basically)
        """

        vol = -100

        if sinkMonitor is None:
            sinkMonitor = self.sinkMonitors[0]

        if debug:
            print("Killing old parec functions")

        subprocess.run("pkill -f 'parec --format=s16le'", shell=True)

        if debug:
            print("Starting recording")

        # Start recording with parec
        recording = subprocess.Popen(
            "parec --format=s16le -d {} | sox -t raw -r 44100 -b 16 -c 2 -e signed-integer - -t wav out.wav".format(sinkMonitor),
            shell=True
        )
        time.sleep(0.1)  # Adjust the duration based on your sample length

        # Stop recording
        recording.send_signal(subprocess.signal.SIGINT)

        if debug:
            print("Recording stopped")

        time.sleep(0.1)

        try:

            if debug:
                print("Running ffmpeg")

            # Run ffmpeg to get volume information
            cmd = "ffmpeg -i out.wav -af 'volumedetect' -vn -sn -dn -f null /dev/null"
            reading = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for the process to finish
            out, err = reading.communicate()

            if debug:
                print("ffmpeg volume check finished")

            # If invalid data detected set volume to -100 to indicate no sound detected
            errlines = err.decode("utf-8").split('\n')
            for line in errlines:
                if "Invalid Data" in line:
                    print("Invalid data detected")
                    vol = -100

            # Get the volume
            outlines = err.decode("utf-8").split('\n')
            for line in outlines:
                # print(line)  # Print each line for debugging
                if "mean_volume" in line:
                    vol = float(line.split("mean_volume: ")[1].split(" dB")[0])
                    break

        except Exception as e:
            if debug:
                print("Error in ffmpeg:", str(e))

        outVol = round((100 - vol*-1), 1)
        if debug:
            print("Volume:", outVol)

        return outVol

    # Function to convert speech to text using the microphone run in a separate thread to the main program
    def SpeechToText(self):
        """Function to convert speech to text using the microphone run in a separate thread to the main program
        """
        while True:
            print("Listening... Say something.")
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                print("Listening... Say something.")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            try:
                print("Recognizing...")
                self.sleepQueue.put([False, False])
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                self.speechTextQueue.put(text)
            except Exception as e:
                print("Error:", str(e))

    def ConsoleListen(self):
        """Listens for a console input and put it into the queue, an alternative to the SpeechToText function
        """
        while True:
            userInput = input("You: ")
            self.sleepQueue.put([False, False])
            self.speechTextQueue.put(userInput)