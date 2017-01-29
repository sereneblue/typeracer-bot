from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from sys import exit
from time import sleep
import platform

class TypeRacer:
	def __init__(self):
		print('TypeRacer Bot v1.0')
		print('==================')
		print('Available Commands: ')
		print('private     | Play a private match')
		print('public      | Play a public match')
		print('practice    | Practice using the bot')
		print('login       | Login to your typeracer account')
		print('exit        | Exit the bot')
		print('\n')
		print('What browser do you want to use? It must be installed on your computer!')
		print('[1] Firefox')
		print('[2] Chrome/Chromium')
		choice = input('> ')
		self.browser_driver = "geckodriver" if choice == "1" else "chromedriver"
		self.build_path()
		self.start()
		self.console()

	def build_path(self):
		path = "assets/drivers/"
		system = platform.system()
		arch = ""
		while arch not in ('32','64'):
			arch = input('Are you using a 32bit browser or 64bit browser? If in doubt, use 32. (32)/(64) \n> ')

		#determine driver executable path
		if system == "Windows":
			self.path = "{}windows/{}_{}.exe".format(path, self.browser_driver, arch)
		elif system == "Mac":
			self.path = "{}mac/{}".format(path, self.browser_driver)
		elif system == "Linux":
			self.path = "{}linux/{}_{}".format(path, self.browser_driver, arch)
		else:
			print("Your platform is unsupported!")
			exit()

	def console(self):
		while True:
			cmd = input('What would you like to do?\n> ')
			if cmd in ('private', 'public', 'practice','login','exit'):
				if cmd == 'private':
					self.play_private_match()
				elif cmd == 'public':
					self.play_public_match()
				elif cmd == 'practice':
					self.practice()
				elif cmd == 'login':
					self.login()
				elif cmd == 'exit':
					try:
						self.driver.quit()
					except: #this is normally bad but ¯\_(ツ)_/¯
						pass
					finally:
						exit()
			else:
				print('That was an invalid command!')

	def play(self):
		"""
		The 'bot'
		"""
		while True:
			#get current word
			content = self.driver.find_element_by_class_name('nonHideableWords')
			elem = content.find_elements_by_tag_name('span')
			word = elem[1].text + elem[2].text + ' '
			in_elem = self.driver.find_element_by_class_name('txtInput')
			#type word
			try:
				in_elem.send_keys(word)
			except ElementNotVisibleException:
				sleep(2) #wait for page to update with result
				print("The race is over. " + self.driver.find_element_by_class_name('gameStatusLabel').text)
				break
			finally: #no brakes and you'll be disqualified!
				sleep(.25)

	def play_private_match(self):
		"""
		Play a private match against your friends
		"""
		url = input('What is the private match URL?\n> ')
		self.driver.get(url)
		sleep(4)
		self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, Keys.ALT, 'K')
		# self.driver.find_element_by_xpath('//*[@id="gwt-uid-28"]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/a').click()
		sleep(11)
		self.play()

	def play_public_match(self):
		"""
		Play a public match against other people
		"""
		self.driver.get('http://typeracer.com')
		self.driver.find_element_by_xpath('//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a').click()
		sleep(11)
		self.play()

	def practice(self):
		"""
		Practice with the bot
		"""
		self.driver.get('http://play.typeracer.com')
		self.driver.find_element_by_xpath('//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a').click()
		sleep(5)
		self.play()

	def login(self):
		"""
		Login to your account. Results don't save unless you have premium afaik
		"""
		user = input('What is your username?\n> ').strip()
		password = input('What is your password?\n> ').strip()
		self.driver.get('http://play.typeracer.com')
		self.driver.find_element_by_xpath('//*[@id="tstats-edit"]/div/table/tbody/tr/td[1]/a').click()
		self.driver.find_element_by_name("username").send_keys(user)
		self.driver.find_element_by_name("password").send_keys(password)
		self.driver.find_element_by_xpath("/html/body/div[4]/div/table/tbody/tr[2]/td/div/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[4]/td[2]/table/tbody/tr/td[1]/button").click()

	def start(self):
		"""
		Start the webdriver, loads ublock origin to improve performance
		"""
		if self.browser_driver == "geckodriver":
			fp = webdriver.FirefoxProfile()
			fp.add_extension(extension='assets/ublock_origin-1.10.6-an+fx+sm+tb.xpi')
			firefox_capabilities = DesiredCapabilities.FIREFOX
			firefox_capabilities['marionette'] = True

			print('Starting Firefox...')
			self.driver = webdriver.Firefox(capabilities=firefox_capabilities, executable_path=self.path, firefox_profile=fp)
		else:
			chrome_options = ChromeOptions()
			chrome_options.add_extension('assets/extension_1_10_4.crx')
			print('Starting Chrome...')
			self.driver = webdriver.Chrome(desired_capabilities = chrome_options.to_capabilities(), executable_path=self.path)
		self.driver.implicitly_wait(10)

TypeRacer()