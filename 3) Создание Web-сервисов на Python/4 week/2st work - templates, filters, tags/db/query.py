from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC
from .models import User, Blog, Topic


def create():
    u1 = User.objects.create(first_name='u1', last_name='u1')
    u2 = User.objects.create(first_name='u2', last_name='u2')
    u3 = User.objects.create(first_name='u3', last_name='u3')

    b1 = Blog.objects.create(title='blog1', author=u1)
    b2 = Blog.objects.create(title='blog2', author=u1)
    #     Подписать пользователей u1 u2 на blog1, u2 на blog2.
    b1.subscribers.add(u1, u2)
    b2.subscribers.add(u2)

    t1 = Topic.objects.create(title='topic1', blog=b1, author=u1)
    t2 = Topic.objects.create(title='topic2_content', blog=b1, author=u3,
                              created=datetime(year=2017, month=1, day=1, tzinfo=UTC))

    t1.likes.add(u1, u2, u3)


def edit_all():
    # Поменять first_name на uu1 у всех пользователей (функция edit_all).
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    # Поменять first_name на uu1 у пользователей, у которых first_name u1 или u2 (функция edit_u1_u2).
    User.objects.filter(first_name__in=['u1', 'u2']).update(first_name='uu1')


def delete_u1():
    # удалить пользователя с first_name u1 (функция delete_u1).
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    # отписать пользователя с first_name u2 от блогов (функция unsubscribe_u2_from_blogs)
    u2 = User.objects.get(first_name='u2')
    for b in Blog.objects.all():
        b.subscribers.remove(u2)


def get_topic_created_grated():
    # Найти топики у которых дата создания больше 2018-01-01 (функция get_topic_created_grated).
    return Topic.objects.filter(created__gt='2018-01-01')



def get_topic_title_ended():
    # Найти топик у которого title заканчивается на content (функция get_topic_title_ended).
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    # Получить 2х первых пользователей (сортировка в обратном порядке по id) (функция get_user_with_limit).
    return User.objects.all().order_by('-id')[:2]


def get_topic_count():
    # Получить количество топиков в каждом блоге, назвать поле topic_count,
    # отсортировать по topic_count по возрастанию (функция get_topic_count).
    return Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    # Получить среднее количество топиков в блоге (функция get_avg_topic_count).
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    # Найти блоги, в которых топиков больше одного (функция get_blog_that_have_more_than_one_topic).
    return Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    # Получить все топики автора с first_name u1 (функция get_topic_by_u1).
    return Topic.objects.all().filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    # Найти пользователей, у которых нет блогов, отсортировать по возрастанию id (функция get_user_that_dont_have_blog).
    return User.objects.annotate(count_blogs=Count('blog')).filter(count_blogs=0).order_by('id')


def get_topic_that_like_all_users():
    # Найти топик, который лайкнули все пользователи (функция get_topic_that_like_all_users).
    lu = User.objects.all().count()
    return Topic.objects.annotate(count_likes=Count('likes')).filter(count_likes=lu)


def get_topic_that_dont_have_like():
    # Найти топики, у которы нет лайков (функция get_topic_that_dont_have_like).
    return Topic.objects.annotate(count_likes=Count('likes')).filter(count_likes=0)

