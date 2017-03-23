import os
os.environ['DJANGO_SETTINGS_MODULE'] = "MFsite.settings"

import django
django.setup()

from masterfaster.models import User

# u = User(username="maxschridde2", password="lol", email="whatever@gmail.com", image_file='max.jpg'.file.read())
# from blog.models import BlogPost
# from django.utils import timezone
# import datetime

# names = ['max1', 'max2', 'max3']
# passwords = ['a', 'b', 'c']
# emails = ['maxschridde@yahoo.com', 'maxschridde@gmail.com', 'maxschridde@berkeley.edu']

# titles = ['Test Post 1', 'Test Post 2', 'Test Post 3']
# placeholder_text = "What is Lorem Ipsum?\
# \nLorem Ipsum is simply dummy text of the printing and \
# typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, \
# when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has \
# survived not only five centuries, but also the leap into electronic typesetting, remaining essentially \
# unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, \
# and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. \
# \n Why do we use it?\
# \nIt is a long established fact that a reader will be distracted by the readable content of a page when looking at \
# its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed \
# to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web \
# page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web \
# sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose \
# (injected humour and the like)."

# for i in range(3):
# 	#Populate fake users
# 	u = User(username=names[i], password=passwords[i], email=emails[i])
# 	u.save()
# 	#Populate fake blog posts
# 	date = timezone.now() - datetime.timedelta(days=10*i)
# 	b = BlogPost(author=u, title=titles[i], pub_date=date, text=placeholder_text)
# 	b.save()