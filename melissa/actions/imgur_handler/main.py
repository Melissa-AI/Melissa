import os
import sqlite3
from datetime import datetime
from imgurpython import ImgurClient

# Melissa
from melissa.profile import data

WORDS = {'image_uploader': {'groups': ['upload']},
         'show_all_uploads': {'groups': [['all', 'uploads'],
                                         ['all', 'images'], ['uploads']]}}


class ImgurHandler():

    def __init__(self):
        self.client = ImgurClient(
            data['imgur']['client_id'],
            data['imgur']['client_secret']
        )

    def img_list_gen(self):
        image_list = []
        valid_image_extensions = [".tiff", ".png", ".gif", ".jpg"]
        for root, _, files in os.walk(data['images_path']):
            for filename in files:
                if os.path.splitext(filename)[1] in valid_image_extensions:
                    image_list.append(os.path.join(root, filename.lower()))
        return image_list

    def image_uploader(self, speech_text):
        if data['imgur']['client_id'] == "xxxx" \
            or data['imgur']['client_secret'] == "xxxx":
            msg = 'upload requires a client id and secret'
            print msg
            return msg

        words_of_message = speech_text.split()
        words_of_message.remove('upload')
        cleaned_message = ' '.join(words_of_message)
        if len(cleaned_message) == 0:
            return 'upload requires a picture name'

        image_listing = self.img_list_gen()

        for i in range(0, len(image_listing)):
            if cleaned_message in image_listing[i]:
                result = self.client.upload_from_path(
                    image_listing[i], config=None,
                    anon=True
                )

                conn = sqlite3.connect(data['memory_db'])
                conn.execute(
                    "INSERT INTO image_uploads "
                    "(filename, url, upload_date) VALUES (?, ?, ?)", (
                        image_listing[i], result['link'],
                        datetime.strftime(datetime.now(), '%d-%m-%Y')
                    )
                )
                conn.commit()
                conn.close()

                print result['link']
                return 'Your image has been uploaded'

    def show_all_uploads(self, text):
        conn = sqlite3.connect(data['memory_db'])
        cursor = conn.execute("SELECT * FROM image_uploads")

        for row in cursor:
            print(row[0] + ': (' + row[1] + ') on ' + row[2])
        conn.close()
        return 'Requested data has been printed on your terminal'
