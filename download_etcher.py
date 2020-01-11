import requests
from bs4 import BeautifulSoup

archive_url = "https://www.balena.io/etcher/"

def get_file_links():
	try:
		r = requests.get(archive_url)
		soup = BeautifulSoup(r.content, "html.parser")
		links = soup.findAll('a')
		file_links = [archive_url + link['href'] for link in links if link['href'].endswith('zip')]
		return 0, file_links
	except:
		return 1, []
