import sys
import time

def slow_type(text, delay=0.002):
    """
    Yavaş yavaş yazı yazdıran fonksiyon (progressive typing efekti).
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_banner():
    # Renk kodları
    yellow = '\033[93m'
    blue = '\033[1;94m'
    cyan = '\033[1;96m'
    green = '\033[1;92m'
    red = '\033[1;91m'
    white = '\033[1;97m'
    bold = '\033[1m'
    blink = '\033[5m'    # Yanıp sönen efekt
    reset = '\033[0m'

    # Banner ASCII sanatı
    banner_art = rf'''
{yellow}
               \.   \.      __,-"-.__      ./   ./ 
           \.   \`.  \`.-'"" _,="=._ ""`-.'/  .'/   ./ 
            \`.  \_`-''      _,="=._      ``-'_/  .'/ 
             \ `-',-._   _.  _,="=._  ,_   _.-,`-' / 
          \. /`,-',-._"""  \ _,="=._ /  """_.-,`-,'\ ./ 
           \`-'  /    `-._  "       "  _.-'    \  `-'/ 
           /)   (         \    ,-.    /         )   (\ 
        ,-'"     `-.       \  /   \  /       .-'     "`-, 
      ,'_._         `-.____/ /  _  \ \____.-'         _._`, 
     /,'   `.                \_/ \_/                .'   `,\ 
    /'       )                  _                  (       `\ 
            /   _,-'"`-.  ,++|T|||T|++.  .-'"`-,_   \ 
           / ,-'        \/|`|`|`|'|'|'|\/        `-, \ 
          /,'             | | | | | | |             `,\ 
         /'               ` | | | | | '               `\ 
                            ` | | | ' 
                              ` | ' 
{reset}
'''

    title = f"{bold}{white}OBLIVION{reset} {blue}[{cyan}{sys.argv[0]}{blue}]{green}:{red}# {reset}"

    motto = f"{blink}{bold}{white}In the darkness, only the hunter prevails.{reset}"

    # Terminalde basmak
    print(title)
    slow_type(banner_art, delay=0.0008)   # ASCII banner'ı hafif yavaş basıyoruz
    print('\n')
    print(motto.center(80))                # Motto'yu ortalayıp blink efektle yazıyoruz
    print('\n')

# Eğer bu dosya doğrudan çalıştırılırsa:
if __name__ == "__main__":
    print_banner()
