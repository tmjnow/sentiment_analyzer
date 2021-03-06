import os
import json
import numpy as np
import html.parser
import re
import pickle
import time

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import enchant
import pandas as pd

def get_wordnet_pos(treebank_tag):
    ## Removed Adjective from pos tagging as word_lemmatizer convert superlative degree to original form
    # if treebank_tag.startswith('J'):
    #     return wordnet.ADJ
    if treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def data_preprocessing(data):
    # PreProcess the data
    # Escape HTML char ir present
    html_parser = html.parser.HTMLParser()
    html_cleaned_data = html_parser.unescape(data)

    # Remove all unnecessary special character
    html_cleaned_data = re.sub('[^A-Za-z ]+', '', html_cleaned_data)

    # Break data into words and remove stop Words(or unnecessary words which doesn't have much influence on meaning)
    # TODO: pickle and save stop word list
    stop_words = ['after', 'others', 'clud', 'would', 'id', 'self', 'youll', 'brother', 'second', 'shes', 'yet', 'bit',
                  'break', 'shop', 'suppose', 'sell', 'holiday',
                  'becomes', 'youd', 'etc', 'college', 'shin', 'server', 'uni', 'jordanknight', 'wishing', 'swine',
                  'adam', 'full', 'clean', 'anyway', 'sometimes',
                  'prom', 'england', 'bath', 'battery', 'button', 'plz', 'freakin', 'click', 'addict', 'topic', 'code',
                  'puppy', 'app', 'random', 'ball', 'heard', 'mile', 'plane', 'revision', 'sat', 'ahead', 'kiss', 'arm',
                  'ear', 'indeed', 'tan', 'state', 'hmmm', 'group', 'longer', 'vip', 'mommy', 'fire', 'co', 'sale',
                  'hotel', 'wash', 'web', 'lakers', 'dark', 'currently', 'ruin', 'lately', 'ohh', 'ff', 'hun', 'left',
                  'huh', 'track', 'buddy', 'profile', 'bloody', 'fucking',
                  'tough', 'island', 'wave', 'official', 'oops', 'setting', 'pls', 'ok', 'thunder', 'oo', 'grandma',
                  'fave', 'complete', 'cross', 'eh', 'bug', 'gosh', 'extra', 'practice', 'travel', 'street', 'design',
                  'watchin',
                  'size', 'oooh', 'charge', 'disney', 'guys', 'xbox', 'mind', 'link', 'fall', 'course', 'hair', 'wife',
                  'eye', 'thats', 'come', 'plot',
                  'english', 'so', 'house', 'year', 'stick', 'nap', 'sigh', 'ride', 'dress', 'sing', 'tea', 'fast',
                  'account', 'realize', 'park', 'decide', 'understand', 'order', 'nd', 'cream', 'less', 'chat', 'way',
                  'spend', 'fly', 'try', 'baby', 'already', 'call', 'eat', 'follow', 'play', 'men', 'take', 'cooky',
                  'gunna', 'wall', 'tree', 'client',
                  'essay', 'sushi', 'germany', 'twice', 'list', 'be', 'jon', 'loud', 'fav', 'danny', 'boat', 'style',
                  'mention', 'camp', 'except', 'chill', 'block', 'near', 'hospital', 'lets', 'radio', 'fight', 'lie',
                  'gorgeous', 'looks', 'alright', 'taste', 'issue', 'storm', 'scary', 'wine',
                  'girlfriend', 'vid', 'spring', 'jam', 'hit', 'reply', 'close', 'remember', 'soup', 'line', 'put',
                  'lines', 'direct', 'three', 'couple', 'next', 'pray', 'glass', 'waiting', 'count', 'arrive', 'bag',
                  'bar', 'invite', 'mothers', 'pull', 'sounds', 'reading', 'remind', 'along', 'round', 'matter',
                  'although', 'swim', 'guitar', 'mate', 'joke', 'return', 'low', 'single', 'hangover', 'everybody',
                  'door', 'hahah', 'bb',
                  'home', 'else', 'saw', 'work', 'check', 'foot', 'may', 'birthday', 'bottle', 'machine', 'sunburn',
                  'mmm', 'grad', 'mmm', 'available',
                  'followers', 'chris', 'joy', 'anymore', 'teach', 'got', 'catch', 'hang', 'outside', 'drive', 'real',
                  'sit', 'feeling', 'every', 'turn', 'follower', 'going', 'send', 'listen', 'stay', 'god', 'kitty',
                  'kate', 'mcfly', 'demi', 'france', 'davidarchie', 'tip',
                  'gutted', 'ima', 'present', 'airport', 'computer', 'half', 'hello', 'able', 'room', 'chance',
                  'throat', 'pool', 'band', 'probably', 'bring', 'anyone', 'babe', 'lunch', 'food', 'cry', 'whats',
                  'seem', 'update', 'meet', 'forget', 'uh', 'attack', 'woohoo', 'mama', 'local', 'jack',
                  'student', 'smoke', 'brazil', 'york', 'everything', 'taking', 'couch', 'green', 'mitchelmusso',
                  'support', 'file', 'flight', 'comment', 'kick', 'sunshine', 'beat', 'butt', 'alive', 'imma', 'bff',
                  'texas', 'morrow', 'pant', 'law', 'cloud', 'desk',
                  'personal', 'kitchen', 'hes', 'west', 'push', 'king', 'training', 'warm', 'huge', 'bet', 'paper',
                  'card', 'burn', 'hold', 'load', 'cook', 'fell', 'rather', 'evening', 'moon', 'apparently', 'ate',
                  'boys', 'wii', 'strange', 'credit', 'mi', 'girls', 'strawberry', 'control', 'grade', 'talent',
                  'anytime', 'forgot', 'burnt', 'brothers', 'connect', 'accident',
                  'taylorswift', 'switch', 'mo', 'made', 'canada', 'jb', 'mornin', 'fry', 'bus', 'cake', 'blue',
                  'white', 'age', 'throw', 'plus', 'nope', 'small', 'looking', 'forever', 'trying', 'vacation', 'beer',
                  'upload', 'listening', 'mess', 'working', 'light', 'day', 'channel', 'bird', 'cleaning', 'cell',
                  'wheres', 'schedule', 'msn', 'folk', 'article', 'milk', 'imagine', 'key', 'darn', 'dnt', 'san',
                  'making', 'knee', 'clear', 'everyday', 'crack', 'anywhere', 'afford', 'consider', 'floor', 'however',
                  'somebody', 'expensive', 'secret', 'drag', 'draw', 'quote', 'lake', 'chip', 'unless', 'strong',
                  'delicious', 'row', 'system', 'crappy', 'workout', 'create',
                  'husband', 'blackberry', 'gig', 'goes', 'fam', 'guy', 'allow', 'bro', 'alot', 'whatever', 'roll',
                  'clothes', 'theres', 'minutes', 'done', 'july', 'different', 'safe', 'record', 'lay', 'sort',
                  'cancel', 'relax', 'thinking', 'stand', 'absolutely', 'apart', 'cuddle', 'hide', 'mini', 'ily',
                  'explain', 'j', 'attempt', 'possibly', 'bos', 'nooo', 'war', 'pet', 'sam', 'flower', 'lead', 'option',
                  'juice', 'spanish', 'table', 'rough', 'handle', 'lookin', 'fault', 'dat', 'public', 'nightmare',
                  'football', 'hehehe', 'soccer', 'request', 'everyones', 'florida', 'squarespace', 'sport', 'six',
                  'onto', 'sa', 'hoo', 'heres', 'north', 'winter', 'alex', 'delay', 'truly', 'medium', 'spam', 'workin',
                  'wind', 'pro',
                  'world', 'could', 'yourselves', 'text', 'august', 'energy', 'ad', 'egg', 'tonite', 'narrative',
                  'point', 'speak', 'cover', 'shout', 'trailer', 'thru', 'peep', 'wet', 'copy', 'trek', 'friends',
                  'shift', 'contact', 'woke', 'honey', 'screw', 'drinking' 'spot', 'tune', 'graduate', 'gift', 'jk',
                  'australia', 'price', 'board', 'south', 'hahahaha', 'fresh', 'match', 'prob', 'bunch', 'cough',
                  'laundry', 'color', 'degree', 'include', 'feelin', 'anyways', 'sum', 'broken', 'mix', 'living',
                  'prepare', 'dry', 'orange', 'attend', 'boston', 'daily',
                  'everyone', 'sequence', 'deliver', 'finale', 'sit', 'assignment', 'spell', 'science', 'social',
                  'treat', 'heading', 'fml', 'nearly', 'fat', 'somewhere', 'playing', 'nose', 'child', 'f', 'tweetdeck',
                  'earlier', 'ton', 'library', 'gah', 'hah', 'whos', 'grrr', 'lord', 'suggestion', 'sandwich', 'ac',
                  'bread', 'mostly', 'aunt', 'shitty', 'conference', 'deep', 'tha', 'awhile', 'spent', 'relaxing', 'ms',
                  'model', 'noooo', 'cupcake', 'net', 'fab', 'network', 'fuckin', 'prefer', 'toast', 'lmfao', 'sarah',
                  'status', 'otherwise', 'aha', 'os', 'heh', 'abt', 'appear', 'sucks', 'ughh', 'tattoo', 'rent',
                  'earth', 'meal', 'hoping', 'bowl', 'golf', 'cali', 'allergy', 'macbook', 'anybody', 'gross', 'heck',
                  'snow', 'contest', 'slightly', 'cable',
                  'us', 'weight', 'level', 'exams', 'million', 'america', 'diet', 'getting', 'toe', 'stage', 'dammit',
                  'rd', 'fever', 'delete', 'race', 'info', 'blow', 'ring', 'went', 'magic', 'brain', 'lesson', 'manage',
                  'background', 'possible', 'doubt', 'missing', 'land', 'interest', 'sitting', 'nail', 'bite', 'mark',
                  'doin', 'starbucks', 'rid', 'middle', 'cheap',
                  'yum', 'taylor', 'gay', 'sooooo', 'daddy', 'eating', 'dang', 'awwww', 'nyc', 'paint', 'album', 'ny',
                  'sometime', 'continue', 'neck', 'player', 'simple', 'cost', 'prayer', 'barely', 'everywhere',
                  'program', 'finished', 'somehow', 'hav', 'matt', 'chinese', 'edit', 'found', 'angel', 'harry',
                  'marry', 'log', 'ahhhh', 'atm',
                  'jon', 'series', 'store', 'actually', 'years', 'man', 'im', 'with', 'only', 'is', 'had', 'rd', 'shut',
                  'fever', 'delete', 'better', 'race', 'silly', 'info', 'blow', 'ring', 'went', 'magic', 'brain',
                  'lesson', 'manage', 'background', 'possible', 'doubt', 'missing', 'land', 'interest', 'sitting',
                  'nail', 'bite', 'mark', 'doin', 'starbucks', 'rid', 'middle',
                  'll', 'into', 'being', 'a', 'ohhh', 'me', 'seem', 'has', 'mine', 'ask', 'age', 'dinner', 'been',
                  'why', 'force', 'flat', 'connection', 'apartment', 'market', 'limit', 'leaving', 'perhaps', 'loss',
                  'slept', 'rule', 'goodness', 'total', 'um', 'paris', 'bgt', 'h', 'festival', 'shake', 'woot', 'dc',
                  'skin',
                  'where', 'can', 'than', 'in', 'sex', 'memory', 'blood', 'pc', 'nick', 'itunes', 'coz', 'cheese',
                  'chillin', 'hill', 'mall', 'dunno', 'mail', 'bear', 'def', 'ooh', 'drunk', 'choice', 'heat', 'sky',
                  'surgery', 'sir', 'quit', 'across', 'hero', 'pair',
                  'days', 'from', 'who', 'the', 'should', 'your', 'blah', 'thanx', 'weve', 'xo', 'hannah',
                  'jonathanrknight', 'bf', 'mobile', 'tweeps', 'vegas', 'teacher', 'realise', 'kno', 'shopping', 'area',
                  'purse', 'victoria', 'alyssamilano',
                  'outta', 'bother', 'dentist', 'session', 'pack', 'themselves', 'chicago', 'donniewahlberg', 'while',
                  'we', 'africa', 'sm', 'injury', 'necklace', 'remote', 'lens', 'indoors', 'amen', 'sd', 'device',
                  'bound', 'sofa',
                  'against', 'further', 'sydney', 'conan', 'sleeping', 'dave', 'soul', 'grab', 'recently', 'tennis',
                  'software', 'makes', 'wide', 'remove', 'enter', 'replace', 'awe'
                                                                             'these', 'those', 'were', 'be', 'holy',
                  'turn', 'leave', 'station', 'midnight', 'him', 'cuz', 'hardcore', 'sorta', 'extreme', 'arse', 'mario',
                  'relieve', 'coverage', 'phoenix', 'linux', 'purpose', 'therapy', 'sonic', 'legal', 'safely', 'dizzy',
                  'simon', 'introduce', 'karma', 'halo', 'rabbit', 'cheesecake', 'buying', 'snl', 'phil', 'distance',
                  'signing', 'nigga',
                  'teeth', 'bummer', 'office', 'argh', 'our', 'which', 'yo', 'jus', 'piss', 'daughter', 'cup', 'wit',
                  'effin', 'eve', 'yogurt', 'plastic', 'sand', 'needle', 'mariahcarey', 'valley', 'tiger', 'wings',
                  'clever', 'beg', 'legend', 'united', 'nine', 'edition', 'gt', 'sober', 'rly', 'twitterville',
                  'workshop', 'usb', 'mirror', 'z', 'tad', 'election', 'aaron', 'bagel', 'proof', 'came', 'met', 'dia',
                  'ian', 'addictive', 'smooth', 'chain', 'backyard', 'await', 'countdown', 'development', 'sweden',
                  'cleveland', 'trentreznor', 'inbox', 'chilly', 'reception', 'jessica', 'patrick', 'overnight',
                  'engine', 'tournament', 'beef', 'tat', 'tweetup', 'federer', 'hahaa', 'doh', 'thread', 'thou',
                  'just', 'box', 'note', 'tom', 'myspace', 'service', 'cheer', 'raining', 'road', 'rainy', 'window',
                  'menu', 'butterfly', 'sickness', 'dvr', 'fantasy', 'started', 'chop', 'besties', 'alice',
                  'management', 'berry', 'mega', 'srsly', 'skirt', 'yelyahwilliams', 'oooo', 'vanilla', 'potential',
                  'xxxxx', 'factory', 'korean', 'memorial', 'sara', 'kat', 'neglect', 'whale', 'meeee', 'ikea',
                  'passion', 'don', 'trap', 'iz', 'polish', 'active', 'leavin', 'reckon', 'pat', 'videos', 'pr', 'gum',
                  'knw', 'ubuntu', 'blogger', 'shaun', 'girly', 'strip', 'diff', 'twist', 'collect', 'convo', 'detroit',
                  'campus', 'laker', 'hype', 'iced', 'nokia', 'furniture', 'uber', 'humid', 'exit', 'opposite', 'solid',
                  'chilling', 'yucky', 'childhood',
                  'tummy', 'doing', 'this', 'had', 'mike', 'shoulder', 'salad', 'asap', 'dirty', 'performance', 'comp',
                  'shell', 'driver', 'grand', 'error', 'member', 'freeze', 'spending', 'obviously', 'goodmorning',
                  'hook', 'survive', 'user', 'literally', 'twitpic', 'scratch', 'chick', 'crush', 'knock', 'diversity',
                  'toy', 'massive', 'everytime', 'mmmm', 'wee', 'letter', 'driving', 'apps', 'bake', 'boot', 'plant',
                  'pa', 'writing', 'stream', 'trend', 'uncle', 'presentation', 'conversation', 'susan',
                  'wwwtweeteraddercom', 'sugar', 'hella', 'brand', 'baseball', 'crave', 'tweeter', 'montana', 'horse',
                  'third', 'vet', 'yard', 'ankle', 'tht', 'truck', 'accept', 'theyll', 'aim', 'original', 'fellow',
                  'andy',
                  'theirs', 'i', 'under', 'm', 'herself', 'show', 'club', 'alone', 'bitch', 'cheap', 'interview',
                  'yummy', 'spread', 'hole', 'doc', 'california', 'jesus', 'launch', 'lovin', 'lip', 'print', 'ryan',
                  'wifi', 'dougiemcfly', 'detail', 'selenagomez', 'soooooo', 'perform',
                  'type', 'bbq', 'apple', 'graduation', 'by', 'at', 'until', 'here', 'officially', 'case', 'idk',
                  'bike', 'atlanta', 'ang', 'bone', 'mon', 'ng', 'careful', 'vs', 'bbc', 'surf', 'jacket', 'compliment',
                  'yeahh', 'glorious', 'iv', 'brownie', 'speech', 'allergic', 'twitterverse', 'bedroom', 'lightning',
                  'bruise', 'bob', 'similar', 'nooooo', 'normally', 'marketing', 'sunburnt', 'needs', 'pretend',
                  'trade', 'roast', 'offline', 'emily', 'en', 'talented', 'bull', 'playin', 'highly', 'hack', 'package',
                  'basketball', 'competition', 'bt', 'simply', 'hay', 'rich', 'mexico', 'bubble', 'gd', 'singer',
                  'punch', 'rofl', 'cereal', 'att', 'yey', 'battle', 'gaga', 'awh', 'virus', 'pump', 'grill', 'ireland',
                  'pure', 'soak', 'gf', 'que', 'prolly',
                  'itll', 'garden', 'sims', 'leg', 'boyfriend', 'camera', 'jonasbrothers', 'son', 'were', 'if',
                  'myself', 'closer', 'hawaii', 'pee', 'itd', 'poker', 'court', 'sauce', 'icecream', 'ace', 'surely',
                  'perezhilton', 'apt', 'lolz', 'china', 'easily', 'bought', 'bugger', 'distract', 'boooo', 'ure',
                  'pride', 'desperate', 'mexican', 'assume', 'fridge', 'seeing', 'stalk', 'cherry', 'wondering',
                  'awwwww', 'preview', 'common', 'mass', 'oil', 'ti', 'feedback', 'effort', 'india', 'female', 'skill',
                  'september', 'babysitting', 'outfit', 'trick', 'hd', 'wolverine', 'fox', 'eu', 'piano', 'convince',
                  'frm', 'urgh', 'pity', 'bestie', 'swimming', 'funeral', 'rate', 'jordan', 'stone', 'fully',
                  'studying', 'spoil', 'monster', 'chest', 'tony', 'yoga', 'youngq', 'con', 'thnx', 'deck', 'momma',
                  'cap', 'creepy', 'opinion', 'stoke', 'garage',
                  'ma', 'delivery', 'password', 'swell', 'pressure', 'il', 'progress', 'mp', 'earn', 'pill', 'spin',
                  'bud', 'hrs', 'pasta', 'entry', 'steak', 'comfy', 'technology', 'pillow', 'hockey', 'di', 'escape',
                  'wheel', 'donut', 'damnit', 'dare', 'philippines', 'repair', 'softball', 'ch', 'accidentally',
                  'tasty', 'scotland', 'audition', 'register', 'melbourne', 'wana', 'recipe', 'freedom', 'dis', 'skool',
                  'marathon', 'dear', 'join', 'together', 'figure', 'sunny', 'learn', 'test', 'watching', 'tell',
                  'ours', 'as', 'all', 'each', 'how', 'when', 'adult', 'thanks', 'whose', 'other', 'itself', 'an',
                  'beginning', 'cramp', 'plug', 'sittin', 'angels', 'mary', 'sneak', 'faith', 'houston', 'pig', 'yu',
                  'jimmy', 'friendly', 'tomorow', 'farrah', 'compare', 'iranelection', 'doll', 'november', 'moms',
                  'tweets', 'sweat', 'austin', 'icon', 'maths', 'yikes', 'metro', 'ghost', 'bk', 'manchester',
                  'announce', 'april', 'makin', 'square', 'walking', 'tt', 'access', 'coast', 'advice', 'lock',
                  'happen',
                  'thursday', 'ahhh', 'miley', 'my', 'did', 'them', 'ourselves', 'va', 'melt', 'dawn', 'tomfelton',
                  'cooking', 'gloomy', 'eric', 'fest', 'apprentice', 'refresh', 'manager', 'kim', 'philly',
                  'opportunity', 'struggle', 'cam', 'starve', 'yawn', 'tax', 'tongue', 'bump', 'meat', 'contract',
                  'cop', 'shaundiviney', 'gfalcone', 'item', 'sadness', 'yuck', 'poster', 'chelsea', 'noon', 'heel',
                  'pot', 'moro', 'desktop', 'depend', 'confirm', 'lawn', 'omfg', 'q', 'kris', 'ray', 'serve', 'peanut',
                  'hungover', 'aswell', 'japan', 'singing', 'ass', 'walmart', 'noodle', 'naked', 'cnt', 'lover',
                  'brunch', 'italian', 'potato', 'couldve', 'community', 'honor', 'pen', 'hip', 'mia', 'ho', 'gs',
                  'during', 'whom', 'am', 'i', 'r', 'o', 'same', 'are', 'visual', 'maintain', 'number', 'wannabe',
                  'jonas', 'bc', 'lab', 'whilst', 'nkotb', 'mondays', 'noo', 'theyve', 'thinkin', 'hills', 'scared',
                  'muscle', 'snack', 'dan', 'poo', 'lyric', 'purchase', 'relate', 'application', 'shape', 'monkey',
                  'rehearsal', 'van', 'clip', 'vids', 'katie', 'mee', 'charger', 'section', 'celebrity', 'ol', 'yellow',
                  'justin', 'giant', 'insomnia', 'tim', 'general', 'mission', 'kelly', 'jess', 'yell', 'bio', 'comic',
                  'breath', 'laying', 'planning', 'mcdonalds', 'grass', 'comin', 'coming',
                  'french', 'business', 'yup', 'tuesday', 'have', 'ipod', 'above', 'what', 'both', 'do', 'off',
                  'before', 'spirit', 'noone', 'blink', 'tool', 'spider', 'someday', 'ocean', 'darling', 'actual', 'ow',
                  'duty', 'picnic', 'apply', 'loose', 'candy', 'er', 'proper', 'idiot', 'migraine', 'situation',
                  'shock', 'cancer', 'breathe', 'meh', 'certainly', 'ashley', 'mm', 'tooth', 'med', 'texting', 'rite',
                  'cash', 'burger', 'challenge', 'cavs', 'whenever', 'flash', 'heaven', 'bacon', 'killer', 'xxxx',
                  'chuck', 'todays', 'packing', 'kitten',
                  'or', 'having', 'now', 'too', 'on', 'and', 'town', 'ms', 'cd', 'ode', 'imagery', 'company', 'xoxo',
                  'cyrus', 'amy', 'wrap', 'shouldve', 'ie', 'al', 'gb', 'nothin', 'tie', 'tryin', 'makeup', 'hunt',
                  'museum', 'jason', 'field', 'tag', 'corner', 'bathroom', 'dish', 'rice', 'fancy', 'lauren', 'potter',
                  'missin', 'booo', 'truth', 'sea', 'process', 'commercial', 'tech', 'rubbish', 'hadnt', 'banana',
                  'yah', 'difference', 'response', 'repeat', 'bedtime', 'chair', 'loser', 'national', 'fee',
                  'appointment', 'pancake',
                  'doctor', 'wedding', 'dm', 'wednesday', 'twilight', 'luv', 'notice', 'ps', 'smell', 'front', 'hubby',
                  'gb', 'tie', 'recommendation', 'george', 'dread', 'tommorow', 'cookie', 'stink', 'cheers', 'gold',
                  'vega', 'joeymcintyre', 'mouse', 'anniversary', 'ground', 'press', 'ftw', 'certain', 'fathers',
                  'retweet', 'sux', 'gas', 'atl', 'neighbor', 'kevin', 'rush', 'el', 'httptweetsg', 'health', 'havin',
                  'ahaha', 'tix', 'nah', 'often', 'revise', 'twit', 'fish', 'fill', 'double', 'feed', 'bank', 'wat',
                  'shot', 'through', 'ppl', 'mood', 'meeting', 'lil', 'she', 'his', 'do', 'bday', 'laptop', 'youtube',
                  'wen', 'peterfacinelli', 'usa', 'miami', 'mountain', 'tried', 'pub', 'youu', 'miserable', 'orlando',
                  'massage', 'ed', 'pre', 'pie', 'current', 'settle', 'tight', 'address', 'keyboard', 'bang', 'install',
                  'princess', 'butter', 'ebay', 'adventure', 'wicked', 'paul', 'wants', 'times', 'seattle', 'clock',
                  'nephew', 'forum', 'twin', 'running', 'dallas', 'instal', 'colour', 'hanging', 'niece', 'tmrw',
                  'wing', 'aka', 'nut', 'iran', 'pour', 'clue', 'purple', 'coke', 'ep', 'mode', 'eff', 'ew', 'parade',
                  'starting', 'magazine', 'atleast', 'crew', 'chapter', 'fruit', 'italy', 'ex', 'rub', 'jersey', 'dj',
                  'tweeting', 'building', 'terminator', 'wwwtweeterfollowcom', 'le', 'ughhh', 'heyy', 'bell', 'suggest',
                  'alcohol', 'thunderstorm', 'curious', 'pound', 'regular', 'correct', 'bust', 'language', 'josh',
                  'basically', 'tshirt',
                  'church', 'side', 'mother', 'homework', 'goin', 'tour', 'lady', 'there', 'won', 'they', 'firefox',
                  'probs', 'data', 'sf', 'peter', 'snap', 'root', 'watched', 'shine', 'insane', 'flip', 'talkin',
                  'swift', 'seems', 'hugs', 'bah',
                  'to', 't', 'few', 'put', 'was', 'woo', 'within', 'gang', 'wellacted', 'stir', 'bring', 'soap',
                  'aplusk', 'climb', 'wooo', 'wouldve', 'tooo', 'private', 'content', 'bee', 'guest', 'dig',
                  'gym', 'shirt', 'wed', 'ache', 'si', 'chicken', 'goodbye', 'yr', 'g', 'pizza', 'talk', 'today',
                  'hows', 'broke', 'tweetie', 'cruise', 'ko', 'whether', 'ooo', 'boyle', 'hayfever', 'beyond', 'quiz',
                  'cafe',
                  'c', 'mum', 'episode', 'sleepy', 'hr', 'via', 'xxx', 'london', 'ahh', 'chocolate', 'phone', 'date',
                  'red', 'gossip', 'yeh', 'besides', 'dannymcfly', 'hw', 'bunny', 'beta', 'tiny', 'thankyou', 'txt',
                  'jay', 'pas', 'smh', 'restaurant', 'senior', 'grey', 'east', 'feels', 'hardly', 'focus', 'research',
                  'ish', 'dollar', 'admit', 'center', 'discover', 'cos', 'grr', 'goal', 'gr', 'ben', 'windows',
                  'decision', 'german', 'properly', 'ship', 'grocery', 'speed', 'host', 'jean', 'europe', 'cloudy',
                  'slowly', 'customer', 'downtown', 'decent', 'ty', 'haircut', 'taco',
                  'city', 'soooo', 'nite', 'xd', 'ice', 'bout', 'it', 'did', 'june', 'cat', 'afternoon', 'tommcfly',
                  'hop', 'gnight', 'britney', 'bay', 'inspire', 'suit', 'queen', 'avatar', 'exercise',
                  'lmao', 'himself', 'facebook', 'aw', 'fix', 'asleep', 'her', 'such', 'have', 'yours', 'for', 'things',
                  'gear', 'infection', 'msg', 'palm', 'noise', 'several', 'geek', 'wild', 'exist', 'spain', 'iron',
                  'bomb', 'zoo', 'toronto', 'suddenly', 'umm', 'bean', 'took', 'steve', 'per', 'buck', 'river', 'stock',
                  'headed', 'whoa', 'skype',
                  're', 'will', 'ain', 's', 'you', 'identity', 'leaden', 'christmas', 'americans', 'street',
                  'preposterous', 'ladies', 'petewentz', 'lion', 'randomly', 'katy', 'centre', 'thankfully',
                  'l', 'timing', 'pink', 'audience', 'viewer', 'search', 'get', 'toward', 'gettin', 'ouch', 'bum',
                  'cousin', 'curl', 'prince', 'gona', 'wood', 'thurs', 'dancing', 'woah', 'singapore', 'sry', 'zone',
                  'popular', 'curse', 'edward', 'teen', 'sundays', 'eventually', 'url', 'sniff', 'sooner', 'jeff',
                  'meant', 'bein', 'theory', 'paranoid', 'jet', 'license', 'ups', 'se', 'moving', 'bleh', 'writer',
                  'cmon', 'amanda', 'rt', 'errand', 'microsoft', 'havnt', 'dye', 'blind', 'lvatt', 'gun', 'tomato',
                  'ban', 'blonde', 'demo', 'function', 'roof', 'wallet', 'andrew', 'tap', 'shave', 'grandpa', 'muffin',
                  'layout', 'photoshop', 'split', 'bros', 'hall', 'nighty', 'podcast', 'grace', 'subway', 'thatll',
                  'hire', 'woop', 'diego', 'headphone', 'windy', 'spare', 'zombie', 'tryna', 'mah', 'planet', 'rachel',
                  'panda', 'hooray', 'tease', 'police', 'hee', 'destroy', 'transformer', 'university', 'spill',
                  'rescue', 'drum', 'tgif', 'photography', 'yahoo', 'hangin', 'kirstiealley', 'cod', 'bummed', 'knight',
                  'officialtila', 'amazon', 'sweetheart', 'security', 'lemon', 'sheet', 'oven', 'pe', 'loop', 'dope',
                  'dust', 'holla', 'toooo', 'pit', 'eatin', 'poem', 'geography', 'sub', 'tweeple', 'frozen', 'recital',
                  'pin', 'hike', 'vista', 'helpful', 'vibe', 'kimkardashian', 'dump', 'mental', 'nj', 'pregnant',
                  'thomas', 'marley', 'dannygokey', 'friggin', 'eminem', 'argentina', 'whoo', 'sucky', 'society',
                  'bracelet', 'torture', 'nc', 'asshole', 'therealjordin', 'whoever', 'upon', 'aussie', 'march',
                  'voting', 'flow', 'organize', 'pix', 'grateful', 'pleased', 'favor', 'nerve', 'precious', 'te',
                  'hood', 'advance', 'swollen', 'gots',
                  'uk', 'stomach', 'shoe', 'google', 'their', 'yall', 'fb', 'team', 'flu', 'thx', 'wtf', 'voice', 'esp',
                  'fri', 'central', 'bing', 'universe', 'jerk', 'tank', 'coach', 'duck', 'coursework', 'meee', 'seven',
                  'tube', 'mrs', 'swing', 'takin', 'tape', 'reunion', 'waitin', 'owe', 'sudden', 'tbh', 'itchy',
                  'judge', 'disneyland', 'youuu', 'wk', 'digital', 'hv', 'amuse', 'ohhhh', 'neighbour', 'jen', 'appt',
                  'turkey', 'alexalltimelow', 'alas', 'dick', 'lisa', 'heal', 'rainbow', 'talking', 'megan',
                  'following', 'bleed', 'fl', 'remain', 'divorce', 'afterwards', 'finals', 'gnite', 'tracecyrus',
                  'awkward', 'fo', 'wth', 'playlist', 'michelle', 'mag', 'yer', 'flag', 'information', 'shiny', 'nxt',
                  'jake', 'blanket', 'stair', 'ahah', 'deadline', 'fawcett', 'scott', 'robin', 'exact', 'legs',
                  'twitters', 'sunglass', 'santa', 'smith', 'learning', 'ellen', 'tues', 'veggie', 'unable', 'tall',
                  'jim', 'married', 'cartoon', 'steph', 'tx', 'heap', 'asot', 'bowling', 'sob', 'plate', 'gal', 'pete',
                  'map', 'reaction', 'recent', 'wknd', 'willing', 'coldplay', 'papa', 'thai', 'stranger', 'waking',
                  'reader', 'approve', 'norway', 'develop', 'concern', 'irish', 'kristen', 'slide', 'raw', 'forecast',
                  'finger', 'mtv', 'math', 'followfriday', 'yep', 'download', 'bye', 'rain', 'about', 'between', 'wan',
                  'flickr', 'october', 'hahahah', 'previous', 'wanted', 'cheat', 'source', 'cricket', 'transformers',
                  'comedy', 'borrow', 'theatre', 'cab', 'location', 'require', 'dam', 'jst', 'kids', 'rove', 'pocket',
                  'useful', 'morn', 'rockin', 'charlie', 'bak', 'owner', 'definately', 'greek', 'insurance', 'ran',
                  'hater', 'mmmmm', 'pissed', 'youth', 'solo', 'zero', 'ull', 'iamdiddy', 'trending', 'whoop', 'ga',
                  'addiction', 'crawl', 'lem', 'wrist', 'gmail', 'ne', 'kobe', 'emma', 'homemade', 'carpet', 'role',
                  'brace', 'hmmmm', 'parking', 'wise', 'dun', 'ooooh', 'xp', 'porn', 'accent', 'twittering', 'mummy',
                  'exchange', 'jamie', 'mow', 'wossy', 'buzz', 'shoutout', 'gone', 'ash', 'aye', 'rat', 'speaker',
                  'dads', 'budget', 'geez', 'ashleytisdale', 'indian', 'skate', 'flood', 'sync', 'whore', 'demand',
                  'solve', 'oz', 'hiya', 'twitterland', 'metal', 'sooooooo', 'guide', 'tmr', 'lilyroseallen', 'cutie',
                  'rap', 'impressed', 'backup', 'shade', 'charm', 'slice', 'sec', 'speaking', 'doggy', 'dull',
                  'bastard', 'trash', 'resist', 'wrk', 'natural', 'shortly', 'joey', 'adore', 'slip', 'brush',
                  'unfollow', 'ds', 'premiere', 'promote', 'intense', 'ohio', 'celebration', 'temp', 'bride', 'anna',
                  'hp',
                  'hug', 'season', 'tweet', 'hey', 'weekend', 'that', 'once', 'does', 'shall', 've', 'save', 'drop',
                  'answer', 'staff', 'grrrr', 'lounge', 'shed', 'asian', 'wordpress', 'poop', 'vampire', 'prove', 'dd',
                  'wireless', 'musicmonday', 'waffle', 'sneeze', 'logo', 'comfort', 'opening', 'express', 'gud',
                  'vodka', 'brian', 'lang', 'obsess', 'medicine', 'tidy', 'soft', 'hon', 'laura', 'browser', 'bridge',
                  'bella', 'stephenfry', 'cu', 'snuggle', 'billy', 'lap', 'nicole', 'audio', 'nurse', 'drain',
                  'somethin', 'biology', 'lb', 'emotional', 'sayin', 'ahhhhh', 'bass', 'maintenance', 'towards',
                  'semester', 'tempt', 'nicely', 'wars', 'ummm', 'selena', 'plain', 'leak', 'yayy', 'din', 'sausage',
                  'cow', 'fyi', 'nba', 'envy', 'tee', 'typical', 'task', 'thingy', 'kyle', 'smash', 'personally',
                  'dannywood', 'boom', 'andyclemmensen', 'wa', 'johncmayer', 'giggle', 'jones', 'supernatural',
                  'position', 'inch', 'discuss', 'prize', 'thee', 'yayyy', 'nadal', 'theyd', 'pathetic', 'christian',
                  'denver', 'phew', 'obama', 'lo', 'grandparent', 'male', 'pup', 'blister', 'easter', 'cycle', 'gg',
                  'weed', 'blogging', 'jazz', 'belong', 'grind', 'farm', 'physic', 'signal', 'un', 'army', 'username',
                  'highlight', 'display', 'sleepover', 'patient', 'wud', 'accord', 'explode', 'updated', 'downstairs',
                  'chore', 'lebron', 'solution', 'skinny', 'refer', 'daniel', 'curry', 'twitterer', 'minus',
                  'reference', 'transfer', 'thousand',
                  'he', 'of', 'y', 'own', 'again', 'roll', 'international', 'medium', 'martin', 'make', 'd', 'people',
                  'condition', 'demons', 'supply', 'eww', 'paramore', 'whew', 'concentrate', 'reminder', 'km',
                  'souljaboytellem', 'songzyuuup', 'shoulda', 'glasgow', 'dublin', 'tend', 'johnny', 'naw', 'spymaster',
                  'claim', 'wreck', 'grumpy', 'statement', 'activity', 'duh', 'pal', 'closet', 'gooood', 'mint', 'teh',
                  'stack', 'monitor', 'ft', 'pepper', 'craving', 'balance', 'wipe', 'homie', 'leno', 'caffeine',
                  'jacob', 'blip',
                  'amount', 'screen', 'sun', 'due', 'em', 'mac', 'page', 'yea', 'message', 'xox', 'sony', 'mosquito',
                  'junior', 'sinus', 'ap', 'remix', 'roommate', 'wire', 'died', 'donate', 'gotten', 'pt', 'league',
                  'warn', 'checking', 'any', 'partner', 'game', 'hehe', 'st', 'thatd', 'habit', 'markhoppus', 'flick',
                  'kay', 'nevermind', 'multiple', 'holly', 'twitterberry', 'chem', 'somewhat', 'domain', 'oclock',
                  'virtual', 'titanic', 'wats', 'lily', 'wishes', 'silver', 'earthquake', 'rose', 'route', 'sent',
                  'dessert', 'puke', 'freezing', 'emo', 'wah', 'hint', 'ttyl', 'emergency', 'everythings', 'mango',
                  'pile', 'sean', 'hed', 'umbrella', 'safari',
                  'train', 'til', 'ticket', 'pic', 'study', 'damn', 'morning', 'tonight', 'thing', 'twitter', 'haha',
                  'patch', 'laurenconrad', 'hahahahaha', 'volunteer', 'string', 'stephen', 'vancouver', 'ant', 'kit',
                  'prop', 'salt', 'bash', 'listenin', 'sending', 'ako', 'port', 'gm', 'shud', 'cs', 'wt', 'restore',
                  'castle', 'circle', 'fridays', 'arse'
                                                 'tomorrow', 'does', 'was', 'its', 'below', 'hers', 'yourself']
    movie_stop_words = ['actors', 'actor', 'idea', 'ca', 'provide', 'old', 'timeless', 'goood', 'cultural',
                        'collection', 'target',
                        'return', 'want', 'example', 'filmmaker', 'entertainment', 'touch', 'feature', 'use', 'care',
                        'dvd',
                        'omg', 'wow', 'minute', 'heart', 'set', 'experience', 'piece', 'act', 'also', 'script',
                        'action',
                        'end', 'cast', 'documentary', 'see', 'life', 'exam', 'cold', 'okay', 'parent', 'k', 'e',
                        'project',
                        'hmm', 'website', 'da', 'hat', 'youve', 'tho', 'weather', 'hi', 'car', 'post', 'friday', 'kid',
                        'sunday', 'party', 'read', 'story', 'x', 'ur', 'lol', 'yay', 'night', 'na', 'gon', 'villain',
                        'acting', 'u', 'family', 'oh', 'cinematic',
                        'dialogue', 'hm', 'chynna', 'screenplay', 'head', 'popcorn', 'goofy', 'drive', 'simpleminded',
                        'seat', 'part', 'event', 'nature', 'sustain', 'routine', 'sentimental', 'step', 'instantly',
                        'political', 'raise', 'thoroughly', 'engage', 'summer', 'sequel', 'bogarde', 'moment',
                        'history',
                        'ya', 'thoughtful', 'become', 'photo', 'fan', 'keep', 'ah', 'place', 'write', 'filmmaking',
                        'subject', 'art', 'worth', 'young', 'picture', 'ddlovato', 'p', 'fuck', 'shit', 'plan',
                        'iphone',
                        'video', 'month', 'aww', 'ta', 'n', 'yesterday', 'mom', 'ugh', 'shampoo', 'painfulbr', 'coolio',
                        'musclebound',
                        'baloney', 'hairline', 'joe', 'blog', 'belly', 'aweinspiring', 'power', 'capture', 'herzog',
                        'lawrence', 'et', 'opera', 'product', 'score', 'email', 'mileycyrus', 'breakfast', 'dude',
                        'effect',
                        'shower', 'dance', 'visit', 'wear', 'site', 'pick', 'ha', 'concert', 'online', 'sexy', 'soo',
                        'sister', 'internet', 'boo', 'btw', 'news', 'japanese', 'r', 'name', 'drink', 'b', 'hahaha',
                        'monday', 'think', 'cinematography', 'father', 'say',
                        'studio', 'boy', 'direction', 'remind', 'toilet', 'painting', 'cinema', 'evening', 'soundtrack',
                        'design', 'dreadful', 'pm', 'class', 'mouth', 'stoop', 'occasionally', 'animal', 'friend',
                        'word',
                        'awww', 'imax', 'conviction', 'goodnight', 'trip', 'writ', 'movies', 'american', 'actress',
                        'classic', 'star', 'directed', 'spiritual', 'crime', 'wry', 'final', 'inane', 'directorial',
                        'build', 'fashion', 'add', 'moviemaking', 'junk', 'gem', 'stretch', 'scream',
                        'harvard', 'crowd', 'simultaneously', 'refreshingly', 'future', 'sight', 'doze', 'open',
                        'result',
                        'heavyhanded', 'offbeat', 'touching', 'visuals', 'dream', 'material', 'bor', 'emerge', 'title',
                        'coffee', 'sooo', 'kinda', 'beach', 'dog', 'saturday', 'xx', 'dad', 'human', 'enterta', 'ett',
                        'production',
                        'performances', 'wish', 'feces', 'base', 'examination', 'felt', 'deal', 'flimsy',
                        'demonstrate', 'kill', 'seek', 'air', 'share', 'totally', 'execute', 'films', 'face',
                        'firstrate',
                        'allen', 'skip', 'element', 'lifeless', 'detailed', 'franchise', 'combine', 'quiet', 'inside',
                        'treasure', 'pop', 'landscape', 'usually', 'superficial', 'standard', 'dramatically',
                        'characters',
                        'writerdirector', 'oldfashioned', 'help', 'character', 'oscar', 'adaptation', 'tv', 'main',
                        'sense',
                        'woman', 'girl', 'middle',
                        'scenes', 'terest', 'substance', 'reach', 'newcomer', 'graphic', 'country', 'moviegoing',
                        'vision',
                        'toss', 'guess', 'space', 'aspect', 'crass', 'someone', 'school', 'witless', 'excuse',
                        'meander',
                        'equally', 'merely', 'animated', 'hear', 'person', 'scene', 'suck', 'cheesy', 'creativity',
                        'protagonist', 'artificial', 'rest', 'term', 'ago', 'throughout', 'scifi', 'familiar',
                        'technical',
                        'manner', 'amateurish', 'brown', 'book', 'rhythm', 'exactly', 'mak', 'cut', 'artist', 'image',
                        'edge', 'question', 'director', 'ive', 'back', 'th', 'chemistry', 'bill', 'lee',
                        'audiences', 'producers', 'spielberg', 'mindnumbingly', 'bond', 'document', 'strike', 'ii',
                        'washington', 'poetry', 'soar', 'vital', 'frame', 'remake', 'filmed', 'ensemble', 'watchable',
                        'wellmade', 'sign', 'wo', 'sound', 'form', 'shoot', 'inept', 'melodrama', 'view',
                        'animation', 'review', 'song', 'musical', 'songs', 'black', 'though', 'thriller', 'theater',
                        'br', 'dialog', 'james', 'one', 'clarity', 'whimsical', 'odd', 'tear', 'expect', 'guarantee',
                        'journey', 'dead', 'stunt', 'maker', 'novel', 'choose', 'lift', 'period', 'sensual',
                        'portrayal',
                        'thumb', 'british', 'body', 'quickly', 'characterization', 'worthwhile', 'hand', 'storyline',
                        'first', 'four', 'five', 'ten', 'master', 'wait', 'tone', 'gore', 'ru', 'filmbr',
                        'viewers', 'dr', 'debut', 'predictable', 'fit', 'drug', 'goodhearted', 'jackson', 'reality',
                        'tired', 'career', 'chase', 'suspenseful', 'usual', 'consistently', 'derivative', 'dub',
                        'steven',
                        'transform', 'culture', 'release', 'death', 'money', 'spy', 'insight', 'motion', 'begin', 'era',
                        'stefan', 'jrs', 'mar', 'palestinian', 'elisha', 'taboos',
                        'jessie', 'hindu', 'let', 'gag', 'heartwarming', 'carry', 'value', 'thoughtprovoking',
                        'gandolfini', 'theme', 'job', 'die', 'relationship', 'core', 'past', 'modern', 'watch',
                        'heartfelt',
                        'version', 'live', 'pay', 'water', 'de', 'mov', 'moviebr', 'robert', 'v',
                        'liv', 'david', 'w', 'la', 'sitt', 'volv', 'tak', 'michael', 'ope', 'mr', 'hour', 'movie',
                        'music', 'film', 'two', 'nt', 'th', 'rrb', 'lrb', 'youre', 'john', 'bor', 'ett', 'hollywood',
                        'drama', 'theyre', 'yeah', 'com', 'itbr', 'genre']

    # Performing Word Lemmatization on text
    word_lemmatizer = WordNetLemmatizer()
    words_to_keep = []
    for word, typ in nltk.pos_tag(word_tokenize(html_cleaned_data)):
        typ = get_wordnet_pos(typ)
        if typ:
            lemmatized_word = word_lemmatizer.lemmatize(word, typ).lower()
        else:
            lemmatized_word = word_lemmatizer.lemmatize(word).lower()

        # Removing Stop words and correct spelled words
        # Remove all non-english or mis-spelled words
        enchant_dict = enchant.Dict("en_US")
        if enchant_dict.check(lemmatized_word) and lemmatized_word not in stop_words + movie_stop_words:
            words_to_keep.append(lemmatized_word)

    return words_to_keep

def create_vocab(file_to_read, file_dir_list, vocab_dir):

    len_vocab = 0
    vocab_frequency = {}
    vocab_to_idx = {}
    idx_to_vocab = {}
    for each_file in file_to_read:
        for each_dir in file_dir_list:
            try:
                with open(os.path.join(each_dir, each_file), 'r') as f:
                    data = f.read()
            except:
                continue

        preprocessed_word = data_preprocessing(data)

        # create word to index and index to word dictionary
        vocab = set(preprocessed_word)
        for indx, val in enumerate(vocab):
            # Count frequency of the Word
            if val in vocab_frequency:
                vocab_frequency[val] += 1
            else:
                vocab_frequency[val] = 1
                len_vocab += 1

    print("Length of Vocab", len_vocab)

    # Sort Vocab by their frequency
    frequent_words_tuple = sorted(vocab_frequency.items(), key=lambda x: x[1], reverse=True)

    # Before saving Dictionary create index of vocab based on descending order of their frequency
    # So if we are taking max 'n' words based on frequency then their index will be limited to 'n'
    # Add Extra Padding words
    vocab_to_idx['<pad>'] = 0
    idx_to_vocab[0] = '<pad>'
    idx = 1
    for val, freq in frequent_words_tuple:
        vocab_to_idx[val] = idx
        idx_to_vocab[idx] = val
        idx += 1
    print('Saving Dictionary')
    dictionary = {'vocab_to_index': vocab_to_idx, 'index_to_vocab': idx_to_vocab, 'vocab_frequency_tuple': frequent_words_tuple}
    with open(vocab_dir, 'wb') as f:
        pickle.dump(dictionary, f)
    print('Vocab successfully saved to: {0}'.format(vocab_dir))

def create_data(file_to_read, file_dir_list, vocab_dir, max_word, file_dir):
    with open(vocab_dir, 'rb') as f:
        data = pickle.load(f)
    vocab_to_index = data['vocab_to_index']
    index_to_vocab = data['index_to_vocab']
    vocab_frequency_tuple = data['vocab_frequency_tuple']
    vocab_len = len(data['vocab_frequency_tuple'])

    train_pos_sample_dir = file_dir_list[0]
    train_neg_sample_dir = file_dir_list[1]
    test_pos_sample_dir = file_dir_list[2]
    test_neg_sample_dir = file_dir_list[3]


    max_features = vocab_len
    target_data = []
    input_data = np.array([], int)

    # Keep maximum frequent occurring words
    frequent_words = [val for val, freq in vocab_frequency_tuple][:max_features]

    # Process each file
    for each_file in file_to_read:
        # Read Data from file
        try:
            with open(os.path.join(train_pos_sample_dir, each_file), 'r') as f:
                data = f.read()
                target_data.append(1)
        except:
            try:
                with open(os.path.join(train_neg_sample_dir, each_file), 'r') as f:
                    data = f.read()
                    target_data.append(0)
            except:
                try:
                    with open(os.path.join(test_neg_sample_dir, each_file), 'r') as f:
                        data = f.read()
                        target_data.append(0)
                except:
                    with open(os.path.join(test_pos_sample_dir, each_file), 'r') as f:
                        data = f.read()
                        target_data.append(1)

        # Pre-Process data word level
        preprocessed_word = data_preprocessing(data)

        # Create data
        truncated_review = []
        for each_word in preprocessed_word:
            # Take words which are frequent
            if each_word in frequent_words:
                try:
                    truncated_review.append(vocab_to_index[each_word])
                    if len(truncated_review) >= max_word:
                        break
                except Exception as exc:
                    print(
                        '[Exception] if Key word not present in vocab dict but present in frequent words its a bug: {0}'.format(
                            exc))

        # Pad appropriately if less words are present
        word_len = len(truncated_review)
        if word_len:
            if word_len < max_word:
                truncated_review += [0] * (max_word - word_len)
            if len(input_data) != 0:
                input_data = np.vstack((input_data, truncated_review))
            else:
                input_data = np.hstack((input_data, truncated_review))
        else:
            # Remove latest added element from target data
            target_data.pop()
            print('Truncated Review ', truncated_review)
            print('Data ', data)

    # conver target to numpy array
    target_data = np.array(target_data)

    data_dict = {'input': input_data, 'target': target_data}
    with open(file_dir, 'wb') as f:
        pickle.dump(data_dict, f)

    print('Max value in test: ', data_dict['input'].max(1).max())
    print('Input shape ', data_dict['input'].shape)
    print('Target shape ', data_dict['target'].shape)
    print('Successfully saved data to {0}'.format(file_dir))

def _test_process_imdb_data():
    # Data Directory
    train_pos_sample_dir = '/home/john/geek_stuff/Data_Set/IMDB_sentiment_analysis_data/aclImdb/train/pos'
    train_neg_sample_dir = '/home/john/geek_stuff/Data_Set/IMDB_sentiment_analysis_data/aclImdb/train/neg'
    test_neg_sample_dir = '/home/john/geek_stuff/Data_Set/IMDB_sentiment_analysis_data/aclImdb/test/neg'
    test_pos_sample_dir = '/home/john/geek_stuff/Data_Set/IMDB_sentiment_analysis_data/aclImdb/test/pos'

    train_pos = [each_file for each_file in os.listdir(train_pos_sample_dir) if
                 os.path.isfile(os.path.join(train_pos_sample_dir, each_file))]
    train_neg = [each_file for each_file in os.listdir(train_neg_sample_dir) if
                 os.path.isfile(os.path.join(train_neg_sample_dir, each_file))]
    test_pos = [each_file for each_file in os.listdir(test_pos_sample_dir) if
                os.path.isfile(os.path.join(test_pos_sample_dir, each_file))]
    test_neg = [each_file for each_file in os.listdir(test_neg_sample_dir) if
                os.path.isfile(os.path.join(test_neg_sample_dir, each_file))]

    file_list = train_pos + train_neg + test_pos[:6250] + test_neg[:6250]
    vocab_dir = '/home/john/sentiment_files/data/movie_vocab.pkl'
    train_dir = '/home/janmejaya/sentiment_files/data/complete_data_aug9/imdb_train.pkl'
    test_dir = '/home/janmejaya/sentiment_files/data/complete_data_aug9/imdb_test.pkl'
    dir_list = [train_pos_sample_dir, train_neg_sample_dir, test_pos_sample_dir, test_neg_sample_dir]
    # creating Vocab from training data
    create_vocab(file_to_read=file_list, file_dir_list=dir_list, vocab_dir=vocab_dir)
    # Train data parameters
    max_word = 15           # maximum words to keep in a sentence
    create_data(file_to_read=file_list, file_dir_list=dir_list, vocab_dir=vocab_dir, max_word=max_word, file_dir=train_dir)

    # Test data
    file_list = test_pos[6250:] + test_neg[6250:]
    create_data(file_to_read=file_list, file_dir_list=dir_list, vocab_dir=vocab_dir, max_word=max_word,
                file_dir=test_dir)

def _test_twitter_data():
    vocab_dir = '/home/john/sentiment_files/data/movie_vocab.pkl'
    train_dir = '/home/janmejaya/sentiment_files/data/complete_data_aug9/imdb_train.pkl'

    # Read Train file
    df = pd.read_csv('/home/janmejaya/sentiment_files/text_data/Twitter_3class/training.1600000.processed.noemoticon.csv', encoding='latin-1', header=None)
    df.columns = ['Sentiment', 'NR1', 'NR2', 'NR3', 'NR4', 'Phrase']


    # Create Vocabulary
    sentiment_list = df['Sentiment'].tolist()
    vocab_frequency = {}
    vocab_to_idx = {}
    idx_to_vocab = {}
    len_vocab = 0
    for idx, data in enumerate(df['Phrase'].tolist()):
        if sentiment_list[idx] not in [0, 4]:
            continue

        preprocessed_word = data_preprocessing(data)
        # create word to index and index to word dictionary
        vocab = set(preprocessed_word)
        for indx, val in enumerate(vocab):
            # Count frequency of the Word
            if val in vocab_frequency:
                vocab_frequency[val] += 1
            else:
                vocab_frequency[val] = 1
                len_vocab += 1

    print("Length of Vocab", len_vocab)

    # Sort Vocab by their frequency
    frequent_words_tuple = sorted(vocab_frequency.items(), key=lambda x: x[1], reverse=True)

    # Before saving Dictionary create index of vocab based on descending order of their frequency
    # So if we are taking max 'n' words based on frequency then their index will be limited to 'n'
    # Add Extra Padding words
    vocab_to_idx['<pad>'] = 0
    idx_to_vocab[0] = '<pad>'
    idx = 1
    for val, freq in frequent_words_tuple:
        vocab_to_idx[val] = idx
        idx_to_vocab[idx] = val
        idx += 1
    print('Saving Dictionary')
    dictionary = {'vocab_to_index': vocab_to_idx, 'index_to_vocab': idx_to_vocab,
                  'vocab_frequency_tuple': frequent_words_tuple}
    with open(vocab_dir, 'wb') as f:
        pickle.dump(dictionary, f)
    print('Vocab successfully saved to: {0}'.format(vocab_dir))


    # create Train data

    # train Parameter
    max_word = 15

    with open(vocab_dir, 'rb') as f:
        data = pickle.load(f)
    vocab_to_index = data['vocab_to_index']
    index_to_vocab = data['index_to_vocab']
    vocab_frequency_tuple = data['vocab_frequency_tuple']
    vocab_len = len(data['vocab_frequency_tuple'])

    max_features = vocab_len
    target_data = []
    input_data = np.array([], int)

    # Keep maximum frequent occurring words
    frequent_words = [val for val, freq in vocab_frequency_tuple][:max_features]

    # Process each file
    for idx, data in enumerate(df['Phrase'].tolist()):
        if sentiment_list[idx] not in [0, 4]:
            continue

        # Pre-Process data word level
        preprocessed_word = data_preprocessing(data)

        # Create data
        truncated_review = []
        for each_word in preprocessed_word:
            # Take words which are frequent
            if each_word in frequent_words:
                try:
                    truncated_review.append(vocab_to_index[each_word])
                    if len(truncated_review) >= max_word:
                        break
                except Exception as exc:
                    print(
                        '[Exception] if Key word not present in vocab dict but present in frequent words its a bug: {0}'.format(
                            exc))

        # Pad appropriately if less words are present
        word_len = len(truncated_review)
        if word_len:
            if word_len < max_word:
                truncated_review += [0] * (max_word - word_len)
            if len(input_data) != 0:
                input_data = np.vstack((input_data, truncated_review))
            else:
                input_data = np.hstack((input_data, truncated_review))

            if sentiment_list[idx] == 4:
                target_data.append(1)
            else:
                target_data.append(0)

    # conver target to numpy array
    target_data = np.array(target_data)

    data_dict = {'input': input_data, 'target': target_data}
    with open(train_dir, 'wb') as f:
        pickle.dump(data_dict, f)

    print('Max value in test: ', data_dict['input'].max(1).max())
    print('Input shape ', data_dict['input'].shape)
    print('Target shape ', data_dict['target'].shape)
    print('Successfully saved data to {0}'.format(train_dir))


if __name__ == '__main__':
    _test_process_imdb_data()

    # # Test twitter and Rotten tomato data
    # _test_twitter_data()