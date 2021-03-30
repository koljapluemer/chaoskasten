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
    # signup is direct, convert is for people who had a temporary acc
    path('signup', views.signup),
    path('convert', include('lazysignup.urls'), {'template_name': 'pages/signup.html'}),
    path('convertdone', views.payment_form),

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
    path('open/<slug:noteID>/<str:redirectPath>', views.openNote),
    path('close/<slug:noteID>/<str:redirectPath>', views.closeNote),
    path('closeNotes', views.closeNotes),

    # paginator url
    path('changePage/<str:section>/<int:pageNr>', views.changePage),
    path('pin/<int:noteID>', views.pinNote),
    path('unpin/<int:noteID>', views.unpinNote),

    # Connecting in the notes view
    path('notes/s/<int:sender>', views.activateConnectionSender),
    path('notes/r/<int:recipient>', views.attachConnectionRecipient),
    path('notes/deactiveConnectionMode', views.deactiveConnectionMode),
    path('unconnect/<int:sender>/<int:recipient>', views.unconnectNotes),

    # Editing/new Notes
    path('editMode/<int:noteID>/<str:editmode>', views.notes),
    path('editMode/<str:editmode>', views.notes),


    # Drawer View
    path('drawerView', views.drawerView),
    path('drawerSearch', views.drawerSearch),

    # webhooks
    # path('webhook', views.webhook),

    # collapse sidebar
    path('sidebar', views.sidebar),

    # new attempt to get stripe running
    path('success/', views.success),
    path('cancel/', views.cancel),

    # yet another attempt to stripe
    path('payment_form', views.payment_form),

    # Learning
    path('learning', views.learning_queue, {'show_backsite': False}),
    path('learning/show_backsite', views.learning_queue, {'show_backsite': True}),
    path('learning/get_new', views.open_new_learning_object),
    path('learning/delete/<int:pk>', views.remove_learning_object),
]
