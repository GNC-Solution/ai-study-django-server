from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView

from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('souser.urls')),
    path('', include('soaccess.urls')),
    path('graphql',
         csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
    )
]
