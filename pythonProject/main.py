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
    "My name is ...",
    "I am ... years old",
    "I come from ...",
    "I live in ...",
    "I study ...",
    "I work as a ..."
}

def extractData():
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()

    pathOnCloud = "Audio/"
    pathLocal = "D:\Disertatie\Disertatie\pythonProject"

    for item in itemsToDownload:
        storage.child(pathOnCloud + item + ".wav").download(pathLocal,item + ".wav")


if __name__ == '__main__':
    extractData()
