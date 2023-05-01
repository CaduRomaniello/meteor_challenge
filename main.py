import cv2
import numpy

# defining some constants to represent colors and image elements
PURE_WHITE = (255, 255, 255); STAR = (255, 255, 255)
PURE_RED = (0, 0, 255); METEOR = (0, 0, 255)
PURE_BLUE = (255, 0, 0); OCEAN = (255, 0, 0)
PURE_BLACK = (0, 0, 0); GROUND = (0, 0, 0)
OTHER = (1, 1, 1)

# dict to represent morse code (this were my bet to find the hidden phrase)
MORSE_CODE = { 'A':'.-',    'B':'-...',  'C':'-.-.',   
               'D':'-..',   'E':'.',     'F':'..-.',   
               'G':'--.',   'H':'....',  'I':'..',     
               'J':'.---',  'K':'-.-',   'L':'.-..',   
               'M':'--',    'N':'-.',    'O':'---',    
               'P':'.--.',  'Q':'--.-',  'R':'.-.',    
               'S':'...',   'T':'-',     'U':'..-',    
               'V':'...-',  'W':'.--',   'X':'-..-',   
               'Y':'-.--',  'Z':'--..',  '1':'.----',  
               '2':'..---', '3':'...--', '4':'....-',  
               '5':'.....', '6':'-....', '7':'--...',  
               '8':'---..', '9':'----.', '0':'-----' }


# reading image 
image = cv2.imread('meteor_challenge_01.png')

# getting image size
row = image.shape[0]
col = image.shape[1]

# auxiliar variables to count the desired values
matrix = []
total_stars = 0
total_meteors = 0
fall_on_water = 0

# auxiliar variables to try to find the hidden phrase
meteor_line = numpy.zeros(col)
star_line = numpy.zeros(col)
ocean_line = numpy.zeros(col)

# here we start looking on each pixel of the image to look for the objects defined above
# we start to iterate im each column to optimize the code and make multiple tasks at the same time
for j in range(col):
    # those variables will help us to find the number of meteors that will fall on the ocean
    has_meteor = False
    has_ocean = False
    meteors_in_column = 0
    for i in range(row):
        if image[i, j, 0] == PURE_WHITE[0] and image[i, j, 1] == PURE_WHITE[1] and image[i, j, 2] == PURE_WHITE[2]: #looking for a star
            star_line[j] = 1 # saying that we found a star in this coloumn (this will help to try to find the hidden phrase)
            
            total_stars += 1 # counting the number of stars

        elif image[i, j, 0] == PURE_RED[0] and image[i, j, 1] == PURE_RED[1] and image[i, j, 2] == PURE_RED[2]: #looking for a meteor
            has_meteor = True  # saying that we found a meteor in this column (this will help us find if this meteor will fall in the ocean)
            meteors_in_column += 1 # counting how many meteors are in this column

            meteor_line[j] = 1 # saying that we found a meteor in this column (this will help to try to find the hidden phrase)
            
            total_meteors += 1 # counting the number of meteors

        elif image[i, j, 0] == PURE_BLUE[0] and image[i, j, 1] == PURE_BLUE[1] and image[i, j, 2] == PURE_BLUE[2]: #looking for ocean
            has_ocean = True # saying that we found a ocean part in this column (this will help us find if a meteor will fall in this part of the ocean)

            ocean_line[j] = 1 # saying that we found a ocean part in this column (this will help to try to find the hidden phrase)

        else:
            # we aren't interested in other parts of the image
            print('', end='')

    # after looking all this column we check if meteors will fall on the ocean
    if has_meteor and has_ocean:
            fall_on_water += meteors_in_column

# here we will try to find the hidden phrase looking for morse codes
# the logic is:
#   - if we have a meteor and a star int the same column we have a '-' in morse code
#   - if we have a meteor or a star int the same column we have a '.' in morse code
#   - if we have none of them we start looking for the next symbol
#
# with this method i only found 169 characters, missing 6
hidden_phrase = ''
code = ''
for i in range(len(star_line)):
    
    if (star_line[i] == 1 and meteor_line[i] == 1):  # meteor and star in the same column
        code += '-'
    elif (star_line[i] == 1 or meteor_line[i] == 1): # meteor or star in this column
        code += '.'                                  
    else:                                            # nothing on this column
        if code != '':
            for key in MORSE_CODE:
                if MORSE_CODE[key] == code:
                    hidden_phrase += key
                    break

            code = ''

print(f'Total stars                              : {total_stars}')
print(f'Total meteors                            : {total_meteors}')
print(f'Total meteors that will fall on the ocean: {fall_on_water}')
print(f'Hidden phrase                            : {hidden_phrase}')