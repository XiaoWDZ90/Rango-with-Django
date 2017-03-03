import json
import urllib, urllib2
import requests, requests.utils
# Add your Microsoft Account Key to a file called bing.key

def read_bing_key():
	"""
	reads the BING API key from a file called 'bing.key'
	returns: a string which is either None, i.e. no key found, or with a key
	remember to put bing.key in your .gitignore file to avoid committing it to the repo.
	"""
	
	# See Python Anti-Patterns - it is an awesome resource to improve your python code
	# Here we using "with" when opening documents
	# http://docs.quantifiedcode.com/python-anti-patterns/maintainability/not_using_with_to_open_files.html
	
	bing_api_key = None
	try:
		with open('bing.key','r') as f:
			bing_api_key = f.readline()
	except:
		raise IOError('bing.key file not found')
		
	return bing_api_key
	

def run_query(search_terms):
	
	bing_api_key = read_bing_key()
	if not bing_api_key:
		raise KeyError('Bing Key Not Found')
	
	# Specify the base url and the service (Bing Search API 2.0)
	root_url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'
	# service = 'Web'

	# Specify how many results we wish to be returned per page.
	# Offset specifies where in the results list to start from.
	# With results_per_page = 10 and offset = 11, this would start from page 2.
	results_per_page = 10
	offset = 0

	# Wrap quotes around our query terms as required by the Bing API.
	# The query we will then use is stored within variable query.
	query = "{0}".format(search_terms)
	print "query : ",query
	# Turn the query into an HTML encoded string.
	# We use urllib for this - differences exist between Python 2 and 3.
	# The try/except blocks are used to determine which function call works.
	# Replace this try/except block with the relevant import and query assignment.
	
	
	# Construct the latter part of our request's URL.
	# Sets the format of the response to JSON and sets other properties.
	search_url = "{0}?q={1}".format(
		root_url,
		query)
	print "search url : ", search_url
	# Setup authentication with the Bing servers.
	# The username MUST be a blank string, and put in your API key!
	username = ''

	headers = {'Ocp-Apim-Subscription-Key' : bing_api_key}
	# Create a 'password manager' which handles authentication for us.
	
	request = urllib2.Request(search_url)
	request.add_header('Ocp-Apim-Subscription-Key',bing_api_key)
	

	# Create our results list which we'll populate.
	results = []

	try:
		
		

		print "geting response"
		# Connect to the server and read the response generated.
		response = urllib2.urlopen(request).read()

		# Convert the string response to a Python dictionary object.
		json_results = json.loads(response)
		
		# Loop through each page returned, populating out results list.
		packaged_results = [WebResult(single_result_json) for single_result_json in json_results.get("webPages", {}).get("value", [])]
		for single_result_json in json_results.get("webPages", {}).get("value", []):
			results.append({'url': single_result_json['url'],
                        'name': single_result_json['name'],
						'snippet': single_result_json['snippet']})
	except:
		print("Error when querying the Bing API")
	
	# Return the list of results to the calling function.
	for result in results:
		print(result['url'])
		print('-'*len(result['url']))
		print(result['name'])
		print(result['snippet'])
		print()
	return results
	
class WebResult(object):
    '''
    The class represents a SINGLE search result.
    Each result will come with the following:
    the variable json will contain the full json object of the result.
    title: title of the result (alternately name)
    url: the url of the result. Seems to be a Bing redirect
    displayUrl: the url used to display
    snippet: description for the result (alternately description)
    id: MsCognitive id for the page
    '''

    def __init__(self, result):
        self.json = result
        self.url = result.get('url')
        self.display_url = result.get('displayUrl')
        self.name = result.get('name')
        self.snippet = result.get('snippet')
        self.id = result.get('id')

        #maintain compatibility
        self.title = result.get('name')
        self.description = result.get('snippet')

        self.deep_links = result.get('deepLinks')

def main():
	print("Enter a query ")
	query = raw_input()
	results = run_query(query)

	# for result in results:
	# 	print(result['url'])
	# 	print('-'*len(result['url']))
	# 	print(result['name'])
	# 	print(result['id'])
	# 	print()
		
	
if __name__ == '__main__':
	main()