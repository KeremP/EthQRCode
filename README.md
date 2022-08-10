# EthQRCode
Example repo demonstrating how to generate EIP681 transaction QR Codes using the [EIP681-python](https://github.com/KeremP/EIP681-python) library

# Example
Run `pip install qrcode[pil] django` to install all requirements

(eip681_python is included under the api/lib directory)

Next run `python manage.py runserver` and navigate to http://127.0.0.1:8000/ to view the sample frontend app.

`Target address` must be a valid ethereum address

`Amount` can be zero or blank and must be an integer. eip681_python appends "e18" to represent 18 decimal format. This can be configured in the package itself but is set as default for this example.

`Contract function` (optional) the name of the contract function being called

`Function params` (required if contract function is set) the parameters to be passed to the smart contract being called in the form: `{"arg1":"val1","arg2":"val2"}`

![app screenshot](/screen.PNG "app screenshot")