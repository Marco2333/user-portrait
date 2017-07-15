import twitter
import config
import MySQLdb
import time
from pymongo import MongoClient


class Crawler:
	def __init__(self):
		api = []
		self.apiCount = 58
		for i in range(self.apiCount):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))
		self.api = api
		
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db

	def get_basic_info(self, screen_name):

		api_index = 0
		sleep_count = 0

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()

		try:
			api_index = (api_index + 1) % self.apiCount
			user = self.api[api_index].GetUser(screen_name = screen_name)
		except Exception as e:
			print e
			return		

		try:
			is_translator = 0
			if hasattr(user, "is_translator"):
				is_translator = 1 if user.is_translator else 0

			name = user.name.replace("'","\\'")
			location = user.location.replace("'","\\'") if user.description else ''
			description = user.description.replace("'","\\'") if user.description else ''
			protected = 1 if user.protected else 0
			verified = 1 if user.verified else 0
			geo_enabled = 1 if user.geo_enabled else 0
			listed_count = user.listed_count if user.listed_count else 0
			default_profile_image = 1 if user.default_profile_image else 0 

			sql = """INSERT INTO user_famous(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
					followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
					is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
					('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
					'%s', '%s', '%s', '%s')""" % (user.id, user.screen_name, name, location, user.created_at, description, user.statuses_count, \
					user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
					user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
					user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

		except Exception as e:
			print e
			return

		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print e
			return
	
		db.close()

	def get_following(self, screen_name):
		file_obj = open('following_user/' + screen_name + '.txt','w')

		apis = self.api
		api_index = 0
		api_count = self.apiCount
		sleep_count = 0

		cursor = -1

		while cursor != 0:
			api = apis[api_index]
			api_index = (api_index + 1) % api_count
			try:
				out = api.GetFriendIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			except Exception as e:
				if hasattr(e, "message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							sleep_count = sleep_count + 1
							if sleep_count == api_count:
								print "sleeping..."
								sleep_count = 0
								time.sleep(900)
							continue
						else:
							print e
							break
					except Exception as e2:
						print e2
						break
				else:
					print e
					break

			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()


	def get_followers(self, screen_name):
		file_obj = open('followers_user/' + screen_name + '.txt','w')

		apis = self.api
		api_index = 20
		api_count = self.apiCount
		sleep_count = 0
		cursor = -1

		while cursor != 0:
			api = apis[api_index]
			api_index = (api_index + 1) % api_count
			try:
				out = api.GetFollowerIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			except Exception as e:
				if hasattr(e, "message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							sleep_count = sleep_count + 1
							if sleep_count == api_count:
								print "sleeping..."
								sleep_count = 0
								time.sleep(900)
							continue
						else:
							print e
							break
					except Exception as e2:
						print e2
						break
				else:
					print e
					break

			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()	


	def get_user_tweets(self, screen_name):
		apis = self.api
		api_index = 0
		api_count = self.apiCount
		flag = True
		tweets = [0]
		sleep_count = 0

		# file_obj = open('tweets_user/' + screen_name + '.txt','w')
		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		db = client[db_name]
		collect = db['tweet_famous']

		while len(tweets) > 0:
			api_index = (api_index + 1) % api_count
			if flag:
				try:
					tweets = apis[api_index].GetUserTimeline(screen_name = screen_name, count = 200)
					flag = False
				except Exception as e:
					if hasattr(e, "message"):
						print e.message
						try:
							if e.message[0]['code'] == 88:
								sleep_count = sleep_count + 1
								if sleep_count == api_count:
									print "sleeping..."
									sleep_count = 0
									time.sleep(800)
								flag = True
								continue
							else:
								print e
								break
						except Exception as e2:
							print e2
							break
					else:
						print e
						break
			else:
				try:
					# RT @taylorswift13: So much love...(retweet)  # tag #word  @user
					tweets = apis[api_index].GetUserTimeline(screen_name = screen_name, count = 200, max_id = tweets[-1].id - 1)
				except Exception as e:
					if hasattr(e, "message"):
						print e.message
						try:
							if e.message[0]['code'] == 88:
								sleep_count = sleep_count + 1
								if sleep_count == api_count:
									print "sleeping..."
									sleep_count = 0
									time.sleep(800)
								continue
							else:
								print e
								break
						except Exception as e2:
							print e2
							break
					else:
						print e
						break
				
			# for tt in tweets:
			# 	try:
			# 		file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
			# 	except Exception as e1:
			# 		print e1
			# 		continue
			for tt in tweets:
				tweet = {
					# 'contributors': tt.,
					'coordinates': tt.coordinates,  # Coordinates
					'created_at': tt.created_at, # String
					# 'current_user_retweet': None,
					'favorite_count': tt.favorite_count, # int
					# 'favorited': tt.favorited,
					'filter_level': tt.filter_level if hasattr(tt, 'filter_level') else '', # String
					# 'geo': tt.geo,
					'hashtags': map(lambda x: x.text, tt.hashtags), # {'0': ,'1':}
					'_id': tt.id_str, # String
					# 'id_str': tt.id_str,
					'in_reply_to_screen_name': tt.in_reply_to_screen_name,
					'in_reply_to_status_id': tt.in_reply_to_status_id,
					'in_reply_to_user_id': tt.in_reply_to_user_id,
					'lang': tt.lang, # String
					# 'media': tt.media,
					'place': tt.place, # Place
					'possibly_sensitive': tt.possibly_sensitive, # Boolean
					'retweet_count': tt.retweet_count, # int
					# 'retweeted': tt.retweeted,
					# 'retweeted_status': tt.retweeted_status,
					# 'scopes': tt.scopes, # Object
					'source': tt.source, # String
					'text': tt.text, # String
					# 'truncated': tt.truncated,
					# 'urls': tt.urls, # []
					'user_id': tt.user.id, # int
					'user_mentions': map(lambda x: x.id, tt.user_mentions), # []
					'withheld_copyright': tt.withheld_copyright, # Boolean
					'withheld_in_countries': tt.withheld_in_countries, # Array of String
					'withheld_scope': tt.withheld_scope, #String
				}
				try:
					collect.insert_one(tweet)
				except Exception as e:
					print e

		# file_obj.close()

	def restart(self):
		# sql = "select userid, screen_name from standardusers where screen_name not in (select screen_name from test)" 
		# try:
		# 	self.cursor.execute(sql)
		# 	name_list = self.cursor.fetchall()
		# except:
		# 	return
		
		# return name_list
		sql = "select screen_name from user_famous" 
		try:
			self.cursor.execute(sql)
			name_list = self.cursor.fetchall()
		except Exception as e:
			print e
			# pass

		return name_list

		
if __name__ == "__main__":
	# name_list = ['YESBANK', 'TheOfficialSBI', 'NYSE', 'wrausahamandiri', 'kickstarter', 'gtbank', 'AlRajhiBank', 'BNI', 'AmericanExpress', 'DIFC', 'AlbankAldawli', 'SAIBLIVE', 'sberbank', 'TheWorldCurrenc', 'ycombinator', 'CBOE', 'AlAhliNCB', 'themotleyfool', 'DeutscheBank', 'MYBIGCOIN', 'WesternUnion', 'Banesco', 'itau', 'GoldmanSachs', 'ftfinancenews', 'scb_thailand', '500Startups', 'GVteam', 'StartupGrind', 'Bloomberg', 'Nasdaq', 'BankofAmerica', 'MerrillLynch', 'bank_indonesia', 'Mastercard', 'BofA_News', 'MastercardMEA', 'PayPal', 'sequoia', 'Paytm', 'MorganStanley', 'NBKPage', 'SABBBank', 'Banquemondiale', 'MasterCardVE', 'BBVAProvincial', 'XpresiBCA', 'ecb', 'VisaBR', 'Citibank', 'BcodeVenezuela', 'obmenik', 'BankAlJazira', 'Visa', 'BancoMundial', 'jpmorgan', 'Chase', 'mandirifiesta', 'Citibanamex', 'sahmycom', 'BCPComunica', 'MastercardCol', 'WorldBankAfrica', 'BankAlbilad', 'ICICIBank', 'UBS', 'VisaMX', 'CreditSuisse', 'KFHGroup', 'BancoPacificoEC', 'a16z', 'Bancolombia', 'techstars', 'garanti', 'WellsFargo', 'BancoPichincha', 'MercantilBanco', 'UniBul', 'interbank', 'BancoRepublica', 'BBVAContinental', 'myaccessbank', 'riyadbank', 'BMVMercados', 'WisdomTreeETFs', 'VisaColombia', 'Vanguard_Group', 'MastercardMex', 'ziraatbankasi', 'bank_muscat', 'MoneyGram', 'Square', 'FirstBankngr', 'PIMCO', 'QNBGroup', 'CNEXEU', 'Popularenlinea', 'ANB_BANK', 'NabilAlawadhy', 'alhabibali', 'OCriador', 'saudalshureem', 'goromalbeshe', 'Binothaymeen', 'Bibliaenlinea', 'TeladanRasul', 'ayatquran', 'MohsenAlAwajy', 'alathkaar', 'Khalid_Aljubair', 'ustazharidrus', '1001inventions', 'PastorChrisLive', 'Du3aa', 'philipmantofa', 'SoulDirection1', 'rashedzahrany', 'Amer_Abdulla', 'BispoRodovalho', 'ALNJLA_', 'islamsozler', 'HolyQuran1', 'waktuSolatKL', 'falsunaidy', 'Women_Of_Christ', 'Godly_Life', 'GreatBibleVerse', 'hillsong', 'adel21212121', 'Dr_Heba_Raouf', 'SamaritansPurse', '9alatReminder', 'TahirulQadri', 'CristoEnTi', 'TheNobleQuran', 'UstazAzharIdrus', 'NASSER_MOHAMAD_', 'Quranhadist', 'alikhlas_112', 'Amor_e_Fe', 'To_ld', 'Q8Souq', 'Sultanalablan', 'BookOProverbs', 'Rasoulallah', 'FaithReeI', 'Leia_a_Biblia', 'IslamQuotes', 'TopBibleVerses', 'desiringGod', 'fowadeslamia', 'HoyAfirmo', 'drjustinimel', 'dailybible', 'thichnhathanh', 'judahsmith', 'Akhtan1', 'contraenvidia', 'Quran_ksu', 'BibleVerseQuote', 'ahmadbinhanbl', 'JesusEsFieI', 'diostuitero', 'All_About_Jesus', 'doatertulis', 'Tw_rt_ksa', 'liixoxiil', 'PastorEAAdeboye', 'Godstagram', 'ahlalsunna2', 'cancaonova', 'MotherRose1', 'DiosContigoEsta', 'eslameatm', 'MormonNewsroom', 'salavatlar', 'Q8w6ny', 'HillsongEsp', 'Lagoinha_com', 'cnalive', 'CopelandNetwork', 'khair_maker', 'SadhguruJV', '63ALY', 'TwitFaktaIslam', 'MORMONorg', 'JWRCministries', 'bibliaonline', 'QuranWeekly', 'SismologicoMX', 'UNAM_MX', 'CulturaUNAM', 'kauweb', 'preschoolers', 'univ_indonesia', 'unpad', 'MIT', 'UGMYogyakarta', 'Harvard', 'IPN_MX', 'itbofficial', 'Ind_Mengajar', 'ipbofficial', 'nagasaki', 'pucp', 'LSUfootball', 'Stanford', 'TecdeMonterrey', 'UNJ_Official', 'GoldSilverClub', 'Codecademy', 'bbcle', 'StanfordBiz', 'MSLearning', 'TED_ED', 'CCCMexico', 'medialab', 'WeAreTeachers', 'Wikipedia', 'UniofOxford', 'coursera', 'HarvardHBS', 'Yale', 'DiscoveryEd', 'FilmotecaUNAM', 'Cambridge_Uni', 'YoungOnTop', 'UCarabobo', 'AMAnet', 'egitim_yurtdisi', 'OhioState', 'NiemanLab', 'UdeA', 'Princeton', 'FullSail', 'waktuSMA', 'AeroIasca', 'OxfordWords', 'UPTuks', 'unimedios', 'ASU', '_KSU', 'urbandictionary', 'LearnEnglish_BC', 'eduwillnet', 'MindShiftKQED', 'BINUS_UNIV', 'matherdanceco', 'TAMU', 'descomplica', 'IESA', 'HarvardChanSPH', 'Columbia', 'lsu', 'KelloggSchool', 'LSUbaseball', 'CSIS', 'Wharton', 'AnkaraUni', 'BritishCouncil', 'UOPX', 'ColombiaAprende', 'udg_oficial', 'QatarUniversity', 'Dictionarycom', 'Cornell', 'heiternet', 'LUZadn', 'WaldenU', 'TeachingEnglish', 'harvardmed', 'AUB_Lebanon', 'UTAustin', 'StanfordMed', 'Just_Team', 'ALDC_official', 'UMich', 'unlp', 'Poynter', 'michiganstateu', 'MITSloan', 'CreativeLive', 'InstCervantes', 'rivercottage', 'secretary_kj', 'UWMadison', 'LSPRJAKARTA', 'Pontifex_es', 'RT_Erdogan', 'cbabdullahgul', 'EPN', 'KingSalman', 'MedvedevRussia', 'Ahmet_Davutoglu', 'FelipeCalderon', 'dilmabr', 'CFKArgentina', 'leopoldolopez', 'AlvaroUribeVel', 'naseralomar', 'kilicdarogluk', 'Pontifex_it', 'chavezcandanga', 'HamzawyAmr', 'mauriciomacri', '06melihgokcek', 'MariaCorinaYA', 'HamdeenSabahy', 'dbdevletbahceli', 'NaguibSawiris', 'AamAadmiParty', 'MaryamNSharif', 'bulent_arinc', 'noynoyaquino', 'NicolasMaduro', 'MashiRafael', 'matteorenzi', 'ManceraMiguelMX', 'PTIofficial', 'vekilince', 'drangelocarbone', 'DrAbolfotoh', 'afaaa73', 'Pontifex_pt', 'lopezobrador_', 'liliantintori', 'AymanNour', 'petrogustavo', 'MuhammadMorsi', 'PutinRF', 'ComandoSB', 'memetsimsek', 'amremoussa', 'Kadir__Topbas', 'Valimutlu', 't_ishin', 'alcaldeledezma', 'dcabellor', 'silva_marina', 'sebastianpinera', 'MrKRudd', 'ARTEM_KLYUSHIN', 'Zhirinovskiy', 'safakpavey', 'hattarajasa', 'Almoslemani', 'joseserra_', 'Ollanta_HumalaT', 'GeovanieJeffrie', '3M', 'rendezvousport', 'MahindraRise', 'TataCompanies', 'generalelectric', 'Virgin', '3MNewsroom', 'GEAviation', 'Bayer', 'AdityaBirlaGrp', 'GEdoBrasil', 'coopuk', 'editorarecord', 'DSM', 'LVMH', 'kocholding', 'Maersk', 'Bayer4CropsUS', 'DuPont_News', 'DowChemical', 'GEIndia', 'Cargill', '3MdoBrasil', 'rubbermaid', 'thyssenkrupp_en', 'TupperwareWW', 'honeywell', 'UTC', 'GE_MENAT', 'mudocomtr', '3M_Venezuela', 'DallahAlbaraka', 'thyssenkrupp', 'OdebrechtSA', 'EmpleoCarvajal', 'InsidePMI', 'GE_Canada', 'amwayeurope', 'BoschPresse', 'borusanholding', 'dubaiholding', 'hanwhadays', 'CapriceHoldings', 'GEAustralia', '3M_UK', 'ecoATM', 'Bupa', 'amwayindia', 'GraceKennedyGrp', '3M_Canada', '3MEspana', 'nomadsworld', 'BoschUK', 'GECapitalAus', 'CoxEnterprises', 'LOLCOfficial', 'OrtadoguGrup', 'GodrejGroup', 'AustralianSuper', 'alhabtoorgroup', 'AholdNews', 'GE_UK', 'newell_brands', 'BoschFrance', 'BoschEspana', '3MPortugal', 'Istanbul_Doors', 'AmwayPHofficial', 'Proudly_Bidvest', 'SPRichards', 'CloroxCo', 'RAI_News', 'odebrecht', 'inciholding', 'Grupo_Carso', '3MDeutschland', 'DodoAustralia', 'GE_Deutschland', 'ESSE_ID', '3M_Argentina', 'TheTavanBogd', 'ZF_Karriere', '3MTurkiye', '3MPeru', 'GrupoEmpAngeles', 'DoclerHoldingLU', 'SCM_holding', 'GrupoAgrisalSV', '3MSchweiz', 'BayerSuomi', 'Pakpen', 'IFFCO', '3MEcuador', '3MAustria', 'sonydadc', 'LegendBrands', 'andamioslayher', 'grupoornatus', '3MIreland', 'oxiteno_brasil', 'TMCPoldaMetro', 'dost_pagasa', 'tcbestepe', 'MMDA', 'KremlinRussia', 'WHO', 'spagov', 'DepEd_PH', 'infoBMKG', 'RoyalFamily', 'PresidenciaMX', 'RailMinIndia', 'policia', 'earthquake_jp', 'CinetecaMexico', 'ISPR_Official', 'Kantei_Saigai', 'Refugees', 'GobCDMX', 'cultura_mx', 'KPK_RI', 'NWS', 'JeddahAmanah', 'kadikoybelediye', 'moe_gov_sa', 'MOISaudiArabia', 'gcba', 'metrosp_oficial', 'Elysee', 'SaudiMCI', 'kemristekdikti', 'GOVUK', 'STF_oficial', 'OVIALCDMX', 'govph', 'Presidencia_Ec', 'MLSD_SA', 'SaudiMOH', 'PeaceCorps', 'TheJusticeDept', 'DubaiPoliceHQ', 'onemichile', 'TC_Disisleri', 'IndianDiplomacy', 'NITIAayog', 'MID_RF', 'Bogota', 'UKParliament', 'apod', 'Carabdechile', 'Almajlliss', 'TfLTrafficNews', 'SectorMovilidad', 'batransito', 'KSAMOFA', 'NSF', 'USDAFoodSafety', 'Kemdikbud_RI', 'GobiernodeChile', 'VTVNoticias', 'womenshealth', 'PoliciaColombia', 'Profeco', 'librarycongress', 'francediplo', 'MIB_India', 'FDMA_JAPAN', 'urimal365', 'PresidencialVen', 'NOAA', 'MchsRussia', 'conagua_clima', 'OpenGov44']

	file = open("user/toCrawlBasicInfo")

	crawler = Crawler()
	name_list = crawler.restart()

	name_list = map(lambda x: x[0], name_list)
	# print name_list

	print len(name_list)
	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	    	if line.strip() in name_list:
	    		continue
	        crawler.get_basic_info(line)
	        # crawler.get_user_tweets(line)


	# for user in name_list:
		# print user
		# crawler.get_user_tweets(user)
		# crawler.get_basic_info(user[0])
		# crawler.get_followers('barackobama')
