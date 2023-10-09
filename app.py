import random

# Automatically load and save vocabulary
LOAD_FROM_FILE_ON_START = True
SAVE_ON_EXIT = True

# Filename for vocabulary
VOC_FILE_NAME = 'voc.txt'

voc = set()
voc_desc = {}

def load_voc_from_file():
    '''
    Reads vocabulary from predefined VOC_FILE_NAME file
    :return:
    voc: set of vocabulary words
    voc_desc: dict with words as keys and descriptions as values
    '''
    result_voc = set()
    result_voc_desc = {}
    try:
        with open(VOC_FILE_NAME, 'r', encoding='utf-8') as file:
            for line in file:
                # print(line)
                linesplit = line.split(',', 1)
                # print(linesplit)
                if len(linesplit)!=2 or not linesplit[0].isalpha():
                    raise ValueError
                word=linesplit[0].strip().lower()
                if word in voc:
                    raise IndexError
                result_voc.add(word)
                result_voc_desc[word]=linesplit[1].strip()
    except IOError:
        print(f'No file {VOC_FILE_NAME}, or IO error')
    except ValueError:
        print(f'Wrong file format')
    except IndexError:
        print(f'Duplicate values in file')
    else:
        print('Vocabulary loaded from file')

    assert result_voc == set(result_voc_desc.keys())
    return result_voc, result_voc_desc


def save_to_file(voc,voc_desc):
    '''
    Writes vocabulary to predefined VOC_FILE_NAME file
    :param voc: set of vocabulary words
    :param voc_desc: dict with words as keys and descriptions as values
    :return:
    '''
    assert voc == set(voc_desc.keys())
    try:
        with open(VOC_FILE_NAME, 'w', encoding='utf-8') as file:
            for word in voc:
                file.write(word+','+voc_desc[word]+'\n')
    except IOError:
        print(f'Error writing to {VOC_FILE_NAME}')
    else:
        print('Writing vocabulary to file successfully.')


def printout_voc(voc_desc:dict, short=0, word_width=15):
    '''
    Prints out vocabulary
    :param voc_desc: dicts of vocabulary
    :param short: 0 to print full vocabulary, number to print only number items
    :param word_width: width of words to formatting
    :return:
    '''
    total_items=num_items=len(voc_desc)
    if short:
        num_items=min(short,total_items)
    sorted_words_indexes=sorted(list(voc_desc.keys()))
    print(f'Our vocabulary consist of {total_items} words:')
    for i in range(num_items):
        word = sorted_words_indexes[i]
        word_descr = voc_desc[word]
        if short and len(word_descr)>80:
            word_descr= word_descr[:80]+'...'
        print(word.rjust(word_width)+':  '+word_descr)
    if short and num_items<total_items:
        print('......(press 1 to see full vocabulary)......')
    # print()

def quiz(voc:set, voc_desc:dict, num_words, num_tries=7):
    '''
    Makes a quiz on vocabulary
    :param voc: set of vocabulary words
    :param voc_desc: dict with words as keys and descriptions as values
    :param num_words: how many words to quiz
    :param num_tries: how many tries to ask
    :return:
    '''
    assert voc == set(voc_desc.keys())
    total_words=len(voc)
    if num_words>total_words:
        print('Num words is greater than total words, setting num words to total words')
        num_words=total_words

    print('\n'*100)
    print('Time for quiz!')
    quiz_voc_list=list(voc)
    random.shuffle(quiz_voc_list)
    quiz_voc_list=quiz_voc_list[:num_words]
    score=0
    num_words_guessed=0
    for word_to_guess in quiz_voc_list:
        print('Guess word with meaning:',voc_desc[word_to_guess])
        try_num=7
        while try_num>0:
            guess=input('Your guess:')
            if guess==word_to_guess:
                print("Excellent! Correct guess!")
                score+=try_num
                num_words_guessed+=1
                break
            print('No! Please try again...')
        if try_num==0:
            print('Sorry out of tries! This word was:',word_to_guess,'\nGoog luck next time')
        print()
    print()
    print(f'Quiz completed.\nYou guessed {num_words_guessed} of {num_words} with the score of {score}')
    print()



if LOAD_FROM_FILE_ON_START:
    print('Autoload set to True, loading...')
    voc, voc_desc=load_voc_from_file()

CHOICE_STRING='''Please make a choise:
1. Print out all vocabulary
2. Add a word to vocabulary
3. Remove word from vocabulary
4. Run a quiz
5. Save vocabulary to local file
6. Load vocabulary from local file
7. Exit

'''

print('Welcome to simple Vocabulary builder application')

while True:
    printout_voc(voc_desc, short=5)
    print('----')
    print(CHOICE_STRING)
    choise=input('Your choice:')
    if choise=='1':
        printout_voc(voc_desc)
        print()
        input('Press ENTER to return to main menu')
        print()

    elif choise=='2':
        while True:
            new_word=input('New word to add:')
            new_word=new_word.lower()
            if new_word in voc:
                print('Word all ready in vocabulary')
            if not new_word.isalpha():
                print('Please use letters only')
            else:
                break
        new_word_decs=input(f"Please enter description for {new_word}:")
        voc.add(new_word)
        voc_desc[new_word]=new_word_decs
    elif choise == '3':
        while True:
            del_word = input('Enter word to remove:')
            del_word = del_word.lower()
            if not del_word.isalpha():
                print('Please use letters only')
            else:
                break
        if del_word not in voc:
            print('Word not in vocabulary')
        else:
            voc.remove(del_word)
            del voc_desc[del_word]
    elif choise=='4':
        while True:
            num=input('How many words to quiz:')
            try:
                num=int(num)
                if num>0:
                    break
                else:
                    print('Please enter a positive number')
            except ValueError:
                print('Please enter a positive number')
        quiz(voc,voc_desc,num)
    elif choise=='5':
        save_to_file(voc,voc_desc)
    elif choise=='6':
        voc,voc_desc=load_voc_from_file()
    elif choise=='7':
        break
    else:
        print("Please make a correct choice")
    assert voc==set(voc_desc.keys())

if SAVE_ON_EXIT:
   save_to_file(voc, voc_desc)

print('Thank you for using Vocabulary builder')

'''
                 cat: Vert good home tiger
                 dog: home wolf
                food: both tiger and wolf need it to survive
               happy: what i feel with home tiger and wolf
               honey: product of the bees
               human: prey for tigers and wolfs, but a friend to their home descendants
               mouse: both a computer gadget and a home tiger prey
'''