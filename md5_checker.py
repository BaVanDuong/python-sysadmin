#!/usr/bin/python

import hashlib
import sys
import optparse
import os
import threading
import time

class HashFile(threading.Thread):
    def __init__(self, fname, hash_type):
        super(HashFile, self).__init__()
        self.fname = fname
        self.hash_type = hash_type
        self.result = None
    def run(self):
        self.result =  self.hash_file().hexdigest()

    def hash_file(self):
        BLOCKSIZE = 65536
        hasher = getattr(hashlib, self.hash_type)()
        with open(self.fname, 'rb') as fin:
            buf = fin.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = fin.read(BLOCKSIZE)
        return hasher



def get_argv():
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='fin', help="File check")
    parser.add_option('-t', '--type', dest='hash_type',
                      type="string", default='md5', help="Hash type")
    parser.add_option('-c', '--checksum', dest='checksum', help='checksum')
    return parser.parse_args()


def main():
    HASH = ('md5', 'sha1', 'sha224', 'sha256', 'sha512', 'sha384')
    start = time.time()

    (options, args) = get_argv()
    fname = os.path.abspath(options.fin)
    hash_type = options.hash_type
    checksum = options.checksum

    if not os.path.exists(fname):
        print "File %s don't exists!" % fname
        sys.exit(0)
    if hash_type not in HASH:
        print 'Support hash type: md5, sha1, sha224, sha256, sha512, sha384'
        sys.exit(0)

    hash_file = HashFile(fname, hash_type)

    print 'Checking for %s ...' % (fname)
    hash_file.start()
    hash_file.join()
    result = hash_file.result
    end = time.time()
    print "Hash sum: ", result
    print "Result: ", result == checksum
    print "Checking time: %.2fs" % (end-start)


if __name__ == '__main__':
    sys.exit(main())
