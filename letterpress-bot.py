#Set the game file.
game_file = "game.txt"
file = open(game_file,"r")

#Enter letters which you do NOT want to use
exclude_letters = []

#Set a limit for the number of choices you want to output. A value of 10000 takes a few minutes
move_limit = 10000

#If the longest word that can be played has x characters, then words shorter than (x-word_length_threshold) characters
#in the word bank will be ignored.
word_length_threshold = 11

#How to rank the possible words and choices outputted by the program.
#sort_by = 0: sort according to the number of tiles the player can occupy 
#sort_by = 2: sort according to the number of SAFE tiles the player can occupy
sort_by = 2

#The directory of the word bank through which the program searches.
word_bank_directory = "all_words_lv3.txt"

game_data = file.read()
file.close()

game_letters = game_data.splitlines()[:5]
game_letters = [list(line) for line in game_letters]
game_status = game_data.splitlines()[5:10]
game_status = [[int(x) for x in list(line)] for line in game_status]
used_words = game_data.splitlines()[10:]

alert_freq_1 = 20000 #alert frequency of extracting data
alert_freq_2 = 2000 #alert frequency of calculating possibilities
alert_freq_3 = 2000 #alert frequency of sorting possibilities



def num_letter_in_word(letter, word):
    n = 0
    for x in word:
        if x == letter:
            n += 1
    return n

def get_secure_status():
    global game_status
    game_secure_status = []
    for row in range(5):
        row_secure_status = []
        for col in range(5):
            secure = 1
            if col > 0 and game_status[row][col] != game_status[row][col-1]:
                secure = 0
            if col < 4 and game_status[row][col] != game_status[row][col+1]:
                secure = 0       
            if row > 0 and game_status[row][col] != game_status[row-1][col]:
                secure = 0
            if row < 4 and game_status[row][col] != game_status[row+1][col]:
                secure = 0
            if game_status[row][col] == 0:
                secure = 0
            row_secure_status.append(secure)
        game_secure_status.append(row_secure_status)
    return game_secure_status 

game_secure_status = get_secure_status()

def find_optimal(letter):
    choices = []
    for row in range(5):
        for col in range(5):
            if letter == game_letters[row][col]:
                game_secure_status = get_secure_status()
                choices.append((row, col, game_status[row][col], game_secure_status[row][col]))

    enemy_secure_present = 0
    enemy_insecure_present = 0
    me_present = 0
    
    for choice in choices:
        if choice[2] == 2 and choice[3] == 1:
            enemy_secure_present = 1
        if choice[2] == 2 and choice[3] == 0:
            enemy_insecure_present = 1
        if choice[2] == 1:
            me_present = 1

    if enemy_insecure_present and (enemy_secure_present or me_present):
        choices_copy = choices[:]
        choices = []
        for choice in choices_copy:
            if (choice[2] == 2 and choice[3] == 0) or choice[2] == 0:
                choices.append(choice)
    return choices
        
def choice_number(letter):
    choices = find_optimal(letter)

    need_to_choose = 0
    num_choices = 0
    for choice in choices:
        if (choice[2] == 2 and choice[3] == 0) or choice[2] == 0:
            need_to_choose = 1
            num_choices += 1
    if num_choices == 0:
        return 1
    else:
        return num_choices 

 


#--------------------------Get word bank--------------------------#
file = open(word_bank_directory)
text = file.read()
words = text.split(" ")


#--------------------------Compile list of all letters in game-------------------#        
use_letters = []

for line in game_letters:
    for letter in line:
        use_letters.append(letter)


#--------------------------Compile list of letters left--------------------------#
letters_left = []
for row in range(5):
    for col in range(5):
        if game_status[row][col] == 0:
            letters_left.append(game_letters[row][col])

#--------------------------Define functions--------------------------#
#Function to get the statistics of a game. Returns a tuple with four elements:
#me_occupied: the number of tiles the player occupies
#enemy_occupied: the number of tiles the enemy occupies
#me_safe: the number of tiles the player secures (i.e. cannot be flipped by opponent)
#enemy_safe: the number of tiles the enemy secures (i.e. cannot be flipped by player)

def get_stats():
    me_occupied = 0
    me_safe = 0
    enemy_occupied = 0
    enemy_safe = 0
    
    game_secure_status = get_secure_status()
    
    for row in range(5):
        for col in range(5):
            if game_status[row][col] == 1:
                me_occupied += 1
                if game_secure_status[row][col] == 1:
                    me_safe += 1
            if game_status[row][col] == 2:
                enemy_occupied += 1
                if game_secure_status[row][col] == 1:
                    enemy_safe += 1
    return (me_occupied, enemy_occupied, me_safe, enemy_safe)


#Function to sort a list of words according to their length.    
def letter_sort(word_list):
    max_length = 0
    word_list_sorted = []
    for word in word_list:
        if len(word) > max_length:
            max_length = len(word)
    for i in range(max_length):
        for word in word_list:
            if len(word) >= max_length - i:
                word_list_sorted.append(word)
    return word_list_sorted

#-----------------------Extract words from word bank-----------------------#              
usable_words = []

counter = 0

print("Extracting data...")
for word in words:
    counter += 1
    if counter % alert_freq_1 == alert_freq_1 - 1:
        print("...progress: {}/{}".format(words.index(word), len(words)))
    
    if word.isalpha() == True:
        usable = 1
        
        use_letters_copy = use_letters[:]
        for letter in word:
            if letter in exclude_letters:
                usable = 0
            try:
                use_letters_copy.remove(letter)
            except:
                usable = 0

        if usable == 1:

            #Check to see if you can finish the game.
            #If yes, output the words that can be used to finish the game, and their length
            if len(word) >= len(letters_left):

                finishable = 1
                word_in_list = list(word)
                for letter in letters_left:
                    try:
                        word_in_list.remove(letter)
                    except:
                        finishable = 0
                if finishable == 1:
                    print("{:<10}: length {}, Game can be finished using this word".format(word, str(len(word))))

            #--------Append all usable words--------#
                    
            if word not in usable_words:
                usable_words.append(word)

usable_words = letter_sort(usable_words)

max_word_length = len(usable_words[0])

printed = []

all_moves = []


#-----------------------Calculating all possible plays for each word-----------------------#
print("Calculating possibilities for {} words...".format(len(usable_words)))
counter = 0

for x in range(len(usable_words)):
    word = usable_words[x]

    counter += 1
    if counter % alert_freq_2 == alert_freq_2 - 1:
        print("...progress: {}/{}".format(x, len(usable_words)))


    if len(word) < max_word_length - word_length_threshold:
        continue
    
    if word in printed:
        continue
    if word in used_words:
        continue

    
    printed.append(word)
    
    game_status_backup = [line[:] for line in game_status]
    num_lmc = 0 #numbers of Letters with Multiple Choices
    lmc = [] #letters with multiple choices
    lmc_choices = []
    for letter in word:
        if choice_number(letter) > num_letter_in_word(letter, word):
            num_lmc += 1
            lmc.append(letter)
            lmc_choices.append(find_optimal(letter))

    game_secure_status = get_secure_status()
    if num_lmc == 0:

        for letter in word:
            letter_choice = find_optimal(letter)[0]
            row = letter_choice[0]
            col = letter_choice[1]
        
            
            if  game_secure_status[row][col] == 0:
                game_status[row][col] = 1
        all_moves.append((word, get_stats()))
        game_status = [line[:] for line in game_status_backup]
        game_secure_status = get_secure_status()
    else:
        word_backup = word[:]
        word = list(word)

        letters_num_choices = []
        letters_choices = []

        workable = 1
        for letter in word:

            if num_letter_in_word(letter, word) >= 2:
                workable = 0
                break
            else:
                letters_num_choices.append(len(find_optimal(letter)))
                letters_choices.append(find_optimal(letter))
                
        if workable == 0:
            letter_usage = {}

            for letter in set(word):
                letter_usage[letter] = 0

            for letter in word:
                try:
                    letter_choice = find_optimal(letter)[letter_usage[letter]]
                except:
                    pass
                    
                letter_usage[letter] += 1
                
                row = letter_choice[0]
                col = letter_choice[1]

                if  game_secure_status[row][col] == 0:
                    game_status[row][col] = 1

            all_moves.append((word_backup, get_stats(), "suboptimal"))
            game_status = [line[:] for line in game_status_backup]
            game_secure_status = get_secure_status()
            
        if workable == 1:
            
            data = letters_num_choices

            k = len(data)

            permutations = ""
            permutation = [0] * k

            def perm(n, k, data):

                global permutations
                
                if k <= n-2:
                    for i in range(data[k]):
                        permutation[k] = i
                        perm(n, k+1, data)
                        
                else:
                    permutation_string = ""
                    for x in permutation:
                        permutation_string += str(x)
                        
                    permutations += permutation_string + " "

            perm(k+1,0,data)

            permutations = [[i for i in perm] for perm in permutations.split(" ")]

            game_status_backup = [line[:] for line in game_status]

            best_stats = (0,25,0,25)
            best_stats_moves = []

            printed_stats = []
            
            for permutation in permutations:

                move = []
                
                for i in range(len(permutation)):

                    row = letters_choices[i][int(permutation[i])][0]
                    col = letters_choices[i][int(permutation[i])][1]


                    if game_secure_status[row][col] == 0:
                        game_status[row][col] = 1

                   
                    move.append((col+1,row+1,game_letters[row][col]))

                game_secure_status = get_secure_status()

                
                if get_stats() not in printed_stats and move != []:
                    all_moves.append((word_backup, get_stats(), str(move)))
                    printed_stats.append(get_stats())
                game_status = [line[:] for line in game_status_backup]
                game_secure_status = get_secure_status()



#-----------------------Sorting all possible plays for all possible words-----------------------#
all_moves_sorted = []

print("Sorting all {} moves..".format(len(all_moves)))
counter = 0
for i in range(len(all_moves)):

    if counter >= move_limit:
        break

    
    counter += 1
    if counter % alert_freq_3 == alert_freq_3 - 1:
        print("...progress: {}/{}".format(i, len(all_moves)))
        
    move = all_moves[i]
    placed = 0
    if i == 0:
        all_moves_sorted.append(move)
        placed = 1
        
    else:
        if all_moves_sorted[0][1][sort_by] < move[1][sort_by]:
            all_moves_sorted = [move] + all_moves_sorted
            placed = 1
        elif all_moves_sorted[-1][1][sort_by] > move[1][sort_by]:
            all_moves_sorted = all_moves_sorted + [move] 
            placed = 1
    
        else:
            current_moves = len(all_moves_sorted)-1
            for j in range(current_moves):
                if all_moves_sorted[j][1][sort_by] >= move[1][sort_by] and  all_moves_sorted[j+1][1][sort_by] < move[1][sort_by]:
                    first_section = all_moves_sorted[:j]
                    first_section.append(move)
                    all_moves_sorted = first_section + all_moves_sorted[j:]
                    placed = 1
                    break
            for j in range(current_moves):
                if all_moves_sorted[j][1][sort_by] > move[1][sort_by] and  all_moves_sorted[j+1][1][sort_by] <= move[1][sort_by]:
                    first_section = all_moves_sorted[:j+1]
                    first_section.append(move)
                    all_moves_sorted = first_section + all_moves_sorted[j+1:]
                    placed = 1
                    break
            

    if placed == 0:
        all_moves_sorted = all_moves_sorted + [move]


for this_move in all_moves_sorted:
    word = this_move[0]
    stats = this_move[1]
    if len(this_move) == 3:
        move = this_move[2]
        print("{word}: {stats}, {move}".format(word = word, stats = stats, move = move))
    else:
        print("{word}: {stats}".format(word = word, stats = stats))        


