var ID;
var image_url;

	// get a reference to the input element
const inputElement1 = document.getElementById('file1');
const inputElement2 = document.getElementById('file2');
let uploadedFile1, uploadedFile2;

// Create a FilePond instance
const pond1 = FilePond.create(inputElement1);
const pond2 = FilePond.create(inputElement2);

pond1.on('addfile', (error, file) => {
  if (!error) {
    uploadedFile1 = file.file;
    console.log(uploadedFile1);

  }
});

pond2.on('addfile', (error, file) => {
  if (!error) {
    uploadedFile2 = file.file;
    console.log(uploadedFile2);
  }
});

function uploadData() {

    // const person1 = inputElement.files[0];
    // console.log(inputElement.files);

	// p1 = document.getElementById("file1")
	// p2 = document.getElementById("file2")
	h1 = document.getElementById("height1").value
	h2 = document.getElementById("height2").value

	if (!uploadedFile1 || !uploadedFile2 || !h1 || !h2) {
		alert("upload files first");
	}
	else {
		const jsonData = { height1: h1, height2: h2 };

		const jsonString = JSON.stringify(jsonData);

		const formData = new FormData();
	    formData.append("image1", uploadedFile1);
	    formData.append("image2", uploadedFile2);
	    formData.append("data", jsonString)

	  console.log(formData);

		fetch('/api/upload', {
			method: "POST",
			body: formData
		}).then(res => res.json())
			.then(data => {
				order_id = data["order_id"];
				console.log(order_id);
				ID = order_id;
				image_url = "/media/images/" + ID.toString() + ".jpg"; 

				myInterval = setInterval(function() {
					fetch(image_url)
					.then( res => {
						if (res.ok) {
							clearInterval(myInterval);
							return res.blob();
						}
						else {
							addWaitTag();
						}
					})
					.then(function(blob) {
						image_url = URL.createObjectURL(blob);
						console.log(image_url);
						addIMG(image_url)
					})
				}, 1000);
			})
	    .catch(error => {
	      // Handle the request error
	      console.error(error);
	    });
	}
}

function addIMG(image_name) {
	var html = `<img src="` + image_name + `" alt="final.jpg" width="800" height="500">`;
	img_div = document.getElementById("image-container");
	img_div.innerHTML = html;
}

function addWaitTag() {
	document.getElementById("form1").style.display = "none";
	document.getElementById("form2").style.display = "none";
	document.getElementById("button").style.display = "none";
	document.getElementById("image-container").style.display = "block";
	var html = `<h2 style="position: absolute; top: 10%; left:9%">Your order will display here, please wait..</h2>`
	img_div = document.getElementById("image-container");
	img_div.innerHTML = html;
}

function extractImageFromBlob(blob) {
		  return new Promise((resolve, reject) => {
		    const reader = new FileReader();

		    reader.onloadend = () => {
		      const img = new Image();
		      img.src = reader.result;
		      img.onload = () => resolve(img);
		      img.onerror = reject;
		    };

		    reader.onerror = reject;

		    reader.readAsDataURL(blob);
		  });
		}

