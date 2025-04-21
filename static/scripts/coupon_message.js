function showCouponMessage(element) {
  const signUpUrl = element.getAttribute("data-signup-url"); //Data signnup url is from frontend in base.html coupon section

  Swal.fire({
    icon: "info",
    title: "Please Sign Up",
    text: "You have to create an account to get a reward coupon.",
    confirmButtonText: "Sign Up",
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = signUpUrl;
    }
  });
}
