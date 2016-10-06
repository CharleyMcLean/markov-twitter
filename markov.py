import sys

import random

import os
import twitter




def open_and_read_file(file_path):

    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    #for files in sys.argv[1:]:
        # open(files).read()

    return open(file_path).read()



def make_chains(text_string, chains, n_gram=2):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """
    # Added in chains as a parameter so we can pass in multiple chain dictionaries.
    # Don't return at end when using chains as a paramenter.
    # chains = {}
    
    words = text_string.split()

    

    #Looping over the text and making dictionary of tuples and lists
    for i in range(len(words) - n_gram):
        n_gram_key = tuple(words[i:i + n_gram])
        n_gram_value = words[i + n_gram]
        if n_gram_key not in chains:
            chains[n_gram_key] = [n_gram_value]
        else:
            chains[n_gram_key].append(n_gram_value)

    # Checking the last two words.  If not in dictionary, a
    if tuple(words[-n_gram:]) not in chains:
        chains[tuple(words[-n_gram:])] = [None]
    else:
        chains[tuple(words[-n_gram:])].append(None)

    # return chains


def make_text(chains, n_gram=2):
    """Takes dictionary of markov chains; returns random text."""

    text_list = []

    generated_key = random.choice(chains.keys())

    while True:
        if generated_key[0].istitle():
            text_list.extend(list(generated_key))
            # print text_list
            break
        else:
            generated_key = random.choice(chains.keys())
            # print generated_key

    
    previous_words = generated_key[-(n_gram-1):]
    next_word = random.choice(chains[generated_key])


    while next_word:
        if next_word[-1] in [".", "?", "!"]:
            text_list.append(next_word)
            break
        text_list.append(next_word)
        next_group = tuple(text_list[-n_gram:])
        next_word = random.choice(chains[next_group])

    return " ".join(text_list)



input_path = sys.argv[1]
#another_input_path = sys.argv[2]

n_gram = int(raw_input("What size n-gram would you like to use? > "))

# Open the file and turn it into one long string
input_text_1 = open_and_read_file(input_path)
# input_text_2 = open_and_read_file(another_input_path)

# Get a Markov chain
chains = {}
chains_1 = make_chains(input_text_1, chains, n_gram)
# chains_2 = make_chains(input_text_2, chains, n_gram)

#print chains_1
#print chains_2

# print chains

# Produce random text
random_text = make_text(chains, n_gram)

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    )

# print api.VerifyCredentials()
print "random text:", random_text
status = api.PostUpdate(random_text)

print status.text

# Check out .update for dictionaries