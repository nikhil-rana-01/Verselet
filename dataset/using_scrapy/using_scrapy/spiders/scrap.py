import csv
import scrapy

class Get_Poems(scrapy.Spider):
	name = "poems"
	durations = [ [1050,1375] , [1375,1700], [1700,1900] , [1900, 2021]  ]
	author_name_to_era = {}

	start_urls = ["http://kavitakosh.org/kk/index.php"]
	def parse(self, response):
		authors = response.css("div.poet-list-section")
		file = open('dataset.csv', mode='w')
		poem_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		author_links = response.css('div.poet-list-section a::attr(href)').getall()
		for author_link in author_links:
			complete_link = "http://kavitakosh.org" + author_link
			yield scrapy.Request(complete_link, self.parse_authors)

	def parse_authors(self, response):
		does_author_info_exist = response.css('div.kkparichay-box').get()
		if does_author_info_exist is not None:
			author_info = response.css('div.kkparichay-box li a::attr(href)').getall()
			author_name = response.css('span#kkparichay-name::text').get()
			author_date = response.css('div.kkparichay-box table.wikitable td::text')[0].get().split()[-1]
			author_name = author_name.strip()
			self.author_name_to_era[author_name] = author_date

			
			poem_of_author_links = response.css('li a::attr(href)').getall()
			for poem_link in poem_of_author_links:
				complete_link = "http://kavitakosh.org" + poem_link
				yield scrapy.Request(complete_link, self.parse_poems)

	def parse_poems(self, response):
		author_poem = response.css('h1.firstHeading span::text').get()
		if( author_poem is not None ):
			author_poem = author_poem.split('/', 2)

			if( len(author_poem) > 1 ):
				author_name = author_poem[1]
				poem_name = author_poem[0]
				
				author_name = author_name.strip()
				poem_name = poem_name.strip()

				with open("all.txt", 'a') as file:
					file.write(poem_name + "~" + author_name + "\n")
				
				poem_exist = response.css('div.poem').get()
				if poem_exist is not None:
					with open("poem_exist.txt", 'a') as file:
						file.write(poem_name + "~" + author_name + "\n")
					poem_lines = response.css('div.poem p::text').getall()
					poem = ""
					if poem_lines is not None:
						for line in poem_lines:
							line = line.strip()
							poem += line
						poem = poem.strip()

						if poem != "":
							with open("collection.txt", 'a') as file:
								file.write(author_name  + "~"+ self.author_name_to_era[author_name]  + "~" + poem_name + "~" + poem +"~" + "\n")


