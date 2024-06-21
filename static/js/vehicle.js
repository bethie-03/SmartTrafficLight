document.addEventListener('DOMContentLoaded', function() {
    var dots = document.querySelector('.dots').children;
    var menu = document.querySelector('.menu');
    var menuIcon = document.getElementById('menu_icon');
    var Home_selection = document.getElementById('Home');
    var RA_selection = document.getElementById('RA');
    var Demo_selection = document.getElementById('Demo');
    var click = true

    menuIcon.addEventListener('click', function(event) {
        if (click){
            menu.style.display = 'flex';
            click = false;
        } else{
            menu.style.display = 'none';
            click = true;
        }
        event.stopPropagation();
    });

    document.addEventListener('click', function(event) {
        if (!menu.contains(event.target) && !menuIcon.contains(event.target)) {
            menu.style.display = 'none';
            click = true;
        }
    });

    Home_selection.addEventListener('click', function() {
        window.location.href = '/';
    })

    RA_selection.addEventListener('click', function() {
        window.location.href = '/RA-template';
    })

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
var Output = document.querySelector('.Output');
var yesclick = true;
var chooseAnotherFile = document.querySelector('.chooseOtherfiles')
var buttonfileUpload = document.querySelector('.browse')
var placeholderText = document.getElementById("placeholderText");
var pause=false;
var processing_dots = document.querySelector('.processing_dots')
var buttonPause =  document.getElementById('Pause')
var buttonProcessImage = document.getElementById('ProcessImage')
var buttonProcessVideo = document.getElementById('ProcessVideo')
var buttonProcessVideoRealtime = document.getElementById('ProcessVideoRealtime')
var placeholderTextVehicle = document.getElementById("placeholderText3");
var alt = document.querySelector('.alt')
var altInput = document.querySelector('.Inputtext')
var altOutput = document.querySelector('.Outputtext')
var vehicleRange = document.querySelector('.vehicleRange');
var text = document.createElement('p')
text.id = 'persontext'


function updatePlaceholder() {
    var fileUpload = document.getElementById("file_upload");
    var selectedOption = document.querySelector('input[name=input_type]:checked');

    if (selectedOption) {
        switch (selectedOption.value) {
            case "image":
                placeholderText.textContent = "Choose an image";
                fileUpload.accept = "image/*"; 
                buttonfileUpload.style.display = 'block';
                break;
            case "video":
                placeholderText.textContent = "Choose a video";
                fileUpload.accept = "video/*"; 
                buttonfileUpload.style.display = 'block';
                break;
            case "video_realtime":
                placeholderText.textContent = "Choose a video";
                fileUpload.accept = "video/*"; 
                buttonfileUpload.style.display = 'block';
                break;
        }
    } else {
        buttonfileUpload.style.display = 'none';
    }
}

function updatePlaceholder2(){
    var selectedOption1 = document.querySelector('input[id=vehicleRange]');

    if (selectedOption1 && placeholderTextVehicle) {
        placeholderTextVehicle.textContent = selectedOption1.value;
    }
}

function yesClick() {
    Input.innerHTML = '';
    Output.innerHTML = '';
    yesclick = true;
    buttonProcessImage.style.display='none'
    buttonProcessVideo.style.display='none'
    buttonProcessVideoRealtime.style.display='none'
    buttonPause.style.display='none'
    del.style.display = 'none';
    chooseAnotherFile.style.display='none';
    buttonfileUpload.style.display='block';
    placeholderText.style.display='block';
    alt.style.display='none'
    Output.style.display='none'
    Input.style.width= "100%";
}

function noClick() {
    yesclick = false;
    del.style.display = 'none';
    chooseAnotherFile.style.display='block';
    buttonfileUpload.style.display='none';
    placeholderText.style.display='none';
}

function pauseVideo(){
    var placeholderText2 = document.querySelector(".placeholderText2");
    var VidElement1 = document.getElementById('InputVideo')
    var VidElement2 = document.getElementById('OutputVideo')
    if (!pause){
        VidElement1.play()
        VidElement2.play()
        placeholderText2.textContent = "Pause";
        pause=true;
    } else{
        VidElement1.pause()
        VidElement2.pause()
        placeholderText2.textContent = "Play";
        pause=false;
    }
}

function checkFile() {
    var images = Input.getElementsByTagName('img');
    var videos = Input.getElementsByTagName('video');
    if (images.length > 0 || videos.length > 0) {
        del.style.display = 'flex';
    } else {
        yesclick = true;
    }
}

function uploadImage() {
    if (yesclick) {
        var fileInput = document.getElementById('file_upload')
        var selectedOption = document.querySelector('input[name=input_type]:checked');
        var buttonfileUpload = document.querySelector('.browse')
        var reader = new FileReader();
        file = fileInput.files[0]
        if (file) {
            reader.onload = function(e) {
                if (selectedOption.value == 'image'){
                    var Element = document.createElement('img');
                    Element.id='InputImage'
                    Element.title='Default Image'
                    Element.style.display='block'
                    buttonProcessImage.style.display='block'
                } else if (selectedOption.value == 'video' || selectedOption.value == 'video_realtime'){
                    var Element = document.createElement('video');
                    Element.id='InputVideo'
                    Element.title='Default Video'
                    Element.autoplay=false;
                    Element.style.display='block'
                    if (selectedOption.value == 'video'){
                        buttonProcessVideo.style.display='block'
                    } else if (selectedOption.value == 'video_realtime') {
                        buttonProcessVideoRealtime.style.display='block'
                    }
                }
                Element.src = e.target.result
                Input.appendChild(Element);
                fileInput.value = '';
            }
            reader.readAsDataURL(file)
        } else {
            alert('Please choose a file!');
        }
        chooseAnotherFile.style.display='block';
        buttonfileUpload.style.display='none';
        placeholderText.style.display='none';
    } else {
        alert('false');
    }
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
        Output.appendChild(Element);
        Input.style.width= "50%";
        Output.style.display='flex';
        alt.style.display = 'flex';
        processing_dots.style.display='none';
        dots.style.display='none';
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    buttonProcessImage.style.display='none'
    
}

function processVideo() {
    var vidElement = document.getElementById('InputVideo');
    var formData = new FormData();
    formData.append('video', vidElement.src);
    formData.append('vehicle_cfd', parseInt(placeholderTextVehicle.textContent) / 100);
    processing_dots.style.display='flex'
    dots.style.display='flex'

    fetch('/process-video', {
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
        var Element = document.createElement('video');
        Element.id = 'OutputVideo';
        Element.title = 'Detected Video';
        Element.type = 'video/mp4';
        Element.src = data.result;
        Input.style.width= "50%";
        Output.appendChild(Element);
        Output.style.display = 'flex';
        buttonPause.style.display = 'block';
        buttonProcessVideo.style.display = 'none';
        alt.style.display='flex'
        altInput.innerHTML='Default Video'
        altOutput.innerHTML='Detected Video'
        processing_dots.style.display='none';
        dots.style.display='none';
    })
    .catch(error => {
        console.error('Error:', error);
    });
    buttonProcessVideo.style.display='none'
}

async function processVideoRealtime(){
    var vidElement = document.getElementById('InputVideo');
    var formData = new FormData();
    formData.append('video', vidElement.src);
    formData.append('vehicle_cfd', parseInt(placeholderTextVehicle.textContent) / 100);

    var Element = document.createElement('img');
    Element.id = 'OutputVideo';
    Element.title = 'Detected Video';
    Input.style.width= "50%";
    buttonProcessVideoRealtime.style.display = 'none';
    alt.style.display='flex'
    altInput.innerHTML='Default Video'
    altOutput.innerHTML='Detected Video'
    processing_dots.style.display='flex'
    dots.style.display='flex'

    const response = await fetch('/process_video_realtime',{
        method : 'POST',
        body : formData
    })
    vidElement.play()
    Output.appendChild(Element);
    Output.style.display = 'flex';
    
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    while (true){
        const {value, done} = await reader.read();
        if (done) {
            console.log(value)
            processing_dots.style.display='none';
            dots.style.display='none';
            break;
        }
        const url = decoder.decode(value)
        console.log(url)
        Element.src = url
    }
}