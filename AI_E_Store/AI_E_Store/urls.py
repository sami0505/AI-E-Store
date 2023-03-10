from django.contrib import admin
from django.urls import path
from customerSection import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.register, name='registration'),
    path('verification/<str:token>/', views.verification, name='verification'),
    path('login/', views.attempt_login, name='login'),
    path('resetrequest/', views.request_reset, name='reset_request'),
    path('logout/', views.attempt_logout, name='logout'),
    path('deletion/', views.deletion, name='deletion'),
    path('review/', views.review, name='review'),
    path('category/<str:currentCategory>/', views.category, name='category'),
    path('search/', views.search, name="search"),
    path('detailed/<int:itemID>', views.detailed, name="detailed"),
    path('basket/', views.basket, name="basket"),
    path('addtobasket/<int:styleID>', views.addToBasket, name="addToBasket"),
    path('removefrombasket/<int:styleID>', views.removeFromBasket, name="removeFromBasket"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('addtowishlist/<int:styleID>', views.addToWishlist, name="addToWishlist"),
    path('removefromwishlist/<int:styleID>', views.removeFromWishlist, name="removeFromWishlist"),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
