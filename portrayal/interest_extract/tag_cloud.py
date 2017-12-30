# -*- coding: utf-8 -*-
import re

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

from .. config import PROJECT_PATH

file_path = PROJECT_PATH + "portrayal/resource/tag_cloud/"


def generate_tag_cloud(text, user_id):
	word_count = []
	word_list = text.split(',')
	length = len(word_list) * 2

	for word in word_list:
		word_count.append((word, length / 10))
		length -= 1

	tags = make_tags(word_count, maxsize = 48)

	for item in tags:
		item['tag'] = re.sub(r'label(\w+)label',r'#\1', item['tag'])

	file_name = file_path + '%d.png' % user_id
	create_tag_image(tags, file_name, size = (999, 688), fontname = 'Lobster',  background=(0, 0, 0, 0))

	return file_name