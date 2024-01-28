/*..............text captcha......................*/
const captchaTextBox = document.querySelector(".captcha_box input");
const refreshButton = document.querySelector(".text-captcha-refresh_button");
const captchaInputBox = document.querySelector(".captcha_input input");



// Variable to store generated captcha
let captchaText = null;

// Function to generate captcha
const generateCaptcha = () => {
  const randomString = Math.random().toString(36).substring(2, 7);
  const randomStringArray = randomString.split("");
  const changeString = randomStringArray.map((char) => (Math.random() > 0.5 ? char.toUpperCase() : char));
  captchaText = changeString.join("   ");
  captchaTextBox.value = captchaText;
  /*console.log(captchaText);*/
};

const refreshBtnClick = () => {
  generateCaptcha();
  captchaInputBox.value = "";
};


// Add event listeners for the refresh button, captchaInputBox, submit button
refreshButton.addEventListener("click", refreshBtnClick);

// Generate a captcha when the page loads
generateCaptcha();
/*..............text captcha......................*/
