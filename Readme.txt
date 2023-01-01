Welcome to C&C app:


to run this app :
1. run CCserver.py.
2. run as many CCclient.py as you want.
3. you can play with the basic commands I've put in the server, all the commands will run threw the server cmd.

To add new commands all you need to do is:
in the server:
1. add new print that describe the command in the main_page().
2. create new function 
3. add new elif with the next userInput that send to the function you created.
4. in the end of the function, redirect to the main_page

if you need the client to this command too :
1. when you send message to the client start it with the userinput+':'
2. make elif for client that reads this prefix and send to a new function.
3. make the function syncronized to what you make in the server.



notice:
1. the client prints "sent keep alive to server" just to make us know - we can comment this line
2. this is my first time hearing about C&C and first time working with multi-threading application.
3. i know it's not perfect and not exacly what you asked for, but I wanted to handle it alone without any help from friends.
4. hope you would like it :)


Thank you,
Omer Arviv

