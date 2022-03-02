import os
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCELoufHJ8jCuuBkBC1ykpfK9jEJkWXCQ0",
  "authDomain": "soundrecorder-ddc2b.firebaseapp.com",
  "projectId": "soundrecorder-ddc2b",
  "storageBucket": "soundrecorder-ddc2b.appspot.com",
  "messagingSenderId": "52019306448",
  "appId": "1:52019306448:web:8608d7ce4ec97eeb21e3d5",
  "measurementId": "G-5VS3F71B89",
  "databaseURL" : ""
}

itemsToDownload = {
    "Hello",
    "Name",
    "Age",
    "From",
    "LiveIn",
    "Study",
    "Work"
}

def extractData():
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()

    pathOnCloud = "Audio/"
    pathLocal = "D:/Disertatie/Disertatie/pythonProject"
    if not os.path.exists(pathLocal):
        os.makedirs(pathLocal)

    for item in itemsToDownload:
        storage.child(pathOnCloud + item + ".3gp").download(pathLocal,item + ".3gp")

    for file in os.listdir(pathLocal):
        if file.endswith(".3gp"):
            newFile = file[:-3].replace(".", "")
            sound = pathLocal + "/" + file
            result = pathLocal + "/" + newFile + ".wav"
            os.system(f'ffmpeg -i "{sound}" "{result}"')
            os.remove(sound)

if __name__ == '__main__':
    extractData()
