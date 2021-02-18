from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # pages
    path('', views.home, name='index'),
    path('accounts/reset/done/', views.home),
    path('about', views.about),

    # settings
    path('settings', views.settings),
    path('settings/editDrawers', views.editDrawers),
    path('generateWelcomeNote', views.generateWelcomeNote),

    # Search
    path('search', views.search),

    # Users
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/changeEmail', views.changeEmail),
    path('signup', views.signup),
    path('payment', views.payment),
    path('profile', views.profile),
    path('deleteUser', views.deleteUser),

    # delete
    path('delete/<int:noteID>', views.deleteNote),

    # I/O
    path('download', views.download),
    path('upload', views.upload),

    # Notes view
    path('notes', views.notes),
    # slug is used to allow a symbol which opens a random note
    path('open/<slug:noteID>', views.openNote),
    path('close/<int:noteID>', views.closeNote),
    path('closeNotes', views.closeNotes),

    # paginator url
    path('changePage/<str:section>/<int:pageNr>', views.changePage),
    path('pin/<int:noteID>', views.pinNote),
    path('unpin/<int:noteID>', views.unpinNote),

    # Connecting in the notes view
    path('notes/<int:sender>', views.notes),
    path('notes/<int:sender>/<int:recipient>', views.notes),
    path('unconnect/<int:sender>/<int:recipient>', views.unconnectNotes),

    # Editing/new Notes
    path('editMode/<int:noteID>/<str:editmode>', views.notes),
    path('editMode/<str:editmode>', views.notes),
    path('convert', include('lazysignup.urls'), {'template_name': 'pages/signup.html', 'redirect_field_name': 'payment'}),

    path('drawerView/<int:drawerID>', views.drawerView),

    # webhooks
    path('webhook', views.webhook),

    # collapse sidebar
    path('sidebar', views.sidebar),
]
