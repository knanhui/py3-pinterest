from py3pin.Pinterest import Pinterest
import time
import requests
from requests.exceptions import ConnectionError
import os

countrSkip = 0
countrDnld = 0


# this can download images by url
def download_image(url, path):
    global countrSkip
    global countrDnld
    if os.path.isfile(path):
        countrSkip += 1
    else:
        nb_tries = 10
        while True:
            nb_tries -= 1
            try:
                # Request url
                r = requests.get(url=url, stream=True)
                break
            except ConnectionError as err:
                if nb_tries == 0:
                    raise err
                else:
                    time.sleep(1)
        if r.status_code == 200:
            countrDnld += 1
            print("Downloading " + url)
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)        


download_dir = './pinterest_images/'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

pinterest = Pinterest(email='your_email',
                      password='your_password',
                      username='your_username',
                      cred_root='cred_root')

boards = pinterest.boards()
for board in boards:
    target_board = board

    ##################
    # save pins in board not including section  
    if not os.path.exists(download_dir + target_board['name']):
        os.makedirs(download_dir + target_board['name'])

    # get all pins for the board
    board_pins = []
    pin_batch = pinterest.board_feed(board_id=target_board['id'])

    while len(pin_batch) > 0:
        board_pins += pin_batch
        pin_batch = pinterest.board_feed(board_id=target_board['id'])


    for pin in board_pins:
        if 'images' in pin:
            url = pin['images']['orig']['url']
            if not os.path.exists(download_dir + target_board['name'] + '/' + pin['title']):
                os.makedirs(download_dir + target_board['name'] + '/' + pin['title'])
            print(download_dir + target_board['name'] + '/' + pin['title'] + '/' + url.rsplit('/', 1)[-1])
            #download_image(url, download_dir + target_board['name'] + '/' + pin['title'] + '/' + url.rsplit('/', 1)[-1])


    ##################
    # get sections in board
    sections = pinterest.get_board_sections(board_id=target_board['id'])
    for section in sections:

        if not os.path.exists(download_dir + target_board['name'] + '/' + section['slug']):
            os.makedirs(download_dir + target_board['name'] + '/' + section['slug'])

        ##################
        # get pins in section        
        save_pins = []
        section_pins = pinterest.get_section_pins(section_id=section['id'])
        while section_pins:
            for sec_pin in section_pins:
                save_pins += section_pins
            section_pins = pinterest.get_section_pins(section_id=section['id'])

        print('\n')    

        for pin in save_pins:
            if 'images' in pin:
                url = pin['images']['orig']['url']
                if not os.path.exists(download_dir + target_board['name'] + '/' + section['slug'] + '/' + pin['title']):
                    os.makedirs(download_dir + target_board['name'] + '/' + section['slug'] + '/'+ pin['title'])
                print(download_dir + target_board['name'] + '/' + section['slug'] + '/' + pin['title'] + '/' + url.rsplit('/', 1)[-1])
                #download_image(url, download_dir + target_board['name'] + '/' + section['slug']  + '/' + pin['title'] + '/' + url.rsplit('/', 1)[-1])    

print("Existing files:" + str(countrSkip))
print("New files:" + str(countrDnld))