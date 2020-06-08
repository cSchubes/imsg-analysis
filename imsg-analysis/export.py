import os
import sqlite3
import csv
import shutil
from hashlib import sha1
from pathlib import Path

## SETUP ##
# name of msg db in iPhone backups
msg_db_name = "3d0d7e5fb2ce288813306e4d4636395e047a3d28"
# path to top level directory of backup data
root = Path("/media/carson/Carson Recovery/iPhone X Backups/07a3fff385b1a6b9ccf2b7fe4e119ee886474062")
# destination path
export_dest = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / 'data'
# make destination paths
os.makedirs(export_dest, exist_ok=True)
os.makedirs(export_dest / 'attachments', exist_ok=True)
# filepath to msg db
msg_db_path = root / msg_db_name[:2] / msg_db_name

## LOAD DB ## 
# connect
msg_db = sqlite3.connect(msg_db_path)
# get cursor for command execution
c = msg_db.cursor()

## BUILD MSG CSV ##
msg_fields = [
    'ROWID',
    'handle_id',
    'text',
    'date',
    'date_delivered',
    'date_read',
    'is_from_me',
    'cache_has_attachments',
    'associated_message_type',
    'expressive_send_style_id',
    'associated_message_range_length'
]
fields_str = ', '.join(msg_fields)
handle_id = 1020
# actual SQL command
msg_cmd = (f"SELECT {fields_str} FROM message T1 "
            f"WHERE handle_id={handle_id} "
            "ORDER BY date")
# retrieve messages
c.execute(msg_cmd)
# export to csv
labels = msg_fields
labels[0] = 'message_id'
with open(export_dest / 'messages.csv', 'w') as f:
    csv_f = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    csv_f.writerow(labels)
    csv_f.writerows(c)

## BUILD ATTACHMENTS CSV AND EXTRACT FILES ##
attachment_fields = [
    'created_date',
    'filename',
    'mime_type',
    'is_outgoing',
    'total_bytes',
    'is_sticker'
]
fields_str = ', '.join(attachment_fields)
# table id is based on attachment ID
attachment_cmd = (f"SELECT T2.ROWID, T1.ROWID, {fields_str} FROM message T1 "
                    "INNER JOIN attachment T2 "
                    "INNER JOIN message_attachment_join T3 "
                    "ON T2.ROWID=T3.attachment_id "
                    f"WHERE T3.message_id=T1.ROWID AND T1.handle_id={handle_id}")
# retrive messages
c.execute(attachment_cmd)
# export to csv
labels = ['attachment_id', 'message_id']
labels.extend(attachment_fields)
with open(export_dest / 'attachments.csv', 'w') as f:
    csv_f = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    csv_f.writerow(labels)
    for row in c:
        # must convert raw filepath to attachment hash
        raw_path = row[3]
        # first find Library in the path
        lib_ind = raw_path.find('Library')
        if lib_ind != -1:
            # convert for hashing
            path = 'MediaDomain-' + raw_path[lib_ind:] 
            # actual hash
            hash_name = sha1(path.encode())
            # construct path to file in the backup
            attachment_path = root / hash_name.hexdigest()[:2] / hash_name.hexdigest()
            # attempt to extract
            try:
                shutil.copy(attachment_path, export_dest / 'attachments')
            except Exception:
                print("Unable to find: " + path)
            # replace entry with hashed name
            # must completely remake tuple since they are immutable
            altered_row = row[0:3] + (hash_name.hexdigest(),) + row[4:]
            csv_f.writerow(altered_row)
        else:
            # if we cannot parse the path, just leave it and move on
            print('Cannot parse path: ' + raw_path)
            csv_f.writerow(row)
            continue
    