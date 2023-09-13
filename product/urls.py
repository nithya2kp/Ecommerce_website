from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from .views import add_to_cart, show_cart
urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('test/',views.test,name = "test"),
    path('checkout/',views.checkout,name="checkout"),
    path('contact/',views.contact,name="contact"),
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("product-detail/<int:pk>",views.ProductDetail.as_view(),name="product-detail"),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('address/',views.address,name="address"),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='cart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('add-to-cart-new/',views.add_to_cart_new,name="add-to-cart-new"),
    path('update-address/<int:pk>',views.updateAddress.as_view(),name="update-address"),

    #Login Authentication
    path('signup/', views.CustomerRegistrationView.as_view(), name='signup'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name="login.html", authentication_form=LoginForm),name='login'),
    path('password-change/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',form_class =MyPasswordChangeForm,success_url='/passwordchangedone'),name ='password-change'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name = 'passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(template_name='logout.html'),name = 'logout'),

    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),


]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
