/**
 * 
 */
var img;
var pic;
var reader = new FileReader();

function uploadFile(files) {
    reader.onload = function (pic) {
    	img.style.backgroundImage = 'url(' + pic.target.result + ')';
    };
    reader.readAsDataURL(files[0]);
    var req = new XMLHttpRequest();
    var url = "https://www.googleapis.com/upload/storage/v1/b/hackathon2019/o?uploadType=media&name="+files[0].name;
    req.open("POST",url);
    req.setRequestHeader("Authorization", "Bearer ya29.GlyzBmBoYan8h1ZJTHXFqhBnh7ohNeSh2QMNUtWRyp23zh-wU3N_SInWIsGw1KhwkwJOEk1llNY0qDHhCA5EvECeaiqcDmO7Mg4OPWKsxopQHCsDkcU_Z13qrHMHyw");
    req.setRequestHeader("Content-Type", files[0].type);
    var blob = new Blob(files);
    req.send(blob);
    req.onreadystatechange = function () {
        if(this.readyState==4 && this.status==200){
            var json = JSON.parse(req.responseText);
            console.log(req.responseText);
            // send the  file  name to your python
            url = "http://34.73.56.231/python/hackathon.py";
            req.open("POST",url);
            var json = JSON.parse(req.responseText);
            console.log(req.responseText);
        }
    };

}

window.onload = function() {
	img = document.getElementById("getPic");  
    }

function showFileInput() {
	var fileInput = document.getElementById("fileInput");
    fileInput.click();
}

function stepscondition() {
	var element = document.getElementById("step1");   
    if(element.style.display=="none")  {
    	element.style.display="";  
    }else{
    	element.style.display="none";   
    }    
}


