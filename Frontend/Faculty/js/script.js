function startAttendance() {

  fetch('/start-attendance', {
    method: 'POST'
  })

  .then(res => res.json())

  .then(data => {
    alert(data.message || "Attendance started!");
  })

  .catch(err => {
    alert("Error starting attendance");
  });

}
