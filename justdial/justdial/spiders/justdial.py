import scrapy
from bs4 import BeautifulSoup as BS
import sqlite3



class JDSpider(scrapy.Spider):
	name = "justdialspider"
	links = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


	def init_db(self):
		conn = sqlite3.connect('test.db')
		conn.execute("""CREATE TABLE justdial_data
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         ADDRESS        CHAR(50),
         PHONE         TEXT);""")

		conn.execute("""CREATE TABLE justdial_links
         (ID INT PRIMARY KEY     NOT NULL,
         URL           TEXT    NOT NULL,
         PROCESSED     BOOLEAN);""")

		conn.close()
		print("******** DB Created")

	def insert_to_db(self, table, fields, values):
		conn = sqlite3.connect('test.db')
		try:
			values = [ '"' + i + '"' for i in values]
			# values = map(lambda x: '"' +  x + '"', values)
			query = "INSERT INTO %s (%s) VALUES (%s)"%(table, ",".join(fields), ",".join(values) )
			conn.execute(query);
		except Exception as e:
			import pdb; pdb.set_trace()
			raise e
		conn.close()

	def start_requests(self):
		# self.init_db()
		urls = ['https://www.justdial.com/Bangalore/Car-Washing-Services']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

	def parse(self, response):
		soup = BS(response.body)
		try:
			next_link = soup.find('a', rel="next").get('href')		
		except Exception as e:
			print "\n\n--- next link Exception "
			import pdb; pdb.set_trace()
			print "Exception " + e.message
			next_link = False

		id_num = 0
		for i in  soup.find_all("h4", { "class" : "store-name" }):

			try:
				value = i.find('a').get('href')
				id_num += 1
				self.insert_to_db('justdial_links', ['ID', 'URL', 'PROCESSED'], [str(id_num), value, "0" ])		
			except Exception as e:
				import pdb; pdb.set_trace()
				print "\n\n-------exception"
				print "Failed processing tag " + str(i)


		if next_link:
		 	yield scrapy.Request(url=next_link, callback=self.parse, headers=self.headers)
		
		# page = response.url.split("/")[-2]
		# filename = '/Users/sarah/projects/sailesh/justdial/justdial-%s.html' % page
		# with open(filename, 'wb') as f:
		#     f.write(response.body)
		# self.log('Saved file %s' % filename)

		
