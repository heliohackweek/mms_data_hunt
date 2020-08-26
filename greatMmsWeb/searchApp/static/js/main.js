
document.addEventListener('DomContentLoaded', function() {
  alert.log("done");
  const form = document.getElementById( "form-sitl" ),
        generateBtn = document.getElementById( "generateBtn" );
  generateBtn.addEventListener( "click", function (e) {
      getData();
      alert('donawe');
  });

})
const getData = function() {
  // get the date input
  const dateInput = document.querySelector("#dateInput").value;
  // check for empty
  if (dateInput !== "") {
    alert.log("Error message");
  }
  else {
    // make a request
    console.log('dateInput')
    const url = `/date/${dateInput}`;
    fetchDataFromUrl(url)
      .then(response => console.log(response))
      .catch(error => console.log(error));
  }
}

async function fetchDataFromUrl() {
  const response = await fetch(url);
  const text = await response.text();
  return text;
}
