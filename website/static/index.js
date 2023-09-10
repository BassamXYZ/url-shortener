function deleteUrl(urlId) {
  fetch("/delete-url", {
    method: "POST",
    body: JSON.stringify({ urlId: urlId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function clicks(urlId, mainUrl) {
  fetch("/clicks", {
    method: "POST",
    body: JSON.stringify({ urlId: urlId }),
  }).then((_res) => {
    console.log("success");
    window.location.href = mainUrl;
  });
}