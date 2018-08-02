from rest_framework import generics, viewsets

from assets.models import Contact
from assets.serializers import ContactSerializer


class ContactViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Contact.objects
    serializer_class = ContactSerializer
