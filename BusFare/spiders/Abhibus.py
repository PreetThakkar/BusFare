from scrapy.utils.response import open_in_browser
import scrapy
import json
from datetime import datetime, timedelta


class AbhibusSpider(scrapy.Spider):
	name = 'Abhibus'
	# Starting point
	start_urls = ['https://www.abhibus.com/bus_search/Delhi/344/Manali/1777/31-07-2020/O']
	# Form Request path to gather bus fare
	seatlayout_url = 'https://www.abhibus.com/seatlayout'
	# Form Data required to get each travel agent's bus seat layout
	form_data = {"rid": "", "sourceid": "344", "destination": "1777", "jdate": "", "concession": ""}

	def parse(self, response):
		# Gather data for next few(3) days
		dates = []
		today = datetime.today()
		for i in range(3):
			temp = today + timedelta(i)
			dates.append(temp.strftime("%Y-%m-%d"))
		# print(f'*****\nDates: \t{dates}*****\n')
		for i in dates:
			# Access path to list all the travel agents for particular date
			print(f'https://www.abhibus.com/getonewayservices/{i}/344/1777')
			request_main = scrapy.http.JsonRequest(f'https://www.abhibus.com/getonewayservices/{i}/344/1777', callback=self.parse_main_page)
			request_main.cb_kwargs['date'] = i # pass argument with object
			yield request_main

	def parse_main_page(self, response, date):
		raw = json.loads(response.body.decode())
		service_list = raw['serviceDetailsList']
		for agent in service_list:
			rid = agent['serviceKey'] # Identify unique key to pass as Form Data
			self.form_data['rid'] = rid
			self.form_data['jdate'] = date
			# Gather seat layout information
			agent_request =  scrapy.http.FormRequest(self.seatlayout_url, callback=self.parse_seat_layout, formdata=self.form_data)
			agent_request.cb_kwargs['date'] = date
			agent_request.cb_kwargs['rid'] = rid
			agent_request.cb_kwargs['complete_detail'] = agent
			yield agent_request


	def parse_seat_layout(self, response, date, rid, complete_detail):
		# yeild the final output
		item = self.format_fare(response.css('a.tooltip::attr(title)').extract())
		yield {
			'timestamp': str(datetime.now()),
			'date': date,
			'rid': rid,
			'travelerAgentName': complete_detail['travelerAgentName'],
			'seat': item
		}


	def format_fare(self, listt):
		ret = []
		for i in listt:
			temp = i.split('|')
			ret.append({temp[0].split(" ")[1].strip(): temp[1].split(":")[1].strip()})
		return ret
