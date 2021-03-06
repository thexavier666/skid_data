import json
import requests
import os
from bottle import run, route, static_file

class Skidstorm_App:

	def __init__(self,dummy_args):
		self.url_str_prefix = "http://api.skidstorm.cmcm.com/v2/"
		self.dummy_args = dummy_args

	def page_number_range(self,page_number):
		upper_lim = page_number * 100
		lower_lim = (page_number * 100) - 99

		rank_range = "%d-%d" % (lower_lim,upper_lim)

		return rank_range

	def get_dummy(self):
		return self.dummy_args

	def get_web_pages(self,filepath):
		return static_file(filepath, root="./public")
	
	def list_to_string(self,some_list):

		giant_str = ''

		for a_item in some_list:
			small_str = ''
			small_str = ','.join(a_item)
			small_str += '\n'

			giant_str += small_str

		print ("Main string")
		print (giant_str)

		return giant_str

	def get_data(self,page_number=1):

		rank_range = self.page_number_range(int(page_number))

		full_url_str = self.url_str_prefix + "rank/list/%s/ALL" % (rank_range)

		response_obj = requests.get(full_url_str)

		if response_obj.status_code == 200:
			json_dump = response_obj.json()

			print(type(json_dump))

			return json_dump

		else:
			error_str = "{status:ERROR}"
			return error_str

	def get_player_data(self,page_number=1):
		json_dump = self.get_data(page_number)

		player_dict = {}

		for each_player in json_dump["ranks"]:

			plr_username = each_player["username"]
			plr_clan_tag = each_player["clanTag"]
			plr_clan_id  = each_player["clanId"]
			plr_curr_trophy = each_player["rank"]
			plr_clan_rank = "<NO_CLAN_RANK>"

			if plr_clan_id == None:
				plr_clan_id = "<NO_CLAN_ID>"
				plr_clan_tag = "<NO_CLAN_TAG>"
			else:
				plr_profile = each_player["profile"]
				plr_clan = plr_profile["clan"]
				plr_clan_rank = str(plr_clan["clanScore"])

			player_dict[plr_curr_trophy] = ["Clan tag : " + plr_clan_tag, "Clan ID : " + plr_clan_id, "Username : " + plr_username, "Clan Score : " + plr_clan_rank]

		return player_dict

def main():

	skid_app = Skidstorm_App("100")

	route('/<filepath:path>')(skid_app.get_web_pages)
	route('/get_data/<page_number>')(skid_app.get_data)
	route('/dummy')(skid_app.get_dummy)
	route('/get_player_data/<page_number>')(skid_app.get_player_data)

	if os.environ.get('APP_LOCATION') == 'heroku':
		run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
	else:
		run(host='localhost', port=8080, debug=True)

if __name__ == '__main__':
	main()
