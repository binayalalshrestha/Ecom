from django.core.mail import send_mail
from django.conf import settings

def has_customer(user):

	if(hasattr(user,'customer')):

		return user.customer
	return None


 # send registration email
def send_email(user):
# 	send_mail(
#     'Subject',
#     'Message body',
#     'noreply@infodev.com.np',
#     ['binaya.shrestha08@gmail.com'],
#     fail_silently=False,
# )
	subject = 'Email confirmation'
	message = ' Thank you for registering to bCommerce, your one stop shop for everything you need !! '
		#Please click the following link to verify your email: {verification_url}'
	
	# from_email = settings.EMAIL_HOST_USER
	# print('---------------',from_email)
	recipient_list = [user.username,]
	send_mail(subject, message, "noreply@infodev.com.np", recipient_list, fail_silently=False)


            