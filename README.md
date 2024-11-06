# Auto Send New Files Webhook
Do you want to automatically send new files from a directory of your computer to a Discord Webhook? Well now you can with this code. Don't worry anymore about taking the time to search the file and sending it manually. This code will automatically do it for you.

*Now Selfbot is available too.*

## Official Releases
You can download the last official release [here](https://github.com/Benjas333/AutoSendNewFilesWebhook/releases/tag/v1.0.0).

*Disclaimer: I don't know if it works properly in other operating systems than Windows.*

## Cloning repo
### Getting Started
[Python 3.12](https://www.python.org/downloads/) recommended.

[Discord](https://discord.com/) lol.

### Clone this project
```
git clone https://github.com/Benjas333/AutoSendNewFilesWebhook
cd AutoSendNewFilesWebhook
```
### Install dependencies
```
pip install -r requirements.txt
```
### Configure the .env file
- Change the content of `example.env`.
- Rename it to `.env`.
## Usage
### Command line
**`.env` file required.**
#### Webhook
```
python webhook.py
```
#### Selfbot
```
python selfbot.py
```
To use the selfbot you must provide your account token in the `.env` file.

`Ctrl + C` to stop the scripts.
### Import
#### Webhook
```python
# Import script
import webhook
from time import sleep

webhook.webhook.url = "https://your.discord.webhook/url" # Set webhook url
webhook.sendMessage("Hello, world!") # You can send simple messages
while True:
        sleep(1)
        webhook.checkForNewFiles(
                directory="C:\Your\Directory\",
                extension="*", # '*' will check all files in the directory
                recursive=True,
        )
        # This will check for new files every 1 second
```
I have realized webhook importing method is trash. I will redo this probably making it a class.
#### Selfbot
```python
# Import script
from selfbot import Selfbot

client = Selfbot(
        channel_id=1234567890 # the channel id where you want to send the files
        directory="C:\Your\Directory"
        extension="mp3"
        recursive=False,
)
client.run(token="YOUR TOKEN HERE")
```
Way better than the webhook importing method lol (for now).
#### If you want to use the .env file with the importing methods, you just need to make `import config`
## TO DO
- Find an optimized way to send big files quickly.

## Changelog
- Added [releases](https://github.com/Benjas333/AutoSendNewFilesWebhook/releases) for people not so familiar with programming in general.

## Contributing
Any contribution would be appreciated.
