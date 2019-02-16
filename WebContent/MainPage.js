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


