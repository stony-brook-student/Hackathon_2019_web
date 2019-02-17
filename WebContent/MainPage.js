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
    req.setRequestHeader("Authorization", "Bearer ya29.GluzBkFWd862dxlUe3BJ0CGLKq-oroHO0GwMoJ5kapyE6OBQQeCwfjE1gVGw7WEt9aQ-Hh7bdo_PE08_OoBIWdayL54TBtr8d4bSlH6xnIOB3BYdCAYIurBafm8J");
    req.setRequestHeader("Content-Type", files[0].type);
    var blob = new Blob(files);
    req.send(blob);

    req.onreadystatechange = function () {
        if(this.readyState==4 && this.status==200){
            var json = JSON.parse(req.responseText);
            console.log(json.id);
            // send the  file  name to your python
        }
    };
    var element = document.getElementById("baba");

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


