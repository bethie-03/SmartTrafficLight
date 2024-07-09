document.addEventListener('DOMContentLoaded', function() {
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

    Demo_selection.addEventListener('click', function() {
        window.location.href = '/Pygame-template';
    })
    
});

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
var resultBox = document.querySelector('.result')
var dotsChildren = document.querySelector('.dots').children;
var originMargin = parseInt(dotsChildren[0].style.marginBottom, 10) || 0;
var shouldStop = false;
var haveSelectedOption = 0
var previousSelectedValue = null

function resetMargin() {
    for (let i = 0; i < dotsChildren.length; i++) {
        dotsChildren[i].style.marginBottom = `${originMargin}px`;
    }
}

function processingDots() {
    shouldStop = false;
    resetMargin();

    for (let i = 0; i < dotsChildren.length; i++) {
        setTimeout(function() {
            if (!shouldStop) {
                toggleDot(dotsChildren[i]);
            }
        }, i * 300); 
    }

    function toggleDot(dot) {
        if (shouldStop) return;

        dot.style.background = 'white';
        increaseMargin(dot, 0);

        setTimeout(function() {
            if (shouldStop) return;

            dot.style.background = 'black';

            setTimeout(function() {
                if (!shouldStop) {
                    toggleDot(dot);
                }
            }, 1000);
        }, 300); 
    }

    function increaseMargin(dot, count) {
        if (shouldStop) return;
        
        if (count < 10) {
            let currentMargin = parseInt(dot.style.marginBottom, 10) || 0;
            dot.style.marginBottom = `${currentMargin + 1}px`;

            setTimeout(function() {
                if (!shouldStop) {
                    increaseMargin(dot, count + 1);
                }
            }, 30); 
        } else {
            decreaseMargin(dot, 10);
        }
    }

    function decreaseMargin(dot, count) {
        if (shouldStop) return;
        
        if (count > 0) {
            let currentMargin = parseInt(dot.style.marginBottom, 10) || 0;
            dot.style.marginBottom = `${currentMargin - 1}px`;

            setTimeout(function() {
                if (!shouldStop) {
                    decreaseMargin(dot, count - 1);
                }
            }, 30); 
        }
    }
}

function stopProcessingDots() {
    shouldStop = true;
}

function updatePlaceholder() {
    var fileUpload = document.getElementById("file_upload");
    var selectedOption = document.querySelector('input[name=input_type]:checked');
    let radios = document.querySelectorAll('input[type="radio"]');

    if (selectedOption) {
        console.log(previousSelectedValue)
        if (Input.querySelector('video') !== null || Input.querySelector('img') !== null){
        del.style.display = 'flex';
        radios.forEach(radio => {
            if (radio.value === previousSelectedValue) {
                radio.checked = true;
                previousSelectedValue = radio.value
            }
        });

        } else{
            del.style.display = 'none';
            previousSelectedValue = selectedOption.value
        }

        switch (selectedOption.value) {
            case "image":
                placeholderText.textContent = "Choose an image";
                fileUpload.accept = "image/*"; 
                buttonfileUpload.style.display = 'block';
                resultBox.style.height = '350px';
                break;
            case "video":
                placeholderText.textContent = "Choose a video";
                fileUpload.accept = "video/*"; 
                buttonfileUpload.style.display = 'block';
                resultBox.style.height = '350px';
                break;
            case "video_realtime":
                placeholderText.textContent = "Choose a video";
                fileUpload.accept = "video/*"; 
                buttonfileUpload.style.display = 'block';
                resultBox.style.height = '500px';
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

    VidElement2.addEventListener("ended", function() {
        placeholderText2.textContent = "Play";
        pause = false;
    });

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
        processing_dots.style.display='flex'
        dots.style.display='flex'
        processingDots()
        if (file) {
            reader.onload = function(e) {
                if (selectedOption.value == 'image'){
                    var Element = document.createElement('img');
                    Element.id='InputImage'
                    Element.title='Default Image'
                    Element.style.display='block'

                    Element.addEventListener('load', function(){
                        const Elementrect = Element.getBoundingClientRect();
                        alt.style.marginTop = (Elementrect.bottom) + 'px';
                        buttonProcessImage.style.marginTop = (Elementrect.bottom + 20) + 'px';
                        processing_dots.style.marginTop=(Elementrect.bottom + 20) + 'px';
                        alt.style.display='flex';
                        altInput.style.display='block';
                        altOutput.style.display = 'none';
                        buttonProcessImage.style.display='block';
                        stopProcessingDots()
                        processing_dots.style.display='none'
                        dots.style.display='none'
                    })

                } else if (selectedOption.value == 'video' || selectedOption.value == 'video_realtime'){
                    var Element = document.createElement('video');
                    Element.id='InputVideo'
                    Element.title='Default Video'
                    Element.autoplay=false;
                    Element.style.display='block';
                    Element.muted = true;

                    Element.addEventListener('loadedmetadata', function(){
                        const Elementrect = Element.getBoundingClientRect();
                        alt.style.marginTop = (Elementrect.bottom) + 'px';
                        processing_dots.style.marginTop=(Elementrect.bottom + 20) + 'px';
                        alt.style.display='flex';
                        altInput.innerHTML='Default Video';
                        altInput.style.display='block';
                        altOutput.style.display = 'none';

                        if (selectedOption.value == 'video'){
                            buttonProcessVideo.style.marginTop = (Elementrect.bottom + 20) + 'px';
                            buttonPause.style.marginTop = (Elementrect.bottom + 20) + 'px';
                            buttonProcessVideo.style.display='block'
                        } else if (selectedOption.value == 'video_realtime') {
                            buttonProcessVideoRealtime.style.marginTop = (Elementrect.bottom + 20) + 'px';
                            buttonProcessVideoRealtime.style.display='block';
                            buttonPause.style.marginTop = (Elementrect.bottom + 20) + 'px';
                        }
                        stopProcessingDots()
                        processing_dots.style.display='none'
                        dots.style.display='none'
                    })
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
    processingDots()

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
        altOutput.style.display = 'block';
        processing_dots.style.display='none';
        dots.style.display='none';
        stopProcessingDots()
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
    processingDots()

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
        altOutput.style.display = 'block';
        processing_dots.style.display='none';
        dots.style.display='none';
        stopProcessingDots()
    })
    .catch(error => {
        console.error('Error:', error);
    });
    buttonProcessVideo.style.display='none'
}

function processVideoRealtime(){
    var vidElement = document.getElementById('InputVideo');
    var formData = new FormData();
    formData.append('video', vidElement.src);
    formData.append('vehicle_cfd', parseInt(placeholderTextVehicle.textContent) / 100);

    var Element = document.createElement('img');
    Element.id = 'OutputVideo';
    Element.title = 'Detected Video';
    Input.style.display= "none";
    Output.style.width = '100%';
    buttonProcessVideoRealtime.style.display = 'none';
    alt.style.display='flex'
    altInput.style.display='none'
    altOutput.innerHTML='Detected Video'
    altOutput.style.display='block'

    fetch('/process_video_realtime', {
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
        Output.appendChild(Element);
        Output.style.display = 'flex';
        Element.src = "/stream_video";
    })
    .catch(error => {
        console.error('Error:', error);
    });

    processing_dots.style.display='flex'
    dots.style.display='flex'
    processingDots()

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
        resultBox.style.height = '350px'
        Input.style.display= "flex";
        Output.innerHTML = ''
        Element.id = 'OutputVideo';
        Element.title = 'Detected Video';
        Element.type = 'video/mp4';
        Element.src = data.result;
        Input.style.width= "50%";
        Output.style.width = '50%';
        Output.appendChild(Element);
        Output.style.display = 'flex';
        buttonPause.style.display = 'block';
        altInput.style.display = 'block';
        altOutput.style.display = 'block';
        processing_dots.style.display='none';
        dots.style.display='none';
        stopProcessingDots()
    })
    .catch(error => {
        console.error('Error:', error);
    });
}