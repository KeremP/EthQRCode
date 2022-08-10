const csrf = document.querySelector('[name=csrfmiddlewaretoken]');

const generate_qrcode = async(id) => {
    await fetch('/generate-qrcode/',{
        method:'POST',
        credentials:'same-origin',
        headers:{
            'Accept':'application/json',
            'Content-Type':'application/json',
            'X-CSRFToken':csrf
        },
        body:JSON.stringify({
            tx_id:id
        })
    }).then(async(resp) => {
        const result = await resp.json();
        let qr = 'data:image/png;base64,'+result.qr_encoded;
        document.getElementById('qr-code').src = qr;
    }, (error) => {
        console.log(error);
    })
}

const generate_tx = async () => {
    let target = document.getElementById('target').value;
    let amount = document.getElementById('amount').value;
    console.log(amount)
    if (amount == null || amount == undefined || amount == '') {
        amount = 0;
    } else {
        amount = parseInt(amount);
    }

    let payment = document.getElementById('payment').checked;
    let function_name = document.getElementById('function').value;
    let function_params = document.getElementById('params').value;


    await fetch('/create-tx/',{
        method:'POST',
        credentials:'same-origin',
        headers:{
            'Accept':'application/json',
            'Content-Type':'application/json',
            'X-CSRFToken':csrf
        },
        body:JSON.stringify({
            target:target,
            amount:amount,
            payment:payment,
            function:function_name,
            params:function_params
        })
    }).then(async(resp) => {
        const result = await resp.json();
        const url_display = document.getElementById('url');
        url_display.innerHTML = result.transaction_url;
        
        generate_qrcode(result.id);
        
        console.log(result);

    }, (error) => {
        console.log(error);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const submit = document.getElementById('submit');
    submit.addEventListener('click', (event) => {
        event.preventDefault();
        generate_tx();
    });
});