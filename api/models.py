from django.db import models
import json
from .lib.eip681_python import eip681

class Transaction(models.Model):

    target = models.CharField(max_length=42, blank=False)

    amount = models.IntegerField(default=0)

    payment = models.BooleanField(default=False)

    function = models.CharField(max_length=800, blank=True)

    params = models.JSONField(blank=True, null=True)

    chain = models.IntegerField(default=1)

    eip = eip681.EIP681(chain)

    @property
    def transaction_url(self):
        
        if self.payment:
            url = self.eip.build_tx_url(self.target, True, self.amount)
        else:
            if self.function is None or self.function == '':
                url = self.eip.build_tx_url(self.target,amount=self.amount)
            else:
                url = self.eip.build_tx_url(self.target, function=self.function, params=json.loads(str(self.params)))
                
        return url