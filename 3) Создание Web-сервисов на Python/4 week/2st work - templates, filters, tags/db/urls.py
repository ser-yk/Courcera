from django.conf.urls import url, include

from .query import *

f = (
    create(), edit_all(), edit_u1_u2(), delete_u1(), unsubscribe_u2_from_blogs(), get_topic_created_grated(),
     get_topic_title_ended(), get_user_with_limit(), get_topic_count(), get_avg_topic_count(),
     get_blog_that_have_more_than_one_topic(), get_topic_by_u1(), get_user_that_dont_have_blog(),
     get_topic_that_like_all_users(), get_topic_that_dont_have_like()
     )

urlpatterns = [
    url(r'^db/', include('db.urls')),
]

