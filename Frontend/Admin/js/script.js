
    function addUser() {
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const role = document.getElementById("role").value;
      fetch('/add-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role })
      })
      .then(res => res.json())
      .then(data => {
        alert("User added!");
        loadFaculty();
      });
    }

    function captureImages() {
      const name = document.getElementById("name").value;
      fetch('/capture-images', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      })
      .then(res => res.json())
      .then(data => {
        alert("Capturing images...");
      });
    }

    function startAttendance() {
      fetch('/start-attendance', {
        method: 'POST'
      })
      .then(res => res.json())
      .then(data => {
        alert("Attendance started!");
      });
    }
   

  
    function showSection(section) {
  document.getElementById("addSection").style.display = "none";
  document.getElementById("facultySection").style.display = "none";
  document.getElementById("attendanceSection").style.display = "none";

  if (section === "add") {
    document.getElementById("addSection").style.display = "block";
  }
  if (section === "faculty") {
    document.getElementById("facultySection").style.display = "block";
    loadFaculty();
  }
  if (section === "attendance") {
    document.getElementById("attendanceSection").style.display = "block";
    loadAttendanceByDate();
  }
}
    function loadFaculty() {
      fetch('/get-faculty')
      .then(res => res.json())
      .then(data => {
        const tbody = document.getElementById("facultyTable");
        tbody.innerHTML = "";
        if (!data.length) {
          tbody.innerHTML = '<tr><td colspan="3"><div class="empty"><div class="empty-icon">👤</div>No faculty added yet.</div></td></tr>';
          return;
        }
        data.forEach(row => {
          const roleClass = row.role === 'admin' ? 'role-admin' : 'role-faculty';
          const dotClass  = row.role === 'admin' ? 'dot-admin'  : 'dot-faculty';
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${row.name}</td>
            <td>${row.email}</td>
            <td><span class="role-badge ${roleClass}"><span class="dot ${dotClass}"></span>${row.role}</span></td>
          `;
          tbody.appendChild(tr);
        });
      });
    }
function showToast(message) {
  const toast = document.getElementById("toast");
  toast.innerText = message;
  toast.style.display = "block";

  setTimeout(() => {
    toast.style.display = "none";
  }, 3000);
}
    function loadAttendanceByDate() {
  const date = document.getElementById("datePicker").value;

  fetch(`/attendance-by-date?date=${date}`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("attendanceBoxes");
      container.innerHTML = "";

      data.forEach(row => {
        const box = document.createElement("div");

        const isPresent = row.status === "Present";

        box.style.width = "150px";
        box.style.padding = "15px";
        box.style.borderRadius = "10px";
        box.style.textAlign = "center";
        box.style.fontWeight = "600";

        box.style.background = isPresent ? "#00e5c320" : "#ff4d4d20";
        box.style.border = isPresent ? "1px solid #00e5c3" : "1px solid #ff4d4d";
        box.style.color = isPresent ? "#00e5c3" : "#ff4d4d";

        box.innerHTML = `
          ${row.name}<br>
          ${row.status}
        `;

        container.appendChild(box);
      });
    });
}

    loadFaculty();
    loadAttendanceByDate();
function showLoader(message="Sending report...") {
  const loader = document.getElementById("loader");
  loader.style.display = "flex";
  loader.querySelector("div:last-child").innerText = message;
}

function hideLoader() {
  document.getElementById("loader").style.display = "none";
}

function getDailyReport() {
  showLoader("Sending Daily Report...");
  
  fetch('/daily-report', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      hideLoader();
      showToast("✅ Daily Report Sent!");
    })
    .catch(err => {
      hideLoader();
      showToast("❌ Failed to send report");
    });
}

function getWeeklyReport() {
  showLoader("Sending Weekly Report...");

  fetch('/weekly-report', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      hideLoader();
      showToast("✅ Weekly Report Sent!");
    })
    .catch(err => {
      hideLoader();
      showToast("❌ Failed to send report");
    });
}

function getMonthlyReport() {
  showLoader("Sending Monthly Report...");

  fetch('/monthly-report', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      hideLoader();
      showToast("✅ Monthly Report Sent!");
    })
    .catch(err => {
      hideLoader();
      showToast("❌ Failed to send report");
    });
}
  