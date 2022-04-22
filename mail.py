#!/usr/bin/env python3

import sys
import os
import mailbox
import email
import re
import argparse
import glob
import uuid
import shutil
import datetime
import random

from email import policy, parser
import email
from bs4 import BeautifulSoup


def argparsing(exec_file):
    parser = argparse.ArgumentParser(exec_file)
    parser.add_argument("--input-dir",
                        dest='inputdir',
                        help="Input directory",
                        default=None,
                        type=str)
    parser.add_argument("--output-dir",
                        dest='outputdir',
                        help="Output directory",
                        default=None,
                        type=str)
    parser.add_argument("--search-field",
                        dest='searchfield',
                        help="Which field in the mail to search? E.g.: To, From, etc",
                        default=None,
                        type=str)
    parser.add_argument("--search-value",
                        dest='searchvalue',
                        help="Which value must match the search field in the mail? E.g.: my@example.com",
                        default=None,
                        type=str)
    return parser



def walk_the_dir(filedir):
    results = []

    for root, dirs, files in os.walk(filedir, topdown=True):
    #    for name in dirs:
    #        print("dirs:", os.path.join(root, name))
        for name in files:
            results.append(os.path.join(root, name))

    return results


def get_size_in_bytes(filepath):
    statinfo = os.stat(filepath)
    return statinfo.st_size


def print_email(msg):
    body = msg.get_body()
    if 'Content-Type' in body:
        body_content_type = body['Content-Type']

    print(body)

#    print(body_content_type)
#    if 'text/html' in body_content_type:
#        if 'charset="us-ascii"' in body_content_type:
#            soup = BeautifulSoup(str(body))
#
#            for p in soup.find_all('p'):
#                print(p.text)
#
#        elif 'charset="utf-8"' in body_content_type:
#            soup = BeautifulSoup(str(body))
#
#            for p in soup.find_all('p'):
#                print(p.text)
#
#        elif 'charset="iso-8859-1"' in body_content_type:
#            soup = BeautifulSoup(str(body), from_encoding='ISO-8859-1')
#
#            for p in soup.find_all('p'):
#                print(p.text)
#
#        else:
#            print(msg.get_body())
#            sys.exit(1)
#
#    else:
#        print(msg.get_body())


def select_matching_attachments(filepath_mail):
    attachments = glob.glob(filepath_mail + "-*")
    return attachments


def copy_file(src_fullpath, dst_dir, add_ext):
    base = os.path.basename(src_fullpath)

    dst_elems = []
    dst_elems.append(dst_dir)
    dst_elems.append("/")
    dst_elems.append(base)
    if add_ext:
        dst_elems.append(add_ext)

    src = src_fullpath
    dst = "".join(dst_elems)

    # Copy file
    print("Copy:", src, "->", dst)
    shutil.copy(src, dst)


def open_mailbox_and_select(filepath_mail, search_field, search_value, outputdir):
    msg = email.parser.BytesParser(policy=email.policy.default).parse(open(filepath_mail, 'rb'))

    if msg[search_field] and search_value in msg[search_field]:
        print("---")
        print(msg['To'])
        print(msg['From'])
        if 'Reply-To' in msg:
            print(msg['Reply-To'])

        print(msg.keys())
        print(msg['Date'])
        date_time_obj = datetime.datetime.strptime(msg['Date'],
                                    "%a, %d %b %Y %H:%M:%S %z")
        maildate = str(date_time_obj)

        print(filepath_mail)
        attachments = select_matching_attachments(filepath_mail)
        print(attachments)

        # Create unique postfix to dir
        uniqid = random.randint(10000, 99999)

        # Create subdir in output directory
        sub_output_dir = outputdir + "/" + maildate + "__" + str(uniqid)
        os.mkdir(sub_output_dir)

        # copy files
        copy_file(filepath_mail, sub_output_dir, ".eml")
        for a in attachments:
            copy_file(a, sub_output_dir, None)


def prepare_output_dir(outputdir):
    return os.path.isdir(outputdir)


def main():
    # Arguments parsing
    argparser = argparsing(os.path.basename(__file__))
    args = argparser.parse_args()

    if args.searchfield is None:
        print("No search field set.")
        sys.exit(1)

    if args.searchvalue is None:
        print("No search value set.")
        sys.exit(1)

    if args.outputdir is None:
        print("Output directory not set.")
        sys.exit(1)

    if not prepare_output_dir(args.outputdir):
        print("Output directory does not exist")
        sys.exit(1)

    filepath_mails = walk_the_dir(args.inputdir)

    for mfp in filepath_mails:
        # print(mfp, get_size_in_bytes(mfp), "bytes")

        # Quick skip extentions
        if mfp.lower().endswith('.xml') or \
            mfp.lower().endswith('.jpg') or \
            mfp.lower().endswith('.png') or \
            mfp.lower().endswith('.pdf') or \
            mfp.lower().endswith('.gif'):
            continue

        open_mailbox_and_select(mfp, 
                                args.searchfield,
                                args.searchvalue,
                                args.outputdir)


### MAIN
if __name__ == "__main__":
    main()


