import get_files as get_files
import parse_files as parse_files
import sys
import getopt

import push.org_transformer as org_transformer
import push.data_pusher as data_pusher

# run download
# get_files.run_download()

# run parse
# parse_files.run_parse()


class Transformer:

    def transform(self, org_dict):
        #         key_list = [key for key in org_dict]
        #         org_list = [value for value in org_dict.values()]
        #         return key_list, org_list
        return org_dict


class Pusher:

    def push(self, org_dict):
        print org_dict


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
        parse_files.run_parse(Transformer(), Pusher())
    elif action == 'parse-and-push':
        parse_files.run_parse(
            org_transformer.OrgTransformer(), data_pusher.SolrDataPusher())
    else:
        print "Nothing to do. options are download or parse"


if __name__ == "__main__":
    main(sys.argv[1:])
