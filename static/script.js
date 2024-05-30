document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    const symptoms = document.getElementById('symptoms').value;
    predictDisease(symptoms);
  });
});

function predictDisease(symptoms) {
  const url = '/predict';
  const queryParams = `?symptoms=${symptoms}`; // Construct query parameters
  const fullUrl = url + queryParams;

  fetch(fullUrl)
  .then(response => response.json())
  .then(data => {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    data.forEach(item => {
      const paragraph = document.createElement('p');
      paragraph.textContent = `Disease: ${item.Disease}, Specialist: ${item.Specialist}, Chances: ${item.Chances}%`;
      resultDiv.appendChild(paragraph);
    });

    const specialist = data[0].Specialist;
    const day = prompt('Enter the day of the week (e.g., Monday, Tuesday, etc.):');

    const doctorsUrl = `/find_doctors?specialist=${specialist}&day=${day}`;
    fetch(doctorsUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(doctorData => {
      if (doctorData.length > 0) {
        const doctorsList = document.createElement('ul');
        doctorData.forEach(doctor => {
          const listItem = document.createElement('li');
          listItem.textContent = `${doctor.name} (${doctor.time}), Rating: ${doctor.rating}`;
          doctorsList.appendChild(listItem);
        });
        resultDiv.appendChild(doctorsList);
      } else {
        const noDoctorsMessage = document.createElement('p');
        noDoctorsMessage.textContent = `No doctors found with specialty '${specialist}' available on ${day}.`;
        resultDiv.appendChild(noDoctorsMessage);
      }
    })
    .catch(error => {
      console.error('Error finding doctors:', error);
    });
  })
  .catch(error => {
    console.error('Error predicting disease:', error);
  });
}
