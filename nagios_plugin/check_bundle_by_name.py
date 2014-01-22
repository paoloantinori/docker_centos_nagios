#!/usr/bin/env python

"""Nagios plugin to check a bundle state providing the bundle name.
   Based on pyjolokia - https://github.com/cwood/pyjolokia/"""

from pyjolokia import Jolokia, JolokiaError
from optparse import OptionParser
import sys, os

# Standard Nagios return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

mbean = 'osgi.core:type=bundleState,version=1.5'


# Enter the jolokia url
j4p = None


nagios_work_folder = '/var/log/nagios/spool'
lock_file = nagios_work_folder + "/_.lock"


parser = OptionParser("usage: %prog [options] bundle_canonical_name")


def create_dictionary() :

    # Put in the type, the mbean, or other options. Check the jolokia users guide for more info
    # This then will return back a python dictionary of what happend to the request
    try: 
        data = j4p.request(type = 'exec', mbean=mbean, operation='listBundles')

        value = data["value"]

        for id in value.keys():
            bundle = value[id]
            name = bundle["SymbolicName"]

            f = open("%s/%s.pid" % (nagios_work_folder, name), "w")
            f.write(id)
            f.close()

        create_lock()

    except JolokiaError as e:
        print str(e)
        sys.exit(UNKNOWN)

def check_state(bundle_name):
    bundle_id = read_bundle_id(bundle_name)
    if bundle_id == None:
        return None
    state = j4p.request(type = 'exec', mbean=mbean, operation='getState', arguments = [bundle_id])
    return state["value"]

def read_bundle_id(bundle_name):
    try:
        filename="%s/%s.pid" % (nagios_work_folder, bundle_name)
        f = open(filename, "r")
        bundle_id = f.read()
        f.close()
        return bundle_id
    except:
        return None

def dictionary_exists():
    try:
        open(lock_file, 'r').close()
        return True
    except:
        return False

def create_lock():
    f =open(lock_file, 'a').close()
    print "Created lock file: %s" % lock_file

def release_lock():
    if os.path.isfile(lock_file):
        os.remove(lock_file)
        print "Released lock file: %s" % lock_file


def configure_options():
    parser.add_option( "--reset",
                       "-r",
                       action="store_true",
                       dest="reset",
                       default=False,
                       help="Reset the helper files that keep track of bundles ids")
    parser.add_option( "--user",
                       "-u",
                       action="store",
                       dest="user",
                       default=None,
                       help="Specify username")
    parser.add_option( "--password",
                       "-p",
                       action="store",
                       dest="password",
                       default=None,
                       help="Specify password")

    return parser.parse_args()



def main():
    global j4p
    (options, args) = configure_options()

    if len(args) != 2:
        parser.print_help()
        sys.exit(UNKNOWN)

    if options.reset :
        release_lock()



    jolokia_endpoint = args[0]
    bundle_name = args[1]

    jolokia_username = options.user
    jolokia_password = options.password


    j4p = Jolokia(jolokia_endpoint)
    j4p.auth(httpusername=jolokia_username, httppassword=jolokia_password)
    


    if not dictionary_exists():
        create_dictionary()

    state = check_state(bundle_name)

    if state == "ACTIVE":
        print "OK - %s - %s" % (bundle_name, state)
        sys.exit(OK)
    elif state == "RESOLVED":
        print "CRITICAL - %s - %s" % (bundle_name, state)
        sys.exit(CRITICAL)
    elif state == None:
        print "UNKNOWN - Bundle %s not recognized" % bundle_name
        sys.exit(UNKNOWN)
    else:
        print "WARNING - %s - %s" % (bundle_name, state)
        sys.exit(WARNING)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Caught Control-C..."
        sys.exit(UNKNOWN)

