#Portal URL

from django.conf.urls import url
from django.conf.urls import include
from . import views
from . import views_admini


urlpatterns = [
               url(r'^adm$', views_admini.adminiHome, name='admin home'),
               url(r'^log$', views.index , name='index'),
               url(r'^red', views.red , name='red'),
               url(r'^attend', views.getAttendance, name='attendance'),
               url(r'^registerNewStudent',views.registerNewStudent, name='just testing'),
               url(r'^putmarks',views.putmar, name='testing marks module'),
               url(r'^welcome_page',views.welcomeRedirect, name='redirect to welcome'),
               url(r'^headtest', views.signOut , name='signing out'),
               url(r'^loadingRedirecting', views.loadingRedirecting , name='temp website while leading'),
               url(r'^welcomeNewRege',views.welcomeNewRege, name='welcome new user'),
               url(r'^headtest_exists', views.headtestExists, name='User already registered'),
               url(r'^error', views.errorStudentAcc, name='no record'),
               url(r'^login_redirection_stu.html', views.login_redirection_stu, name='redirecting login students page'),
               url(r'^new_reg_verfiy.html$', views.verifyUser , name='mail verification'),
               url(r'^verification_page.html',views.verification , name='verification'),
               
               
               url(r'^ad.html$', views_admini.forgotLoginDetails, name='forgot details'),
               url(r'^home_ad.html',views_admini.loginHome, name = 'redirect to home'),
               url(r'^enterMarks.html', views_admini.marksDash, name=' marks dashboard'),
               url(r'^temptest.html', views_admini.testing, name='for tests'),
               url(r'^dbokay.html', views_admini.okay, name='updated'),
               url(r'^login_redirection.html', views_admini.login_redirection, name='re')
               ]
