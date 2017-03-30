import os
import re
import sys
from subprocess import Popen, PIPE

db_user = os.environ.get('DB_USER')
database = os.environ.get('DATABASE')
db_host = os.environ.get('DB_HOST')

if db_user is None and database is None and db_host is None:
    sys.exit('Environment variables not set!')


def get_highest_number():

    """ checks scripts folder and returns script with highest number """

    scripts = {}
    list_of_scripts = os.listdir('scripts')
    for script in list_of_scripts:
        try:
            number = re.findall('\d+', script)[0]
            scripts[script] = int(number)
        except IndexError:
            print "{} does not seem to contain version number\n".format(script)

    script_filename = max(scripts.iterkeys(), key=(lambda key: scripts[key]))
    highest_number = scripts[script_filename]

    print "Script {} has the highest version number: {}".format(script_filename, highest_number)

    return scripts, highest_number


def get_database_version():

    """get highest version from version schema"""

    proc = Popen([
        'psql',
        '-U',
        '{}'.format(db_user),
        '-W',
        '{}'.format(database),
        '-f'
        'utils/read_example.sql',
        '-h'
        '{}'.format(db_host),
        '-w'], stdin=PIPE, stdout=PIPE, stderr=PIPE
    )

    output, err = proc.communicate()
    db_version = int(output.split('\n')[2])

    return db_version


def scripts_to_execute(db_version, scripts, highest_number):

    """Calculates scripts to execute based on db version and list of all script version values"""

    update = None

    for key, value in scripts.iteritems():
        if db_version < value:
            print "Executing: {} ...".format(key)
            Popen([
                'psql',
                '-U',
                '{}'.format(db_user),
                '-W',
                '{}'.format(database),
                '-c'
                'scripts/{}'.format(key),
                '-h'
                '{}'.format(db_host),
                '-w'], stdin=PIPE, stdout=PIPE, stderr=PIPE
            )
            update = True

    if update:
        upgrade_db_version(highest_number)
    else:
        print "Database does not need to be updated"
        return


def upgrade_db_version(highest_number):

    """Writes highest db version to table"""

    fmt = r"INSERT INTO databaseversion(Revision, Applied) VALUES ({}, NOW())"
    sql = fmt.format(highest_number)

    proc = Popen([
        'psql',
        '-U',
        '{}'.format(db_user),
        '-W',
        '{}'.format(database),
        '-c',
        sql,
        '-h'
        '{}'.format(db_host),
        '-w'], stdin=PIPE, stdout=PIPE, stderr=PIPE
    )

    print "Database version upgraded to {}".format(highest_number)


if __name__ == '__main__':
    scripts, highest_number = get_highest_number()
    db_version = get_database_version()

    print "Current database version is: {}\n".format(db_version)

    get_database_version()

    scripts_to_execute(db_version, scripts, highest_number)