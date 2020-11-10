import random
import string

class CommonLib():

	def random_value(stringLength=10):
		#password_characters = string.ascii_letters + string.digits + string.punctuation
		password_characters = string.ascii_letters + string.digits
		return ''.join(random.choice(password_characters) for i in range(stringLength))