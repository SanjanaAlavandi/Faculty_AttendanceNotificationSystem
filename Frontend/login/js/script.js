function fillDemo(email, pass) {
    document.getElementById('email').value = email;
    document.getElementById('password').value = pass;
    document.getElementById('errorBox').style.display = 'none';
  }

  function togglePwd() {
    const inp = document.getElementById('password');
    const btn = document.getElementById('eyeBtn');
    if (inp.type === 'password') { inp.type = 'text'; btn.textContent = '🙈'; }
    else { inp.type = 'password'; btn.textContent = '👁'; }
  }

  function handleSignIn() {
  const email = document.getElementById('email').value;
  const pass = document.getElementById('password').value;
  const box = document.getElementById('errorBox');

  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: email,
      password: pass
    })
  })
  .then(res => res.json())
  .then(data => {
    console.log(data);  
    if (data.status === "success") {
      box.style.background = 'rgba(52,211,153,0.12)';
      box.style.borderColor = 'rgba(52,211,153,0.3)';
      box.style.color = '#34d399';
      box.textContent = '✓ Signed in successfully!';
      box.style.display = 'flex';
      if (data.role === "admin") {
      window.location.href = "/admin-dashboard";
      } else {
    window.location.href = "/faculty-dashboard";
  }
      
    } else {
      box.style.background = 'var(--error-bg)';
      box.style.borderColor = 'rgba(248,113,113,0.3)';
      box.style.color = 'var(--error)';
      box.textContent = '⚠ Invalid email or password.';
      box.style.display = 'flex';
    }
  });
}

function startAttendance() {
  fetch('/start-attendance', {
    method: 'POST'
  })
  .then(res => res.json())
  .then(data => {
    alert("Attendance system started!");
  });
}
  
  document.querySelectorAll('.tab').forEach(t => {
    t.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
      t.classList.add('active');
    });
  });