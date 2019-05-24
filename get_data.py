import json
import requests
import os
from bottle import run, route


class Skidstorm_App:

	def __init__(self):
		self.url_str_prefix = "http://api.skidstorm.cmcm.com/v2/"

	def page_number_range(self,page_number):
		upper_lim = page_number * 100
		lower_lim = (page_number * 100) - 99

		rank_range = "%d-%d" % (lower_lim,upper_lim)

		return rank_range

	def get_index(self):
		web_str = "<h1>Drift Revolution is #1</h1>\n \
		<h1>Drift Revolution Fresher is also #1</h1>\n \
		<h5>Rush is #3</h5>"
		return web_str

	#@route('/players/<num_players>')
	#def get_player_data(num_players):
		
	def get_data(self,page_number=1):


		rank_range = self.page_number_range(int(page_number))

		full_url_str = self.url_str_prefix + "rank/list/%s/ALL" % (rank_range)

		response_obj = requests.get(full_url_str)

		if response_obj.status_code == 200:
			json_dump = response_obj.json()

			return json_dump

		else:
			error_str = "{status:ERROR}"
			return error_str

def main():

	skid_app = Skidstorm_App()

	route('/get_data/<page_number>')(skid_app.get_data)
	route('/')(skid_app.get_index)

	if os.environ.get('APP_LOCATION') == 'heroku':
		run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
	else:
		run(host='localhost', port=8080, debug=True)

	#run(host='localhost', port=9000, debug=True)

if __name__ == '__main__':
	main()
