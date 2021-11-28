button = document.getElementById("login-btn");

document.addEventListener('change',e=>{
  if ([...document.querySelectorAll("input[name='user_name'], input[name='password']")].map(x=>x.value).includes("")) {
    button.disabled = true;
  } else {
    button.disabled = false;
  }
})
