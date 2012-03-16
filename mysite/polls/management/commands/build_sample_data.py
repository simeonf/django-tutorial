from datetime import date

from django.core.management.base import BaseCommand

from polls.models import *
from django.contrib.auth.models import User
import random

lorem = """Lorem ipsum dolor sit amet, consectetur adipisicing elit,
           sed do eiusmod tempor incididunt ut labore et dolore magna
           aliqua. Ut enim ad minim veniam, quis nostrud exercitation
           ullamco laboris nisi ut aliquip ex ea commodo
           consequat. Duis aute irure dolor in reprehenderit in
           voluptate velit esse cillum dolore eu fugiat nulla
           pariatur. Excepteur sint occaecat cupidatat non proident,
           sunt in culpa qui officia deserunt mollit anim id est
           laborum""".split(" ")
lorem = [word.strip(".,").lower() for word in lorem]

def rrange(start, lowstop, highstop):
    return xrange(start, random.randrange(lowstop, highstop))

start_date = date(2011, 1, 1).toordinal()
end_date = date.today().toordinal()
def random_date():
     return date.fromordinal(random.randint(start_date, end_date))

class Command(BaseCommand):
    help = "My shiny new management command."
    
    def handle(self, *args, **options):
        # create 20 users
        existing_names = [u.username for u in User.objects.all()]
        names = []
        while len(names) < 20: #in case we create dupes
            username = ''.join(random.sample("aaabcdeeeefghiiiijklmnooopqrstuuvw", 8))
            if username not in names and username not in existing_names:
                names.append(username)
        for name in names:
            User.objects.create_user(name, name + "@gmail.com", "test")

        # Each user creates between 3 and 40 polls
        for name in names:
            u = User.objects.get(username=name)
            for num in rrange(3, 4, 41):
                sentence = random.sample(lorem, random.randrange(3, 10)) # pick random number of words
                random.shuffle(sentence)
                sentence[0] = sentence[0].title()
                question=" ".join(sentence)
                slug = question[:70].lower().replace(" ", "-")
                num = 1
                while Poll.objects.filter(slug=slug + str(num)):
                    num += 1
                p = Poll(question + "?", slug=slug+str(num), user=u, pub_date=random_date())
                p.save()
                # create 2 - 5 choices for each poll
                for i in rrange(2, 3, 6):
                    Choice(poll=p, choice=random.choice(lorem)).save()
        # Grab all the choices, 1 in 5 chance of being voted on, random# of votes by random users
        choices = list(Choice.objects.all())
        choices = random.sample(choices, len(choices) / 5) # sample of 20% of data
        for c in choices:
            # use power series distribution
            # mostly low numbers but possibility of high numbers
            for i in range(int(random.paretovariate(1))):
                #Make a vote w/ random user
                Vote(choice=c, user=User.objects.get(username=random.choice(names))).save()
        # Favorites
        polls = list(Poll.objects.all())
        polls = random.sample(polls, len(polls) / 20) # sample of 5% of polls
        for p in polls:
            # use power series distribution
            # mostly low numbers but possibility of high numbers
            for i in range(int(random.paretovariate(1))):
                #Make a Favrorite w/ random user
                Favorite(poll=p, user=User.objects.get(username=random.choice(names))).save() 
