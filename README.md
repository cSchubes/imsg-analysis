# iMessage Analysis
Credit to:
https://stmorse.github.io/journal/iMessage.html
https://www.wired.com/2013/11/backup-sms-iphone/
https://www.richinfante.com/2017/3/16/reverse-engineering-the-ios-backup#messages

## Data Format (after export)
There are three components:

### messages.csv
Giant csv file where all messages are stored. This includes messages including 
or entirely made up of an attachment like an image, video, or gif. 

There are 11 fields I chose to export. Not all are important for basic analysis.
The ones that matter are:
- **message_id**: unique ID of the message. Ties to elements in the attachments csv.
- **text**: self explanatory
- **date**, **date_delivered**, **date_read**: also self explanatory. These are in seconds
  past Jan. 1, 2001.
- **is_from_me**: Boolean indicating whether this message was sent by the person who made the 
  backup (me)
- **cache_has_attachments**: Fairly certain this is a boolean that indicates whether the message
  has/is an attachment or not.

The handle id is a unique ID that maps to a person's phone number.

### attachments.csv
Smaller csv file where attachment information is stored. There are 8 fields and again not all are
important. The ones that matter are:
- **message_id**: ties to a message in the messages csv. If a message has an attachment, you can look
  up that attachment using the common message id field.
- **filename**: Self explanatory. A strange sequence of letters and numbers due to Apple computing SHA1
  hashes on the attachment filepaths during backup. Maps to a file stored in the attachments/ folder.
- **attachment_id**: unique id for the attachment. Useful only in creating a unique index for each
  attachment in the csv, since some messages generate multiple entries in the attachment table.
- **created_date**: Date the attachment was created, I think. Separate from message date.
- **is_outgoing**: Same as **is_from_me** I think. Shouldn't need anyway since you can just look 
  at the message.

### attachments/ folder
All attachments referenced in the attachments csv are stored here. Names are derived from SHA1 hashes
computed during the backup procedure on their original filepaths on your phone.

## Setup
I recommend using Python 3.8 (newest), though anything > 3.5 should be fine.

The only external package requirement for now is Pandas. Definitely use 1.0 or greater (newest is 1.0.4).

## Use
`main.py` contains starter code that loads the csv files into Pandas DataFrames and prints a few things.
This code runs as a standalone script but should also work in a notebook. 

The filepaths used for loading assume your data is stored in a directory called `data/` at the root of this repository.

