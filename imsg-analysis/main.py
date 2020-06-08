import pandas as pd
from pathlib import Path

## MESSAGES CSV ##
msg_df = pd.read_csv('../data/messages.csv')
print('-- MESSAGE TABLE')
# you can print the entire DataFrame, or just the head/tail (5 rows each)
print(msg_df)
print(msg_df.head())
print(msg_df.tail())
# print the shape of the DataFrame
# need the str() around the shape attribute because it is a tuple, not a string
print('SHAPE: ' + str(msg_df.shape))
# print the column names
# msg_df.columns is an Index object, so printing it directly is a bit ugly
print('UGLY COLUMNS: ')
print(msg_df.columns)
# instead we can build a list from it, and print it that way
print('NICE COLUMNS:')
print('COLUMNS: ' + str([x for x in msg_df.columns]))

## ATTACHMENTS CSV ##
# not as interesting, so won't print as much
# connected to messages csv by a common "message_id" field
attach_df = pd.read_csv('../data/attachments.csv')
print('-- ATTACHMENT TABLE')
print('SHAPE: ' + str(attach_df.shape))
print('COLUMNS: ' + str([x for x in attach_df.columns]))
