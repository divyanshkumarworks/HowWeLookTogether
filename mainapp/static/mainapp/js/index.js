function uploadData() {
	p1 = document.getElementById("file1")
	p2 = document.getElementById("file2")
	h1 = document.getElementById("height1").value
	h2 = document.getElementById("height2").value

	const file1 = p1.files[0];
	const file2 = p2.files[0];

	const jsonData = { height1: h1, height2: h2 };

	const jsonString = JSON.stringify(jsonData);

	const formData = new FormData();
    formData.append("image1", file1);
    formData.append("image2", file2);
    formData.append("data", jsonString)

	fetch('/api/upload', {
		method: "POST",
		body: formData
	}).then(response => response.json())
	.then(data => {
		image_name = data["message"]
		addIMG(image_name)
	})
    .catch(error => {
      // Handle the request error
      console.error(error);
    });
}

function addIMG(image_name) {
	var html = `<img src="/static/mainapp/images/` + image_name + `" alt="final.jpg" width="600" height="400">`;
	img_div = document.getElementById("image-container");
	img_div.innerHTML = html;
}