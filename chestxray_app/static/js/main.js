/*var img=document.getElementById("img");
img.style.display='none';
var table=document.getElementById("table");
table.style.display='none';
var loading=document.getElementById("loading");
loading.style.display='none';
var btn=document.getElementById("btn_search");*/
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#img_file')
        .attr('src', e.target.result)
        .width(512)
        .height(512);
    };

    reader.readAsDataURL(input.files[0]);
  }
}

function showLoading() {
  var x = document.getElementById("loading");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}