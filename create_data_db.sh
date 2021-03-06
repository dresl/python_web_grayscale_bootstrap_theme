#!/bin/bash
. /srv/bootstrap_sites/bootstrap_venv/bin/activate

echo "
import django;
from django.contrib.auth.models import User;
from polls.models import Question, Choice;
from mathematic.models import Brigade, Day;
from datetime import timedelta;
from django.utils import timezone;
from blog.models import Blog;
from books.models import Publisher, Author, Book;
a=Publisher(name='XXX', address='XXXX', city='XXXXX', state_province='XXX', country='England', website='www.example.com'); a.save();
b=Author(first_name='William', last_name='Shakespeare'); b.save();
b=Author(first_name='Božena', last_name='Němcová'); b.save();
b=Author(first_name='Karel', last_name='Čapek'); b.save();
i='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin egestas iaculis nisl sed molestie. Nam vel sollicitudin sapien. Duis vel semper dolor. Sed non dictum justo, non laoreet enim. Cras semper convallis dapibus. Integer vel neque magna. Proin cursus blandit pellentesque. Cras enim ex, feugiat eu tempus eget, viverra vel libero. Maecenas vitae magna nec orci tristique ultricies ac non velit. Donec tristique arcu id commodo eleifend. Vivamus vehicula elit vitae tortor convallis, id venenatis nibh pharetra. Phasellus eget augue et massa pellentesque ullamcorper eget eget enim. Suspendisse fringilla sapien neque, id aliquet orci ornare a. Fusce in eros lorem. Ut tincidunt in ex non auctor. Duis sed turpis hendrerit, mollis mauris fringilla, tincidunt magna. Sed nec scelerisque nulla. In vitae tellus eu magna consectetur interdum. In in lectus pulvinar, tristique libero at, laoreet ipsum. Donec et nibh sit amet magna varius dictum vel non justo. Aenean eu nisi eget arcu ullamcorper varius. Curabitur mattis consequat lorem, at bibendum nunc laoreet sit amet. Aenean fringilla sapien dolor, ut semper metus pharetra cursus. Etiam vitae ipsum euismod, luctus ex sed, interdum risus. In lectus ante, euismod nec metus nec, porta tincidunt nisl. ';
a=Blog(title='My first blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=5*366)); a.save();
a=Blog(title='My second blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=5*326)); a.save();
a=Blog(title='My third blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=4*366)); a.save();
a=Blog(title='My fourth blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=4*366)); a.save();
a=Blog(title='My fifth blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=4*366)); a.save();
a=Blog(title='My sixth blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=2*366)); a.save();
a=Blog(title='My seventh blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=2*366)); a.save();
a=Blog(title='My eighth blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=2*366)); a.save();
a=Blog(title='My nineth blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=2*366)); a.save();
a=Blog(title='My tenth blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=1*366)); a.save();
a=Blog(title='My eleventh blog', body=(i + ' ') * 3, pub_date=timezone.now()-timedelta(days=1*366)); a.save();
a=Blog(title='My last blog', body=(i + ' ') * 3, pub_date=timezone.now()); a.save();
a=Question(question_text='What is your favourite color?', pub_date=timezone.now()); a.save();
a=Question(question_text='This site looks:', pub_date=timezone.now()-timedelta(days=365)); a.save();
q=Question.objects.get(question_text='What is your favourite color?');
q.choice_set.create(choice_text='black', votes=2);
q.choice_set.create(choice_text='blue', votes=5);
q.choice_set.create(choice_text='red', votes=3);
q.choice_set.create(choice_text='white', votes=4);
q.choice_set.create(choice_text='purple', votes=1);
q.choice_set.create(choice_text='green', votes=7);
q=Question.objects.get(question_text='This site looks:');
q.choice_set.create(choice_text='great', votes=5);
q.choice_set.create(choice_text='fantastic', votes=9);
q.choice_set.create(choice_text='not bad', votes=1);
a=Brigade(brigade_title='Brigada Pavlisov', pub_date=timezone.now(), rate=50); a.save();
a=Brigade(brigade_title='Brigada Kaufland', pub_date=timezone.now()-timedelta(days=20*365), rate=65); a.save();
a=Brigade(brigade_title='Brigada Stavba', pub_date=timezone.now()-timedelta(days=20*365), rate=82); a.save();
q=Brigade.objects.get(brigade_title='Brigada Pavlisov');
q.save()
user = User.objects.create_user('root', 'nikicresl@gmail.com', 'admin');
user.first_name = 'Dominik'; user.last_name = 'Resl'; user.is_superuser=True; user.is_staff=True; user.save();
q.owner.add(user)
q.save()
q.day_set.create(number_of_day='Den: 1', hours_per_day=9, pub_date=timezone.now()-timedelta(days=21));
q.day_set.create(number_of_day='Den: 2', hours_per_day=10, pub_date=timezone.now()-timedelta(days=20));
q.day_set.create(number_of_day='Den: 3', hours_per_day=9, pub_date=timezone.now()-timedelta(days=19));
q.day_set.create(number_of_day='Den: 4', hours_per_day=9, pub_date=timezone.now()-timedelta(days=18));
q.day_set.create(number_of_day='Den: 5', hours_per_day=8, pub_date=timezone.now()-timedelta(days=17));
q.day_set.create(number_of_day='Den: 6', hours_per_day=9, pub_date=timezone.now()-timedelta(days=16));
q.day_set.create(number_of_day='Den: 7', hours_per_day=9, pub_date=timezone.now()-timedelta(days=15));
q.day_set.create(number_of_day='Den: 8', hours_per_day=9, pub_date=timezone.now()-timedelta(days=14));
q.day_set.create(number_of_day='Den: 9', hours_per_day=10, pub_date=timezone.now()-timedelta(days=13));
q.day_set.create(number_of_day='Den: 10', hours_per_day=9, pub_date=timezone.now()-timedelta(days=12));
q.day_set.create(number_of_day='Den: 11', hours_per_day=8, pub_date=timezone.now()-timedelta(days=11));
q.day_set.create(number_of_day='Den: 12', hours_per_day=9, pub_date=timezone.now()-timedelta(days=10));
q.day_set.create(number_of_day='Den: 13', hours_per_day=10, pub_date=timezone.now()-timedelta(days=9));
q.day_set.create(number_of_day='Den: 14', hours_per_day=9, pub_date=timezone.now()-timedelta(days=8));
q.day_set.create(number_of_day='Den: 15', hours_per_day=9, pub_date=timezone.now()-timedelta(days=7));
q.day_set.create(number_of_day='Den: 16', hours_per_day=8, pub_date=timezone.now()-timedelta(days=6));
q.day_set.create(number_of_day='Den: 17', hours_per_day=9, pub_date=timezone.now()-timedelta(days=5));
q.day_set.create(number_of_day='Den: 18', hours_per_day=8, pub_date=timezone.now()-timedelta(days=4));
q.day_set.create(number_of_day='Den: 19', hours_per_day=9, pub_date=timezone.now()-timedelta(days=3));
q.day_set.create(number_of_day='Den: 20', hours_per_day=8, pub_date=timezone.now()-timedelta(days=2));
q.day_set.create(number_of_day='Den: 21', hours_per_day=9, pub_date=timezone.now()-timedelta(days=1));
q.day_set.create(number_of_day='Den: 22', hours_per_day=8, pub_date=timezone.now());
q=Brigade.objects.get(brigade_title='Brigada Kaufland');
q.save()
user = User.objects.create_user('user1', 'userone@userone.com', 'useronepass');
user.first_name = 'User'; user.last_name = 'One'; user.save();
q.owner.add(user)
q.day_set.create(number_of_day='Den: 1', hours_per_day=8, pub_date=timezone.now()-timedelta(days=10));
q.day_set.create(number_of_day='Den: 2', hours_per_day=8, pub_date=timezone.now()-timedelta(days=9));
q.day_set.create(number_of_day='Den: 3', hours_per_day=8, pub_date=timezone.now()-timedelta(days=8));
q.day_set.create(number_of_day='Den: 4', hours_per_day=8, pub_date=timezone.now()-timedelta(days=7));
q.day_set.create(number_of_day='Den: 5', hours_per_day=8, pub_date=timezone.now()-timedelta(days=6));
q.day_set.create(number_of_day='Den: 6', hours_per_day=8, pub_date=timezone.now()-timedelta(days=5));
q.day_set.create(number_of_day='Den: 7', hours_per_day=8, pub_date=timezone.now()-timedelta(days=4));
q.day_set.create(number_of_day='Den: 8', hours_per_day=8, pub_date=timezone.now()-timedelta(days=3));
q.day_set.create(number_of_day='Den: 9', hours_per_day=8, pub_date=timezone.now()-timedelta(days=2));
q.day_set.create(number_of_day='Den: 10', hours_per_day=8, pub_date=timezone.now()-timedelta(days=1));
q.day_set.create(number_of_day='Den: 11', hours_per_day=8, pub_date=timezone.now());
q=Brigade.objects.get(brigade_title='Brigada Stavba');
q.save()
user = User.objects.create_user('user2', 'usertwo@usertwo.com', 'usertwopass');
user.first_name = 'User'; user.last_name = 'Two'; user.save();
q.owner.add(user)
q.save()
q.day_set.create(number_of_day='Den: 1', hours_per_day=9, pub_date=timezone.now()-timedelta(days=14));
q.day_set.create(number_of_day='Den: 2', hours_per_day=8, pub_date=timezone.now()-timedelta(days=13));
q.day_set.create(number_of_day='Den: 3', hours_per_day=10, pub_date=timezone.now()-timedelta(days=12));
q.day_set.create(number_of_day='Den: 4', hours_per_day=9, pub_date=timezone.now()-timedelta(days=11));
q.day_set.create(number_of_day='Den: 5', hours_per_day=10, pub_date=timezone.now()-timedelta(days=10));
q.day_set.create(number_of_day='Den: 6', hours_per_day=8, pub_date=timezone.now()-timedelta(days=9));
q.day_set.create(number_of_day='Den: 7', hours_per_day=8, pub_date=timezone.now()-timedelta(days=8));
q.day_set.create(number_of_day='Den: 8', hours_per_day=10, pub_date=timezone.now()-timedelta(days=7));
q.day_set.create(number_of_day='Den: 9', hours_per_day=8, pub_date=timezone.now()-timedelta(days=6));
q.day_set.create(number_of_day='Den: 10', hours_per_day=9, pub_date=timezone.now()-timedelta(days=5));
q.day_set.create(number_of_day='Den: 11', hours_per_day=8, pub_date=timezone.now()-timedelta(days=4));
q.day_set.create(number_of_day='Den: 12', hours_per_day=11, pub_date=timezone.now()-timedelta(days=3));
q.day_set.create(number_of_day='Den: 13', hours_per_day=9, pub_date=timezone.now()-timedelta(days=2));
q.day_set.create(number_of_day='Den: 14', hours_per_day=9, pub_date=timezone.now()-timedelta(days=1));
q.day_set.create(number_of_day='Den: 15', hours_per_day=8, pub_date=timezone.now());
user = User.objects.create_user('user3', 'userthree@userthree.com', 'userthreepass');
user.first_name = 'User'; user.last_name = 'Three'; user.save();
user = User.objects.create_user('user4', 'userfour@userfour.com', 'userfourpass');
user.first_name = 'User'; user.last_name = 'Four'; user.save();
" | python manage.py shell
