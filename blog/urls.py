from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name="post-detail"),
    path('category/<str:cat>', views.category, name='category'),
    path('refresh/', views.refresh, name="blog-refresh"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html', redirect_authenticated_user=True),
         name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update-profile/', views.update, name='update_profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view
    (template_name='blog/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
    (template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view
    (template_name='blog/password_reset_complete.html'), name='password_reset_complete'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
