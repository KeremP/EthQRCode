import qrcode
import base64
from io import BytesIO
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import TemplateView

from .models import Transaction

class QrView(TemplateView):
    template_name = 'index.html'

class TxSerializer(serializers.ModelSerializer):

    transaction_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = '__all__'

    def get_transaction_url(self, obj):
        return obj.transaction_url

@api_view(['POST'])
def create_tx(request):
    """
    Create transaction object
    """
    print(request.data)
    serializer = TxSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_tx(request, pk):
    """
    Get transaction object
    """
    transaction = Transaction.objects.get(id=pk)
    serializer = TxSerializer(transaction)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def generate_qrcode(request):
    """
    Generate transaction qr-code.
    """
    id = request.data.pop('tx_id')
    transaction = Transaction.objects.get(id=id)
    url = transaction.transaction_url
    qr = qrcode.make(url)
    buffered = BytesIO()
    qr.save(buffered, format='PNG')
    qr_encoded = base64.b64encode(buffered.getvalue())
    return Response({'qr_encoded':qr_encoded})