# letterpress-bot
A bot to help you crush the game Letterpress. Given any game situation, it searches through a word bank and gives you a list of the best words you can play.

Specifying the Game File
The game file must be a text file with the following formatting:
- The first five lines each contain five letters, and together they describe all the letters in the game. There should be no spaces or any other characters.
- The next five lines each contain five numbers with values 0, 1 or 2, and together they describe the status of the game. A value of 0 indicates the tile has not been occupied. A value of 1 indicates that the tile is occupied by yourself / the player. A value of 2 indicates that the tile is occupied by the opponent.
- The remaining lines denote the words that have already been played. The program will ignore these words if they come up in the word bank. Each line must only contain one played word. 

What the Program Does
- The program will 1) extract all words from the word bank and get all words that can be played in the game, 2) calculate all possible plays for each word, 3) sort all possible plays, and finally 4) output those plays.
- During the extraction process, if the program finds a word can be played to end the game (after playing the word, no unoccupied tiles remain), it will immediately output the word and its length.
