import importlib
import pkgutil
import sqlite3
import sys
import os

# Melissa
import profile
import words_db

# This code was adapted from Jasper's brain.py.

class Brain(object):

    # The order_match factor gives a higher score for word_groups
    # matched in order by the expression.
    order_match_factor = 1.5

    def __init__(self):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules.
        """

        self.modules = self.get_modules()

    @classmethod
    def get_modules(cls):
        """
        Dynamically load all the modules in the modules folder.
        """
        modules = {}
        package = importlib.import_module(profile.data['modules'])
        for finder, name, ispkg \
            in pkgutil.walk_packages(package.__path__):

            print 'Processing module '+name
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)

            except:
                print "Skipped module '%s' due to an error." % name

            else:
                if hasattr(mod, 'WORDS'):
                    modules[name] = mod

                else:
                    print "Skipped module '%s' because it misses "\
                         +"the WORDS constant." % name

        return modules                

    def query(self, text):
        """
        Processes the text against the words.sqlite DB to identify
        which module and function can be best applied.

        Arguments:
        text -- user input, typically speech
        """

        text_list = text.split() # Make a list of expression words

        # Make a list of lists where each sublist has an expression
        # word and its sequence in the expression.
        zlist = zip(text_list, list(range(len(text_list))))
        # print zlist

        # Clear the expression table for each new user expression.
        words_db.cur.execute('DELETE FROM expression')

        # Insert expression words in to SQLite. A word may appear more
        # than once in the expression. Only the first occurence will
        # be kept. 
        words_db.cur.executemany("INSERT OR IGNORE INTO expression "
                                 "values (?,?)", zlist)
        words_db.con.commit()

        # Match multiple-word groups against the expression words.
        sql = "SELECT e.word, e.word_order, "\
             +"  g.word_group, g.word_count, g.function "\
             +"FROM expression e "\
             +"JOIN words w "\
             +"ON w.word = e.word "\
             +"JOIN word_groups g "\
             +"ON g.word_group = w.word_group "\
             +"WHERE g.word_count > 1 "\
             +"ORDER BY e.word_order, g.word_group"
        # print sql
        words_db.cur.execute(sql)
        rows = words_db.cur.fetchall()
        # print rows

        scoring = {}
        for row in rows:
            # print row
            if not row[2] in scoring:
                # If the word_group is not already in the scoring
                # dictionary ...

                # Split word_group on spaces into a list.
                group_list = row[2].split()

                # If the row word is the first word in the group_list
                # set order to 1. 'order' checks to see if the words
                # in the word_group are matched in expression order.
                order = 1 if row[0] == group_list[0] else 0
                scoring[row[2]] = {
                    'group': group_list,
                    'score': 0.0,
                    'count': row[3],
                    'matched': 1,
                    'order': order,
                    'function': row[4]}
            else:
                # Update word_group already in the dictionary for
                # total words in the matched group.
                scoring_row = scoring[row[2]]
                scoring_row['matched'] += 1

                # And if the row word matches the next group word in 
                # order, add 1 to order.
                if row[0] ==\
                    scoring_row['group'][scoring_row['order']]:
                    scoring_row['order'] += 1

        # Score the word_groups according to the assembled match
        # results.
        top_scores = []
        for key, fields in scoring.iteritems():
            # A word_group can only enter scoring when all the words
            # in the group were matched. 
            if fields['matched'] == fields['count']:
                score = fields['count'] # Default score

                # Give a greater score if all the words in the group
                # where matched in order.
                if fields['order'] == fields['count']:
                    score = fields['count'] * self.order_match_factor

                # print score
                # If this word_group score is greater-than or equal-to
                # the current best score, prepend it to the top_scores
                # list.
                if len(top_scores) == 0 or score >= top_scores[0][1]:
                    top_scores.insert(0,[key, score, 
                                         fields['function']])
                # else bypass

        if len(top_scores) > 0:
            if len(top_scores) > 1 \
            and top_scores[0][1] == top_scores[1][1]:
                # If there is more than one of the same best score,
                # use a function's priority to choose between them.

                # Assemble a comma-separated string of the function
                # names to be used in the SELECT below to get the
                # priorities.
                top_score = top_scores[0][1]
                function_str = "'"+top_scores[0][2]+"'"
                for pos in range(1, len(top_scores)):
                    if top_scores[pos][1] != top_score:
                        break
                    function_str += ",'"+top_scores[pos][2]+"'"

                # print 'function_str: '+function_str
                qry = "SELECT function, priority "\
                     +"FROM functions "\
                     +"WHERE function IN ("+function_str+") "\
                     +"ORDER BY priority"

                # print qry
                words_db.cur.execute(qry)
                rows = words_db.cur.fetchall()
                # print rows

                # If the priorities of the first two rows are
                # different we have one best priority.
                if rows[0][1] != rows[1][1]:
                    print "Best priority function found: "+rows[0][0]

                # Otherwise there is more then one function with the
                # best priority. Choose the first returned and list
                # the functions having the same best priority.
                else:
                    print "\nThe first function in the following "\
                         +"having equal\n"\
                         +"priorities has been selected.\n"\
                         +"----------------------------------"
                    best_priority = rows[0][1]
                    for pos in range(0, len(rows)):
                        if rows[pos][1] != best_priority:
                            break;
                        print 'function: ('+rows[pos][0]\
                            +')  priority: '+str(rows[pos][1])

            # print top_scores[0]
            print "Run function '%s' \nfor word_group '%s' \nhaving score %4.2f"\
                  % (top_scores[0][2], top_scores[0][0],
                     top_scores[0][1])
            module_name, function = top_scores[0][2].split()
            # run function
            getattr(self.modules[module_name], function)(text)

        else:
            # If there are no matched multiple-word groups, get a
            # function with the greatest number of single word
            # matches.
            sql = "SELECT g.function, count(*) as words_matched, "\
                 +"    f.priority "\
                 +"FROM expression e "\
                 +"JOIN words w "\
                 +"ON w.word = e.word "\
                 +"JOIN word_groups g "\
                 +"ON g.word_group = w.word_group "\
                 +"JOIN functions f "\
                 +"ON g.function = f.function "\
                 +"WHERE g.word_count = 1 "\
                 +"GROUP BY g.function "\
                 +"ORDER BY word_count DESC, f.priority, g.function"
            # print sql
            words_db.cur.execute(sql)
            rows = words_db.cur.fetchall()
            if len(rows) == 1:
                print "Run function: '%s'  words : %d  priority: %d" \
                      % (rows[0][0], rows[0][1], rows[0][2])
                module_name, function = rows[0][0].split()
                # run function
                getattr(self.modules[module_name], function)(text)

            elif len(rows) > 1:
                if rows[0][1] == rows[1][1] \
                and rows[0][2] == rows[1][2]:
                    count = rows[0][1]
                    priority = rows[0][2]
                    print "These functions tied for best individual\n"\
                         +"word match count.\n"\
                         +"----------------------------------"
                    for pos in range(0, len(rows)):
                        if rows[pos][1] != count \
                        or rows[pos][2] != priority:
                            break
                        print "function: '%s'  words : %d  priority: %d"\
                               % (rows[pos][0], rows[pos][1],
                                  rows[pos][2])

                print "Run function " + rows[0][0]
                module_name, function = rows[0][0].split()
                # run function
                getattr(self.modules[module_name], function)(text)

            else:
                # If there are no single word or multiple word matches,
                # provide the 'I dont know what that means!' message.
                getattr(self.modules['general_conversations'],
                        'undefined')('')

