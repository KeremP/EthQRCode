from typing import Union, Optional, Dict
from .constants import _netname_to_id
from web3 import Web3

class EIP681:
    """
    EIP681 base class


    Attributes
    ----------
    chain: str | int, optional
        Specifies the chain to target. Defaults to 1 (ETH mainnet). Takes either chain name or id. Note: limited number of chain names to id are currently mapped.
 
    Methods
    -------
    build_tx_url(target, payment=False, amount=None, decimals=18, function=None, params=None)
        Builds EIP681 transaction url.
    """
    def __init__(self, chain: Optional[Union[str, int]] = None):
        self.chain = 1
        if chain is not None:
            if type(chain) is str:
                if chain not in _netname_to_id.keys():
                    raise KeyError("Network name not found or not currently supported.")
                self.chain = _netname_to_id[str]
            elif type(chain) is int:
                self.chain = chain

    def build_tx_url(
        self,
        target: str, 
        payment: bool = False,
        amount: Optional[Union[int, float]] = None, 
        decimals: int = 18,
        function: Optional[str] = None, 
        params: Optional[Dict[str,str]] = None) -> str:
        """
        Build EIP681 transaction url.

        Parameters
        ----------
        target : str
            Target address (can be ETH wallet or contract). Must be valid address.

        payment: bool
            Flag that indicates whether this transaction is a payment request. Prepends 'pay-' to start of url.
            Not required for ETH transfers (default is False).

        amount: float, optional
            Amount of ETH to send in ETH transfer.
        
        decimals: int
            Used to specify decimals to use when coverting to scientific notation per EIP681.
            e.g 10e18 (default is 18).

        function: str, optional
            Contract function name to call. Must be passed with dict of params.

        params: dict[str,str], optional
            Dictionary of contract function call parameters. Should be of format {variable:parameter}.

        Raises
        ------
        TypeError
            If target address is not valid ETH address.
            
        """

        if Web3.isAddress(target) == False:
            raise TypeError("target must be valid eth address")

        # target_address = Web3.toChecksumAddress(target)
        
        dec = 'e'+str(decimals)

        if amount is not None:
            value = str(amount)+dec

        if payment:
            prefix = 'pay-'
            if amount is None:
                raise ValueError("must specify amount of ETH if making payment request")
        else:
            prefix = 'ethereum:'
            if function is None and amount is None:
                raise ValueError("must specify amount of ETH if making payment request")
        
        if function is not None:
            param_string = ''
            for i, (k,v) in enumerate(params.items()):
                param_string+=k+'='+v

            url = f'ethereum:{target}@{self.chain}/{function}?{param_string}'
            return url
        
        url = f'{prefix}{target}@{self.chain}?value={value}'
    
        return url