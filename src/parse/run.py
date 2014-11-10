import get_files as get_files
import parse_files as parse_files
import sys
import getopt

# run download
# get_files.run_download()

# run parse
# parse_files.run_parse()


class Pusher:

    def push(self, org_dict):
        pass


def main(argv):
    action = ''
    try:
        action = str(argv[0])
    except Exception:
        print "Note. options are download or parse"
        sys.exit(2)
    if action == 'download':
        get_files.run_download()
    elif action == 'parse':
        parse_files.run_parse(Pusher())
    else:
        print "Nothing to do. options are download or parse"


if __name__ == "__main__":
    main(sys.argv[1:])
