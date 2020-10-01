from PIL import Image
import pytesseract
import numpy as np
import cv2
import imagehash
import json


def card_rang(area_rang):
    crop_rang = image.crop(area_rang)
    crop_rang = crop_rang.convert('L')
    cv_rang = np.array(crop_rang)
    new_cv_rang = cv2.resize(cv_rang, None, fx=9, fy=9)
    rang = pytesseract.image_to_string(new_cv_rang, config="--psm 13")
    if rang[0] == '2':
        return '2'
    elif rang[0] == '3':
        return '3'
    elif rang[0] == '4':
        return '4'
    elif rang[0] == '5':
        return '5'
    elif rang[0] == '6':
        return '6'
    elif rang[0] == '7':
        return '7'
    elif rang[0] == '8':
        return '8'
    elif rang[0] == '9':
        return '9'
    elif rang[0] + rang[1] == '10':
        return '10'
    elif rang[0] == 'J':
        return 'Jack'
    elif rang[0] == 'Q':
        return 'Queen'
    elif rang[0] == 'K':
        return 'King'
    elif rang[0] == 'A':
        return 'Ace'


def card_suit(area_suit, h_h, h_s, h_d, h_c):
    crop_suit = image.crop(area_suit)
    hash_suit =  imagehash.average_hash(crop_suit)
    h = hash_suit - h_h
    s = hash_suit - h_s
    d = hash_suit - h_d
    c = hash_suit - h_c
    if min(h, s, d, c) == h:
        return 'Hearts'
    elif min(h, s, d, c) == s:
        return 'Spade'
    elif min(h, s, d, c) == d:
        return 'Diamond'
    elif min(h, s, d, c) == c:
        return 'Club'

def image_to_number(area_number):
    crop_image = image.crop(area_number)
    cv_image = np.array(crop_image)
    new_cv_image = cv2.resize(cv_image, None, fx=9, fy=9)
    number = pytesseract.image_to_string(new_cv_image, config="--psm 13")
    return number.split('\n')[0]

def image_to_number_2(area_number):
    crop_image = image.crop(area_number)
    cv_image = np.array(crop_image)
    new_cv_image = cv2.resize(cv_image, None, fx=9, fy=9)
    number = pytesseract.image_to_string(new_cv_image, config="-c tessedit_char_whitelist=0123456789")
    return number.split('\n')[0]


image = input('Please, input patj to the picture: ')
image = Image.open(image)
image = image.convert('L')

# Patterns for suit
# ---------------------------------------------
area_suit_club = (163, 650, 193, 680)  # крести
area_suit_spade = (394, 650, 424, 680)  # пики
area_suit_diamond = (279, 650, 309, 680)  # буби
area_suit_hearts = (533, 1326, 559, 1349)  # черви

crop_suit_club = image.crop(area_suit_club)
crop_suit_spade = image.crop(area_suit_spade)
crop_suit_diamond = image.crop(area_suit_diamond)
crop_suit_hearts = image.crop(area_suit_hearts)

hash_heart = imagehash.average_hash(crop_suit_hearts)
hash_spade = imagehash.average_hash(crop_suit_spade)
hash_diamond = imagehash.average_hash(crop_suit_diamond)
hash_club = imagehash.average_hash(crop_suit_club)
# ---------------------------------------------

future_json = {'Rate': '',
               'Player balance': '',
               'Total rate': '',
               'Pot': '',
               'Player cards': '',
               'Cards on the table': ''}
# Player cards
first_man_card_rang = (528, 1294, 557, 1326)
first_man_card_suit = (533, 1326, 558, 1349)
future_json['Player cards'] += card_rang(first_man_card_rang) + ' of ' \
                               + card_suit(first_man_card_suit, hash_heart, hash_spade, hash_diamond, hash_club) + '; '

second_man_card_rang = (600, 1288, 631, 1320)
second_man_card_suit = (600, 1321, 625, 1324)
future_json['Player cards'] += card_rang(second_man_card_rang) + ' of ' \
                               + card_suit(second_man_card_suit, hash_heart, hash_spade, hash_diamond, hash_club)

# Cards on table
first_table_card_rang = (163, 611, 191, 648)
first_table_card_suit = (163, 650, 193, 680)
future_json['Cards on the table'] += card_rang(first_table_card_rang) + ' of ' \
                                     + card_suit(first_table_card_suit, hash_heart, hash_spade, hash_diamond,
                                                 hash_club) + '; '

second_table_card_rang = (278, 611, 306, 648)
second_table_card_suit = (278, 650, 308, 680)
future_json['Cards on the table'] += card_rang(second_table_card_rang) + ' of ' \
                                     + card_suit(second_table_card_suit, hash_heart, hash_spade, hash_diamond,
                                                 hash_club) + '; '

third_table_card_rang = (394, 612, 422, 649)
third_table_card_suit = (393, 650, 423, 680)
future_json['Cards on the table'] += card_rang(third_table_card_rang) + ' of ' \
                                     + card_suit(third_table_card_suit, hash_heart, hash_spade, hash_diamond,
                                                 hash_club) + '; '

forth_table_card_rang = (510, 611, 538, 648)
forth_table_card_suit = (509, 650, 539, 680)
future_json['Cards on the table'] += card_rang(forth_table_card_rang) + ' of ' \
                                     + card_suit(forth_table_card_suit, hash_heart, hash_spade, hash_diamond, hash_club)

first_man_balance = (407, 1403, 459, 1429)
future_json['Player balance'] += image_to_number(first_man_balance) + "; "

second_man_balance = (50, 1195, 132, 1221)
future_json['Player balance'] += image_to_number(second_man_balance) + "; "

third_man_balance = (65, 921, 117, 947)
future_json['Player balance'] += image_to_number_2(third_man_balance)

pot = (406, 567, 459, 593)
future_json['Pot'] += image_to_number_2(pot)

total_rate = (414, 493, 467, 523)
future_json['Total rate'] += image_to_number(total_rate)

second_player_rate = (212, 1168, 267, 1193)
future_json['Rate'] += image_to_number(second_player_rate) + '; '

third_player_rate = (211, 896, 266, 922)
future_json['Rate'] += image_to_number(third_player_rate)

with open('data.json', 'w') as fp:
    json.dump(future_json, fp, indent=4)