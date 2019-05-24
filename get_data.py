import json
import requests
import sys

def page_number_range(page_number):
	upper_lim = page_number * 100
	lower_lim = (page_number * 100) - 99

	rank_range = "%d-%d" % (lower_lim,upper_lim)

	return rank_range

def get_data(page_number):

	rank_range = page_number_range(page_number)

	url_str = "http://api.skidstorm.cmcm.com/v2/rank/list/%s/ALL" % (rank_range)

	response_obj = requests.get(url_str)

	if response_obj.status_code == 200:
		json_dump = response_obj.json()

		#print(json_dump)

		return json_dump

	else:
		error_str = "{status:ERROR}"
		return error_str

def main():
	get_data(1)

if __name__ == '__main__':
	main()
