import importlib
import pkgutil
import sqlite3
import sys
import os

# Melissa
import profile

con = 0
cur = 0
modules = {}


def create_actions_db():
    try:
        cur.executescript("""
            CREATE TABLE expression (
              word varchar(50) PRIMARY KEY,
              word_order integer
            );

            CREATE TABLE words (
              word varchar(50),
              word_group varchar(255),
              word_order integer
            );

            CREATE INDEX word_index ON words (word);

            CREATE TABLE word_groups (
              word_group varchar(255),
              function varchar(255),
              word_count integer
            );

            CREATE INDEX word_group_index ON word_groups (word_group);

            CREATE TABLE functions (
              function varchar(255) PRIMARY KEY,
              threaded tinyint,
              returns tinyint,
              silent tinyint,
              priority integer DEFAULT 0
            );

            CREATE TABLE notifications (
              function varchar(255) PRIMARY KEY,
              poll_period integer
            );
            """)
        con.commit()
        
    except sqlite3.Error, err:
        print "Error %s:" % err.args[0]
        sys.exit(1)

    return True


def insert_words(name, words, priority):

    for function_name, fields in words.iteritems():
        function_name = name+' '+function_name

        if 'notification' in fields:
            if not 'poll_period' in fields:
                print "A poll_period is required for notifications " \
                      +function_name
                sys.exit(1)
            poll_period = int(fields['priority'])

            try:
                cur.execute(
                    "INSERT INTO notifications (function, "
                    +"poll_period) values ('{fn}',{pp})"
                    .format(fn=function_name, pp=poll_period))

            except sqlite3.Error, err:
                print "Error %s:" % err.args[0]
                sys.exit(1)

        else: # An action function
            priority = 0
            if 'priority' in fields:
                int(fields['priority'])

            threaded = 0
            returns = 0
            silent = 0
            if 'properties' in fields:
                properties = fields['properties']
                if 'threaded' in properties:
                    threaded = 1
                if 'returns' in properties:
                    returns = 1
                if 'silent' in properties:
                    silent = 1

            try:
                cur.execute(
                    "INSERT INTO functions "
                   +"(function, priority, threaded, returns, silent) "
                   +"values ('{fn}',{p},{t},{r},{s})"
                   .format(fn=function_name, p=priority, t=threaded,
                           r=returns, s=silent))

            except sqlite3.Error, err:
                print "Error %s:" % err.args[0]
                sys.exit(1)

            for group in fields['groups']:
                if type(group) == type(''):

                    word = group.lower()

                    cur.execute(
                        "INSERT INTO word_groups "
                        +"(word_group, function, word_count) "
                        +"values ('{wg}','{fn}',{cnt})"
                        .format(wg=word, fn=function_name, cnt=1))

                    cur.execute(
                        "INSERT INTO words "
                        +"(word, word_group, word_order) "
                        +"values ('{w}','{wg}',{seq})"
                        .format(w=word, wg=word, seq=0))

                elif type(group) == type([]):
                    word_group_string = (' '.join(group)).lower()

                    cur.execute(
                        "INSERT INTO word_groups "
                        +"(word_group, function, word_count) "
                        +"values ('{wg}','{fn}',{cnt})"
                        .format(wg=word_group_string,
                                fn=function_name, cnt=len(group)))

                    for order in range(0, len(group)):

                        word = group[order].lower()
                        cur.execute(
                            "INSERT INTO words "
                            +"(word, word_group, word_order) "
                            +"values ('{w}','{wg}',{seq})"
                            .format(w=word, wg=word_group_string,
                                    seq=order))
        con.commit()


def assemble_actions_db():
    global con, cur, modules
    try:
        if profile.data['actions_db_file'] != ':memory:' \
        and os.path.exists(profile.data['actions_db_file']):
            os.remove(profile.data['actions_db_file'])

        con = sqlite3.connect(profile.data['actions_db_file'])
        con.text_factory = sqlite3.OptimizedUnicode
        cur = con.cursor()

    except sqlite3.Error, e:        
        print "Error %s:" % e.args[0]
        sys.exit(1)

    if create_actions_db():
        print 'Successfully Created '+profile.data['actions_db_file']

    package = importlib.import_module(profile.data['modules'])
    for finder, name, ispkg in pkgutil.walk_packages(package.__path__):
        print 'Loading module '+name
        try: 
            loader = finder.find_module(name)
            mod = loader.load_module(name)

        except:
            print "Skipped module '%s' due to an error." % name

        else:
            priority = mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0

            if hasattr(mod, 'WORDS'):
                insert_words(name, mod.WORDS, priority)
                modules[name] = mod

            else:
                print 'WARNING: Module will not be used.'
                print '    WORDS not found for module ' + name


if con == 0:
    assemble_actions_db()

