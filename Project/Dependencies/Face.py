from tkinter import Tk, Label
from PIL import ImageTk, Image
import time


class FaceDisplay():
    """Class for displaying the face, doesnt actually hold the tkinter window,
    just communicates with it

    Args:
        facePath (string): Path to the folder containing all the face images

    Functions:
        GenerateEmotions: Generates all emotions and stores them in a list, 
        hese are pre-defined but easy to add to
        UpdateFace: Updates the face to a new emotion
        Refresh: Refreshes the face, basically just a pass through to the 
        tkinter window but also considers GIF timings
    """

    def __init__(self, facePath, affectiveMode, xOffset, yOffset):
        self.facePath = facePath
        self.GenerateEmotions()
        self.root = Tk()
        self.window = FaceWindow(self.root, affectiveMode, xOffset, yOffset)
        self.lastTime = time.time()
        self.currentEmotion = "normal"
        self.xOffset = xOffset
        self.yOffset = yOffset

    def GenerateEmotions(self):
        """Generates all emotions and stores them in a list, these are
        pre-defined but easy to add to
        """
        self.emotions = []
        self.emotions.append(Emotion("happy", self.facePath + "/happy_closed.png", True, self.facePath + "/happy_open.png"))
        self.emotions.append(Emotion("normal", self.facePath + "/normal_closed.png", True, self.facePath + "/normal_open.png"))
        self.emotions.append(Emotion("sad", self.facePath + "/sad_closed.png", True, self.facePath + "/sad_open.png"))
        self.emotions.append(Emotion("thinking", self.facePath + "/thinking_closed.png", True, self.facePath + "/thinking_open.png"))
        self.emotions.append(Emotion("tired", self.facePath + "/tired_closed.png", True, self.facePath + "/tired_open.png"))
        self.emotions.append(Emotion("confused", self.facePath + "/confused_closed.png", True, self.facePath + "/confused_open.png"))
        self.emotions.append(Emotion("asleep", self.facePath + "/sleeping.gif", False, ""))

    def UpdateFace(self, emotionName, speaking):
        """Updates the face to a new emotion

        Args:
            emotionName (string): Name of the emotion to change to
            speaking (bool): Whether the user is speaking or not
        """
        self.refreshThread = None
        self.window.ChangeFace(emotionName, self.emotions, speaking)
        self.root.update()

    def Refresh(self):
        """Refreshes the face, basically just a pass through to the tkinter 
        window but also considers GIF timings
        """
        if time.time() - self.lastTime > self.window.timeBetweenFrames:
            self.lastTime = time.time()
            self.window.currentFrame += 1
            if self.window.currentFrame >= len(self.window.imageList):
                self.window.currentFrame = 0
            nextFrame = self.window.imageList[self.window.currentFrame]
            self.window.faceImageLabel.configure(image=nextFrame)

        self.window.faceImageLabel.configure(image=self.window.imageList[self.window.currentFrame])
        self.root.update()


class Emotion():
    """Class for storing emotion information

    Args:
        name (string): Name of the emotion
        path (string): Path to the image
        hasTalking (bool): Whether the emotion has a talking image or not
        talkingPath (string): Path to the talking image

    Functions:
        GetPath: Gets the path to the images the emotion is linked to
    """

    def __init__(self, name, path, hasTalking, talkingPath):
        self.name = name
        self.path = path
        self.hasTalking = hasTalking
        self.talkingPath = talkingPath

    def GetPath(self, talking):
        """Gets the path to the images the emotion is linked to

        Args:
            talking (bool): Whether the user is speaking or not

        Returns:
            string: The path to the image
        """
        if talking is True and self.hasTalking is True:
            return self.talkingPath
        else:
            return self.path


class FaceWindow():
    """Class for the tkinter window

    Args:
        parent (tkinter.Tk): The parent tkinter object

    Functions:
        ChangeFace: Changes the face to a new emotion
        quitFace: Quits the face window
    """

    def __init__(self, parent, affectiveMode, xOffset, yOffset):
        self.parent = parent
        self.parent.title("Face")
        self.parent.geometry("480x800+{}+{}".format(xOffset, yOffset))
        self.parent.resizable(False, False)
        self.parent.overrideredirect(True)
        self.faceImage = Image.open("Project/Dependencies/Faces/Background.png")
        self.faceImageTk = ImageTk.PhotoImage(self.faceImage)

        # Load the background image, this is a static image just to...
        # be rendered behind the face
        self.backgroundImage = Image.open("Project/Dependencies/Faces/Background.png")
        self.backgroundImageTk = ImageTk.PhotoImage(self.backgroundImage)

        # Create the image list which is a list used to store all the frames of the GIF
        self.imageList = [self.faceImageTk]
        self.currentFrame = 0

        # Create the background image label
        self.backgroundImageLabel = Label(image=self.backgroundImageTk)
        self.backgroundImageLabel.grid(row=0, column=0)

        if affectiveMode is True:
            # Create the face image label
            self.faceImageLabel = Label(image=self.faceImageTk)
            self.faceImageLabel.grid(row=0, column=0)

    def ChangeFace(self, emotionName, emotions, speaking):
        """Changes the face to a new emotion

        Args:
            emotionName (string): The name of the emotion to change to
            emotions (list): A list of all emotions
            speaking (bool): Whether the user is speaking or not
        """
        # Assign the current face to a variable to stop it being...
        # garbage collected, just photoimage things
        self.oldFaceImage = self.faceImage
        self.oldFaceImageTk = self.faceImageTk
        self.currentFrame = 0
        self.imageList = []
        # Cycle through all emotions and find the one we want
        for emotion in emotions:
            if emotion.name == emotionName:
                emotionPath = emotion.GetPath(speaking)
                # If the emotion is a gif, load it as a gif
                if emotionPath.endswith(".gif"):
                    # print("Loading GIF")
                    self.faceImage = Image.open(emotionPath)

                    # Get the GIF metadata
                    gif_info = self.faceImage.info

                    # Check if the image is animated and contains duration information
                    if 'duration' in gif_info:
                        duration = gif_info['duration']
                        self.fps = 1000 / duration
                        self.timeBetweenFrames = 1/self.fps
                        # print("GIF FPS: " + str(self.fps))

                    while True:
                        try:
                            # Load the GIF frames
                            self.faceImageTk = ImageTk.PhotoImage(self.faceImage)
                            self.imageList.append(self.faceImageTk)
                            self.faceImage.seek(self.faceImage.tell() + 1)
                            self.currentFrame += 1
                        except EOFError:
                            break

                # If the emotion is a png, load it as a png
                else:
                    self.faceImage = Image.open(emotionPath)
                    self.faceImageTk = ImageTk.PhotoImage(self.faceImage)
                    self.imageList.append(self.faceImageTk)
                    self.timeBetweenFrames = 0.1

                self.currentFrame = 0

        def quitFace():
            """Quits the face window
            """
            self.parent.destroy()
