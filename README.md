# Bot for reading books
___

## A description of the interaction with the bot

The user sends the `/start` command to the bot (or starts it by searching for it). 
The bot greets the user, informs the user that the user can read the book directly in the chat with the bot, and prompts the user to see the list of available commands by sending the `/help` command.

At this point, the user can perform 5 actions:

- Send a chat command /help
- Send into chat the command /beginning
- Send into chat the command /continue
- Send command /bookmarks into chat
- Send any other message to the chat room

__Command__ `/help`.
The user sends the command `/help` into the chat room. The bot sends the user a list of available commands, tells them they can save pages of the book as bookmarks, and wishes them a pleasant reading experience.

__Command__ `/beginning`.
The user sends the chat command `/beginning`. The bot sends the chat the first page of the book and 3 inline buttons (back, current page number and forward).

### Accordingly, when interacting with the message-book, the user can:

- __Press__ the "Forward" button and then the bot will load the next page of the book if the current page is not the last page. 
The current page number on the button will increase by 1. And if the current page is the last page in the book, nothing will change.

- __Press__ on the button with the current page number and then the bot will save that page to bookmarks, letting the user know.

- __Press__ on the "Back" button and then the bot will load the previous page of the book if the current page is not the first page. The current page number on the button will decrease by 1. And if the current page is the first page, nothing will change

__Command__ `/continue`.
The user sends the `/continue` command to the bot. The bot sends to the chat the page of the book where the user stopped reading during the last interaction with the message-book. If the user has not yet started reading the book - the bot sends a message with the first page of the book.

__Command__ `/bookmarks`.
User sends chat command /bookmarks. If the user has saved bookmarks before, the bot sends a list of saved bookmarks to the chat as inline buttons, as well as inline "Edit" and "Cancel" buttons.

## How to run the bot
1. Download the repository with the bot
2. Install all the necessary dependencies by running the `pip install -r requirements.txt` command
3. Create a bot in Telegram and get its __API token__
in the __config.py__ file 
4. Replace the value of the `BOT_TOKEN` variable with the obtained __API token__
5. Run the bot by running the `python main.py` command