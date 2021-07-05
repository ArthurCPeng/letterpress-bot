# letterpress-bot
A bot to help you crush the game Letterpress. Given any game situation, it searches through a word bank and gives you a list of the best words you can play.

## Specifying the Game File
The game file must be a text file with the following formatting:  
- The first five lines each contain five letters, and together they describe all the letters in the game. There should be no spaces or any other characters.
- The next five lines each contain five numbers with values 0, 1 or 2, and together they describe the status of the game. A value of 0 indicates the tile has not been occupied. A value of 1 indicates that the tile is occupied by yourself / the player. A value of 2 indicates that the tile is occupied by the opponent.
- The remaining lines denote the words that have already been played. The program will ignore these words if they come up in the word bank. Each line must only contain one played word. 

## What the Program Does
1. Extract all words from the word bank, and get all words that can be played in the game
2. During the extraction process, if the program finds a word can be played to end the game (after playing the word, no unoccupied tiles remain), it will immediately output the word and its length.
3. Calculate possible plays for each word
4. Sort possible plays
5. Output all plays 

## Program Output
The output is printed in the console. The main output consists of a series of entries, with each entry describing one particular move.  
Each full-length entry has three components:
1. The word to be played
2. A four-element tuple `[me_occupied, enemy_occupied, me_safe, enemy_safe]` denoting the game stats after you play this move
3. A list of tuples `[(x1, y1, letter1), (x2, y2, letter2) ... (xn, yn, lettern)]` describing which tile to choose for each letter in the word.

For example, part of the output using the demo game file will look like:
> horgan: (6, 5, 2, 1), \[(5, 5, 'h'), (2, 2, 'o'), (4, 5, 'r'), (4, 4, 'g'), (5, 4, 'a'), (5, 3, 'n')\]  
> horgan: (6, 4, 2, 0), \[(5, 5, 'h'), (4, 1, 'o'), (4, 5, 'r'), (4, 4, 'g'), (5, 4, 'a'), (5, 3, 'n')\]  
> flyted: (6, 8, 2, 2), \[(1, 2, 'f'), (1, 4, 'l'), (1, 3, 'y'), (2, 3, 't'), (1, 5, 'e'), (2, 5, 'd')\]  
> herald: (6, 7, 2, 2), \[(5, 5, 'h'), (1, 5, 'e'), (4, 5, 'r'), (5, 4, 'a'), (1, 4, 'l'), (2, 5, 'd')\]  
> hareld: (6, 7, 2, 2), \[(5, 5, 'h'), (5, 4, 'a'), (4, 5, 'r'), (1, 5, 'e'), (1, 4, 'l'), (2, 5, 'd')\]  
> hanger: (6, 5, 2, 1), \[(5, 5, 'h'), (5, 4, 'a'), (5, 3, 'n'), (4, 4, 'g'), (2, 4, 'e'), (4, 5, 'r')\]

Some entries may only have the first two components. This may be because:
1. There is only one way to play the word, i.e. only one way to choose the letter tiles in the game to form the word. In this case the third component is unnecessary.
2. The program cannot calculate the full number of possibile moves for the word, due to limitations in functionality. In this case a random move is selected from all possible moves, and the entry is marked with the word "suboptimal".

### The Four-Element Game Stats Tuple
`me_occupied`: the number of tiles the player occupies.  
`enemy_occupied`: the number of tiles the enemy occupies.  
`me_safe`: the number of tiles the player secures (i.e. cannot be flipped by opponent).  
`enemy_safe`: the number of tiles the enemy secures (i.e. cannot be flipped by player).  


## Parameters to Specify
Most of these parameters have already been assigned a value, but you can change them to suit your preferences:
- `game_file`: The directory of the game file.  
- `word_bank_directory`: The directory of the word bank through which the program searches.   
- `exclude_letters`: Letters which you do NOT want to use. These words will be automatically ignored if encountered in the word bank.  
- `move_limit`: a limit for the number of game moves you want to output. For a value of 10000, it will take around 1-2 minutes to start outputting the possible moves. 
- `word_length_threshold`: If the longest word that can be played has x characters, then words shorter than (x-word_length_threshold) characters in the word bank will be ignored.  
- `sort_by`: How to rank the possible words and choices outputted by the program. `sort_by = 0`: sort according to the number of tiles the player can occupy. `sort_by = 2`: sort according to the number of SAFE tiles the player can occupy.  
- `alert_freq_1`: How frequently to output the program's progress when extracting data. Higher values denote lower frequency.  
- `alert_freq_2`: How frequently to output the program's progress when calculating possible moves. Higher values denote lower frequency.  
- `alert_freq_3`: How frequently to output the program's progress when sorting possible moves. Higher values denote lower frequency.  
