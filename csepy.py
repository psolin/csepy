import urllib
import json
import re

class googlecse(object):

	def __init__(self, CSE_ID, SECRET_KEY):

		self.CSE_ID = CSE_ID

		self.SECRET_KEY = SECRET_KEY

	def url(self, **kws):

		# Query is required.  Otherwise, return nothing.
		if kws['query'] == None:
			return None

		# Check the length of the API keys in case something happened
		if (len(self.CSE_ID) != 33) or (len(self.SECRET_KEY) != 39):
			return None

		self.query = urllib.urlencode({'q': kws['query']})
		self.search_string = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&%s' % (self.SECRET_KEY, self.CSE_ID, self.query)

		

		# Append search_string according to optional arguments
		# https://developers.google.com/custom-search/json-api/v1/reference/cse/list#request
		
		#  Append the URL if the key is simply a string
		def append_url(key):
			try:
				self.search_string += ('&' + urllib.urlencode({key: kws[key]}))
			except:
				pass

		# Append the URL if the key matches one found in a specified list
		def append_url_list(key, term_list):
			try:
				for term in term_list:
					if kws[key] == term:
						self.search_string += ('&' + urllib.urlencode({key: kws[key]}))
						break
			except:
				pass

		# Enable or disable Traditional/Simplified Chinese
		try:
			if kws['c2off'] == True:
				append_url_list('c2off', 0)
			elif kws['c2off'] == False:
				append_url_list('c2off', 1)


		# Restrict the date to certain time periods, d, w, m, and y only.
		try:
			if re.search('^[d|w|m|y]\[\d+\]$', kws['dateRestrict']) != None:
				self.search_string += ('&' + urllib.urlencode({'dateRestrict': kws['dateRestrict']}))
		except:
			pass


		# Use some exact terms		
		append_url('exactTerms')

		
		# Exclude some terms
		append_url('excludeTerms')

		
		# Get a specific file type
		# https://support.google.com/webmasters/answer/35287?hl=en
		indexed_file_types = ['swf', 'pdf', 'ps', 'dwf', 'kml', 'kmz',
		'gpx', 'hwp', 'htm', 'html', 'xls', 'xlsx', 'ppt', 'pptx',
		'doc', 'docx', 'odp', 'ods', 'odt', 'rtf', 'wri', 'svg',
		'tex', 'txt', 'text', 'bas', 'c', 'cc', 'cpp', 'cxx', 'h',
		'hpp', 'cs', 'java', 'pl', 'py', 'wml', 'wap', 'xml']

		append_url_list('fileType', indexed_file_types)

		
		# Duplicate content filter, on/off (default is always on)
		try:
			if kws['filter'] == True:
				self.search_string += ('&' + urllib.urlencode({'filter': 1}))
			elif kws['filter'] == False:
				self.search_string += ('&' + urllib.urlencode({'filter': 0}))
		except:
			pass

		
		# Geolocation of end user
		# https://developers.google.com/custom-search/docs/xml_results#countryCodes
		country_codes = ['af', 'al', 'dz', 'as', 'ad', 
		'ao', 'ai', 'aq', 'ag', 'ar', 'am', 
		'aw', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'bb',
		'by', 'be', 'bz', 'bj', 'bm', 'bt', 'bo', 'ba',
		'bw', 'bv', 'br', 'io', 'bn', 'bg', 'bf', 'bi',
		'kh', 'cm', 'ca', 'cv', 'ky', 'cf', 'td', 'cl',
		'cn', 'cx', 'cc', 'co', 'km', 'cg', 'cd', 'ck',
		'cr', 'ci', 'hr', 'cu', 'cy', 'cz', 'dk', 'dj',
		'dm', 'do', 'ec', 'eg', 'sv', 'gq', 'er', 'ee',
		'et', 'fk', 'fo', 'fj', 'fi', 'fr', 'gf', 'pf',
		'tf', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr',
		'gl', 'gd', 'gp', 'gu', 'gt', 'gn', 'gw', 'gy',
		'ht', 'hm', 'va', 'hn', 'hk', 'hu', 'is', 'in',
		'id', 'ir', 'iq', 'ie', 'il', 'it', 'jm', 'jp',
		'jo', 'kz' 'ke', 'ki' 'kp', 'kr' 'kw', 'kg'
		'la', 'lv' 'lb', 'ls', 'lr', 'ly', 'li', 'lt',
		'lu', 'mo', 'mk', 'mg', 'mw', 'my', 'mv', 'ml',
		'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', 'fm',
		'md', 'mc', 'mn', 'ms', 'ma', 'mz', 'mm', 'na',
		'nr', 'np', 'nl', 'an', 'nc', 'nz', 'ni', 'ne',
		'ng', 'nu', 'nf', 'mp', 'no', 'om', 'pk', 'pw',
		'ps', 'pa', 'pg', 'py', 'pe', 'ph', 'pn', 'pl',
		'pt', 'pr', 'qa', 're', 'ro', 'ru', 'rw', 'sh',
		'kn', 'lc', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn',
		'cs', 'sc', 'sl', 'sg', 'sk', 'si', 'sb', 'so',
		'za', 'gs', 'es', 'lk', 'sd', 'sr', 'sj', 'sz',
		'se', 'ch', 'sy', 'tw', 'tj', 'tz', 'th', 'tl',
		'tg', 'tk', 'to', 'tt', 'tn', 'tr', 'tm', 'tc',
		'tv', 'ug', 'ua', 'ae', 'uk', 'us', 'um', 'uy', 
		'uz', 'vu', 've', 'vn', 'vg', 'vi', 'wf', 'eh', 
		'ye', 'zm', 'zw']
		
		append_url_list('pl', country_codes)

		
		# Google host (the domain to use for the search)
		try:
			for country in country_codes:
				if kws['googlehost'] == country:
					self.search_string += ('&' + urllib.urlencode({'googlehost': 'google.' + kws['googlehost']}))
		except:
			pass

		
		# Interface Language
		# https://developers.google.com/custom-search/docs/xml_results#interfaceLanguages
		language_codes = ['af', 'sq', 'sm', 'ar',
		'az', 'eu', 'be', 'bn', 'bh', 'bs', 'bg', 'ca',
		'zh-CN', 'zh-TW', 'hr', 'cs', 'da', 'nl', 'en', 'eo',
		'et', 'fo', 'fi', 'fr', 'fy', 'gl', 'ka', 'de',
		'el', 'gu', 'iw', 'hi', 'hu', 'is', 'id', 'ia',
		'ga', 'it', 'ja', 'jw', 'kn', 'ko', 'la', 'lv',
		'lt', 'mk', 'ms', 'ml', 'mt', 'mr', 'ne', 'no',
		'nn', 'oc', 'fa', 'pl', 'pt-BR', 'pt-PT', 'pa', 'ro',
		'ru', 'gd', 'sr', 'si', 'sk', 'sl', 'es', 'su',
		'sw', 'sv', 'tl', 'ta', 'te', 'th', 'ti', 'tr',
		'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'zu']

		append_url_list('h1', language_codes)


		# hq is an additional query term, as if you used 'and'
		append_url('hq')


		# Restrict to documents written in a specific language
		document_languages = ["lang_ar", "lang_bg", "lang_ca",
		"lang_cs", "lang_da", "lang_de", "lang_el",
		"lang_en", "lang_es", "lang_et", "lang_fi",
		"lang_fr", "lang_hr", "lang_hu", "lang_id",
		"lang_is", "lang_it", "lang_iw", "lang_ja",
		"lang_ko", "lang_lt", "lang_lv", "lang_nl",
		"lang_no", "lang_pl", "lang_pt", "lang_ro",
		"lang_ru", "lang_sk", "lang_sl", "lang_sr",
		"lang_sv", "lang_tr", "lang_zh-CN", "lang_zh-TW",]

		append_url_list('lr', document_languages)


		# All results containing a link to a particular URL
		append_url('linkSite')


		# Number of results, 1-10.
		try:
			if (kws['num'] < 11) and (round(kws['num']) == kws['num']):
				self.search_string += ('&' + urllib.urlencode({'num': kws['num']}))
		except:
			pass

		# ...or contains this additional term
		append_url('orTerms')


		# Related to a particular URL
		append_url('relatedSite')


		# Licensing rights -- could be more than one
		try:
			licensing_rights = ['cc_publicdomain', 'cc_attribute', 'cc_sharealike', 'cc_noncommercial', 'cc_nonderived']
			if type(kws['rights']) == list:
				for right in kws['rights']:
					if right in licensing_rights:
						self.search_string += ('&' + urllib.urlencode({'rights': right}))
			else:
				append_url_list('rights', licensing_rights)
		except:
			pass

		
		# Search safety level.  high, medium, or off.
		safety_levels = ['high', 'medium', 'off']
		append_url_list('safe', safety_levels)

		
		# Search only for images.
		append_url_list('searchType', ['image'])


		# If only searching for images, use some image properties
		try:
			if kws['searchType'] == 'image':
				
				# Black and white, grayscale, or color images.
				color_types = ["color", "gray", "mono"]	
				append_url_list('imgColorType', color_types)

				# Images of a specific dominant color
				dominant_colors = ["black", "blue", "brown", "gray", "green", "pink", "purple", "teal", "white", "yellow"]
				append_url_list('imgDominantColor', dominant_colors)

				# Image Size
				image_sizes = ["huge", "icon", "large", "medium", "small", "xlarge", "xxlarge"]
				append_url_list('imgSize', image_sizes)

				# Image Type
				image_types = ["clipart", "face", "lineart", "news", "photo"]
				append_url_list('imgType', image_types)
		except:
			pass


		# Results from a given site
		append_url('siteSearch')

		# Whether or not to include the above site
		try:
			if len(kwg['siteSearch']) > 0:
				if kwg['siteSearchFilter'] == True:
					append_url_list('siteSearchFilter', ['i'])
				elif kwg['siteSearchFilter'] == False:
					append_url_list('siteSearchFilter', ['e'])
		except:
			pass

		return self.search_string

	def results(self, **kws):
		
		loaded_url = self.url(**kws)

		# Load the JSON
		return json.loads(urllib.urlopen(loaded_url).read())