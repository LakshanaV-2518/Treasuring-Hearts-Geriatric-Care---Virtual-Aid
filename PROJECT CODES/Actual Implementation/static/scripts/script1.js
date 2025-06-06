const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {    
  container.classList.remove("sign-up-mode");
});

const loginForm = document.querySelector('.sign-in-form');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    console.log(username, password);

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('/login_form', {
        method: 'POST',
        body: formData,
    });
    
    const data = await response.json();

    console.log('Response:', data);
    
    if (data.status === 'success') {
        alert(data.message);
        window.location.href = 'http://127.0.0.1:5500/Front%20End%20Design%20Codes/Actual%20Implementation/index.html';
    } else {
        alert(data.message);
    }
});

const registrationForm = document.querySelector('.sign-up-form');

registrationForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username1 = document.getElementById('username1').value;
    const password1 = document.getElementById('password1').value;
    const email = document.getElementById('email').value;

    console.log(username1, password1, email);

    const formData = new FormData();
    formData.append('username1', username1);
    formData.append('password1', password1);
    formData.append('email', email);

    const response = await fetch('/register', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();

    console.log(data);

    if (data.status === 'success') {
        alert(data.message);
    } else {
        alert(data.message);
    }
});