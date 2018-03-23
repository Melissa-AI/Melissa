import sqlite3
from datetime import datetime

# Melissa
from melissa.profile import data


WORDS = {
    'show_all_notes': {
        'groups': [
            ['all', 'note'],
            ['all', 'notes'],
            'notes'
        ]
    },
    'note_something': {
        'groups': ['note']
    },
}


class Notes():

    def show_all_notes(self, text):
        conn = sqlite3.connect(data['memory_db'])
        notes = 'Your notes are as follows:'

        cursor = conn.execute("SELECT notes FROM notes")

        for row in cursor:
            notes = notes + row[0]

        conn.close()
        return notes

    def note_something(self, speech_text):
        conn = sqlite3.connect(data['memory_db'])
        words_of_message = speech_text.split()
        words_of_message.remove('note')
        cleaned_message = ' '.join(words_of_message)

        conn.execute("INSERT INTO notes (notes, notes_date) VALUES (?, ?)", (
            cleaned_message, datetime.strftime(datetime.now(), '%d-%m-%Y')))
        conn.commit()
        conn.close()

        return 'Your note has been saved.'
