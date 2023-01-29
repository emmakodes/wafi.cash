from rest_framework.decorators import action
from rest_framework.response import Response

class P2PViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def deposit(self, request, pk=None):
        user = self.get_object()
        user.balance += request.data.get('amount')
        user.save()
        return Response({'status': 'Deposit successful'})

    @action(detail=False, methods=['post'])
    def send_money(self, request, pk=None):
        sender = self.get_object()
        receiver = User.objects.get(pk=request.data.get('receiver'))
        amount = request.data.get('amount')
        if sender.balance < amount:
            return Response({'status': 'Insufficient balance'})
        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()
        return Response({'status': 'Transaction successful'})

    @action(detail=False, methods=['post'])
    def transfer_out(self, request, pk=None):
        user = self.get_object()
        user.balance -= request.data.get('amount')
        user.save()
        return Response({'status': 'Transfer out successful'})

    @action(detail=False, methods=['get'])
    def check_balance(self, request, pk=None):
        user = self.get_object()
        return Response({'balance': user.balance})
