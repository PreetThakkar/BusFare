from scrapy.utils.response import open_in_browser
import scrapy
import json
from datetime import datetime, timedelta


class AbhibusSpider(scrapy.Spider):
    name = 'Abhibus'
	start_urls = ['https://www.abhibus.com/bus_search/Delhi/344/Manali/1777/31-07-2020/O']
	seatlayout_url = 'https://www.abhibus.com/seatlayout'
	form_data = {"rid": "", "sourceid": "344", "destination": "1777", "jdate": "", "concession": ""}

	def parse(self, response):
		dates = []
		today = datetime.today()
		for i in range(3):
			temp = today + timedelta(i)
			dates.append(temp.strftime("%Y-%m-%d"))
		print(f'\t{dates}')
		for i in dates:
			print(f'https://www.abhibus.com/getonewayservices/{i}/344/1777')
			request_main = scrapy.http.JsonRequest(f'https://www.abhibus.com/getonewayservices/{i}/344/1777', callback=self.parse_main_page)
			request_main.cb_kwargs['date'] = i
			yield request_main

	def parse_main_page(self, response, date):
		raw = json.loads(response.body.decode())
		service_list = raw['serviceDetailsList']
		for agent in service_list:
			rid = agent['serviceKey']
			self.form_data['rid'] = rid
			self.form_data['jdate'] = date
			# print('\t', rid, date)
			agent_request =  scrapy.http.FormRequest(self.seatlayout_url, callback=self.parse_seat_layout, formdata=self.form_data)
			agent_request.cb_kwargs['date'] = date
			agent_request.cb_kwargs['rid'] = rid
			agent_request.cb_kwargs['complete_detail'] = agent
			yield agent_request


	def parse_seat_layout(self, response, date, rid, complete_detail):
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
