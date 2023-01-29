from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
from .models import User, Transaction
from .serializers import UserSerializer, TransactionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def deposit(self, request):
        user = self.get_object()
        user.balance += Decimal(request.data['amount'])
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_money(self, request, pk=None):
        sender = self.get_object()
        receiver = User.objects.get(id=request.data['receiver_id'])
        amount = Decimal(request.data['amount'])
        if sender.balance < amount:
            return Response(status=400, data={'error': 'Insufficient funds'})
        sender.balance -= amount
        sender.save()
        receiver.balance += amount
        receiver.save()
        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
        return Response(status=204)

    @action(detail=True, methods=['get'])
    def balance(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        user = self.get_object()
       
