document.addEventListener('DOMContentLoaded', function() {
    var dots = document.querySelector('.dots').children;

    for (let i = 0; i < dots.length; i++) {
        setTimeout(function() {
            toggleDot(dots[i]);
        }, i * 300); 
    }
});

function toggleDot(dot) {
    dot.style.background = 'white';
    increaseMargin(dot, 0); 

    setTimeout(function() {
        dot.style.background = 'black';

        setTimeout(function() {
            toggleDot(dot);
        }, 1000);
    }, 300); 
}

function increaseMargin(dot, count) {
    if (count < 10) {
        let currentMargin = parseInt(dot.style.marginBottom, 10) || 0;
        dot.style.marginBottom = `${currentMargin + 1}px`;

        setTimeout(function() {
            increaseMargin(dot, count + 1);
        }, 30); 
    } else {
        decreaseMargin(dot, 10);
    }
}

function decreaseMargin(dot, count) {
    if (count > 0) {
        let currentMargin = parseInt(dot.style.marginBottom, 10) || 0;
        dot.style.marginBottom = `${currentMargin - 1}px`;

        setTimeout(function() {
            decreaseMargin(dot, count - 1);
        }, 30); 
    }
}


var del = document.querySelector('.del');
var dots = document.querySelector('.dots');
var Input = document.querySelector('.Input');
var yesclick = true;
var chooseAnotherFile = document.querySelector('.chooseOtherfiles')
var buttonfileUpload = document.querySelector('.browse')
var processing_dots = document.querySelector('.processing_dots')
var buttonProcessImage = document.getElementById('ProcessImage')
var alt = document.querySelector('.alt')
var altOutput = document.querySelector('.Outputtext')
var vehicleRange = document.querySelector('.vehicleRange');
var text = document.createElement('p')
text.id = 'persontext'


function updatePlaceholder2(){
    var selectedOption1 = document.querySelector('input[id=vehicleRange]');

    if (selectedOption1 && placeholderTextVehicle) {
        placeholderTextVehicle.textContent = selectedOption1.value;
    }
}

function yesClick() {
    var InputImage = document.getElementById('InputImage');
    InputImage.style.display='none';
    yesclick = true;
    buttonProcessImage.style.display='none'
    del.style.display = 'none';
    chooseAnotherFile.style.display='none';
    buttonfileUpload.style.display='flex';
    alt.style.display='none'
}

function noClick() {
    yesclick = false;
    del.style.display = 'none';
    chooseAnotherFile.style.display='block';
    buttonfileUpload.style.display='none';
    alt.style.display='block';
}

function checkFile() {
    var images = Input.getElementsByTagName('img');
    if (images.length > 0) {
        del.style.display = 'flex';
    } else {
        yesclick = true;
    }
}

function uploadImage() {
    if (yesclick) {
        var InputImage = document.getElementById('InputImage');
        var fileInput = document.getElementById('file_upload');
        var buttonfileUpload = document.querySelector('.browse');
        var altInput = document.querySelector('.Inputtext');

        var reader = new FileReader();
        file = fileInput.files[0]

        if (file) {
            reader.onload = function(e) {
                InputImage.title = 'Before analyse';
                InputImage.src = e.target.result;
                InputImage.style.display='block';
                buttonProcessImage.style.display='block';
            }
            reader.readAsDataURL(file)
        } else {
            alert('Please choose a file!');
        }

        alt.style.display='block';
        altInput.style.display='block';
        chooseAnotherFile.style.display='block';
        buttonfileUpload.style.display='none';
    } else {
        alert('false');
    }
}

function ChoseLane() {

}

function processImage() {
    var imageElement = document.getElementById('InputImage');
    var Element = document.createElement('img');
    Element.id='OuputImage'
    Element.title='Detected Image'
    var formData = new FormData();
    formData.append('image', imageElement.src);
    formData.append('vehicle_cfd', parseInt(placeholderTextVehicle.textContent) / 100);
    processing_dots.style.display='flex'
    dots.style.display='flex'
    fetch('/process-image', {
        method: 'POST',
        body: formData
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        Element.src = data.result;
        alt.style.display = 'flex';
        processing_dots.style.display='none';
        dots.style.display='none';
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    buttonProcessImage.style.display='none'
    
}
