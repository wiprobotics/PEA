# TTS dependencies
pip install gtts
pip install piper-tts

# Run piper to install the models
echo "ahhhhh" | piper --download-dir Project/Dependencies --data-dir Project/Dependencies --model en_GB-alba-medium --output_file Project/ahh.wav
sudo rm Project/ahh.wav

# Audio dependencies
sudo apt install portaudio19-dev
pip install pyaudio
pip install playsound
pip install sounddevice
sudo apt-get install libportaudio2
sudo apt install sox
sudo apt install ffmpeg

# GPT dependencies
sudo apt install linux-headers-$(uname -r)
sudo apt install pciutils
sudo apt install libvulkan1
wget https://gpt4all.io/installers/gpt4all-installer-linux.run
chmod +x gpt4all-installer-linux.run
sudo apt install libxcb-xinerama0 libxcb-cursor0
./gpt4all-installer-linux.run
pip install gpt4all

# Face dependencies
sudo apt-get install python3-tk
pip install tk
sudo apt-get install python3-pil python3-pil.imagetk

# Speech recognition dependencies
pip install SpeechRecognition

# Other dependencies
pip install pynput

# Module dependencies
pip install networkx