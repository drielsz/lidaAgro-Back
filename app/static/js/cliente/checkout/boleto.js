document.addEventListener("DOMContentLoaded", async () => {
  var stripe = Stripe(
    "pk_test_51KxGDlIax2mPdViIVFlWOMYIGHp8tgu1BY6Agl7inQdkP08q207YJAnyAUW4hKfw2ik2jLq7Qof9rjw2yUvUPJ4z00irU0sLKP"
  );
  const form = document.querySelector("#payment-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const { error: backendError, clientSecret } = await fetch(
      "/create-payment-intent",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          paymentMethodType: "boleto",
          currency: "brl",
        }),
      }
    ).then((r) => r.json());

    if (backendError) {
      addMessage(backendError.message);
      return;
    }
    const name = document.querySelector("#name");
    const email = document.querySelector("#email");
    const address = document.querySelector("#address");
    const city = document.querySelector("#city");
    const state = document.querySelector("#state");
    const postalCode = document.querySelector("#postal_code");
    const country = document.querySelector("#country");
    const taxId = document.querySelector("#tax_id");

    const { error, paymentIntent } = await stripe.confirmBoletoPayment(
      clientSecret,
      {
        payment_method: {
          billing_details: {
            address: {
              line1: address.value,
              city: city.value,
              state: state.value,
              postal_code: postalCode.value,
              country: country.value,
            },
            name: name.value,
            email: email.value,
          },
          boleto: {
            tax_id: taxId.value,
          },
        },
      }
    );
    if (error) {
        addMessage(error.message)
        return
    }
    addMessage('Payment ${paymentIntent.status}: ${paymentIntent.id}')
  });
});


