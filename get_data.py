import json
import requests
from bottle import run, route


class Skidstorm_App:
	def page_number_range(page_number):
		upper_lim = page_number * 100
		lower_lim = (page_number * 100) - 99

		rank_range = "%d-%d" % (lower_lim,upper_lim)

		return rank_range

	@route('/get_data/<page_number>')
	def get_data(page_number):

		page_number = int(page_number)
		upper_lim = page_number * 100
		lower_lim = (page_number * 100) - 99

		rank_range = "%d-%d" % (lower_lim,upper_lim)

		#rank_range = self.page_number_range(int(page_number))

		url_str = "http://api.skidstorm.cmcm.com/v2/rank/list/%s/ALL" % (rank_range)

		response_obj = requests.get(url_str)

		if response_obj.status_code == 200:
			json_dump = response_obj.json()

			return json_dump

		else:
			error_str = "{status:ERROR}"
			return error_str

def main():

	run(host='localhost', port=9000, debug=True)

if __name__ == '__main__':
	main()
