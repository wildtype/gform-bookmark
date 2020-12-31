#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import gspread
import os
import lxml.html
from datetime import datetime
import pytz


def convert_to_iso(timestring):
    timestamp = datetime.strptime(timestring, '%d/%m/%Y %H:%M:%S')
    timestamp_iso = pytz.timezone('Asia/Jakarta'
                                  ).localize(timestamp).isoformat()
    return timestamp_iso


def split_tags(tagstring):
    return [tag.strip() for tag in tagstring.split(',') if len(tag) > 0]


service_account_file = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
spreadsheet_url = \
    'https://docs.google.com/spreadsheets/d/1s4eauN3H5FOozO-RNzedUfIQMC2_xfLi6zTv-l2dTQg'

service = gspread.service_account(service_account_file)
document = service.open_by_url(spreadsheet_url)
sheet = document.sheet1

rows = sheet.get_all_values()
result = [{
    'timestamp': convert_to_iso(data[0]),
    'url': data[1],
    'title': data[2],
    'description': data[3],
    'tags': split_tags(data[4]),
    } for data in rows[1::]]

with open('template/index.html', 'r') as template_file:
    template_string = template_file.read()

template_doc = lxml.html.fromstring(template_string)
data_container = template_doc.cssselect('#bookmark-data')[0]

data_container.text = json.dumps(result)

result_html = lxml.html.tostring(template_doc).decode('utf-8')
with open('public/index.html', 'w') as result_file:
    result_file.write(result_html)
