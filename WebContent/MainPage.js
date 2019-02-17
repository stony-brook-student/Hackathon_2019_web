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
    req.setRequestHeader("Authorization", "Bearer ya29.GluzBuZk2VmtxDv9Dqo_fnAA_9_FYaOy5LT-mzuFL99e4j907yzTWw0S6qHVD-8loreR-X_cQh87Hi1jTfdwVATo3FQYsZyS3cXQUq5_RVOQz3v-7UvRZXPOBQ-O");
    req.setRequestHeader("Content-Type", files[0].type);
    var blob = new Blob(files);
    req.send(blob);
    req.onreadystatechange = function () {
        if(this.readyState==4 && this.status==200){
            var json = JSON.parse(req.responseText);
            console.log(json);
            // send the  file  name to your python
            url = "http://34.73.56.231/python/hackathon.py";
            req.open("POST",url);
            var json = JSON.parse(req.responseText);
            console.log(json);
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


