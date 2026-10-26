async function detect() {
  let file = document.getElementById("imageInput").files[0];
  if (!file) {
    alert("Please select an image!");
    return;
  }

  document.getElementById("status").innerText = "Processing...";

  let formData = new FormData();
  formData.append("image", file);

  let response = await fetch("http://localhost:5000/predict", {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    alert("Error from backend");
    return;
  }

  let blob = await response.blob();
  let url = URL.createObjectURL(blob);

  document.getElementById("output").src = url;
  document.getElementById("status").innerText = "Done!";
}