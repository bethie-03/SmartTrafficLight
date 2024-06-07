var del = document.querySelector('.del');
var Input = document.querySelector('.Input');
var Output = document.querySelector('.Output');
var yesclick = true;
var chooseAnotherFile = document.querySelector('.chooseOtherfiles')
var buttonfileUpload = document.querySelector('.browse')
var placeholderText = document.getElementById("placeholderText");
var pause=false;
var buttonPause =  document.getElementById('Pause')
var buttonProcessImage = document.getElementById('ProcessImage')
var buttonProcessVideo = document.getElementById('ProcessVideo')
var buttonProcessVideoRealtime = document.getElementById('ProcessVideoRealtime')
var loadingBar = document.querySelector(".loading_bar");
var placeholderTextVehicle = document.getElementById("placeholderText3");
var alt = document.querySelector('.alt')
var altInput = document.querySelector('.Inputtext')
var altOutput = document.querySelector('.Outputtext')
var vehicleRange = document.querySelector('.vehicleRange');
var text = document.createElement('p')
text.id = 'persontext'
//PersonRange.appendChild(text)

function updatePlaceholder() {
    var fileUpload = document.getElementById("file_upload");
    var selectedOption = document.querySelector('input[name=input_type]:checked');

    if (selectedOption) {
        switch (selectedOption.value) {
            case "image":
                placeholderText.textContent = "Choose an image";
                fileUpload.accept = "image/*"; 
                buttonfileUpload.style.display = 'block';
                /*
                text.textContent = '(no detect person for image)'
                text.style.marginTop = '0px'
                text.style.marginBottom = '5px'
                text.style.fontSize = '11px'
                text.style.fontStyle = 'italic'
                */
                //text.style.display = 'block'
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
        loadingBar.style.width = "0%";
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
                Input.appendChild(Element)
                loadingBar.style.width = "auto";
            }
            reader.onprogress = function(e){
                if(e.lengthComputable){
                    var percentLoaded = (e.loaded/e.total)*100;
                    var percentString = percentLoaded.toString();
                    loadingBar.style.width = percentString + "%"
                }
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
    loadingBar.style.width = "0%";
    var formData = new FormData();
    formData.append('image', imageElement.src);
    formData.append('vehicle_cfd', parseInt(placeholderTextVehicle.textContent) / 100);

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
        loadingBar.style.width = "auto";
        alt.style.display = 'flex'
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
    loadingBar.style.width = "0%";

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
        loadingBar.style.width = "auto";
        buttonPause.style.display = 'block';
        buttonProcessVideo.style.display = 'none';
        alt.style.display='flex'
        altInput.innerHTML='Default Video'
        altOutput.innerHTML='Detected Video'
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

    loadingBar.style.width = "0%";
    var Element = document.createElement('img');
    Element.id = 'OutputVideo';
    Element.title = 'Detected Video';
    Input.style.width= "50%";
    buttonProcessVideoRealtime.style.display = 'none';
    alt.style.display='flex'
    altInput.innerHTML='Default Video'
    altOutput.innerHTML='Detected Video'

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
            loadingBar.style.width = "auto";
            break;
        }
        const url = decoder.decode(value)
        console.log(url)
        Element.src = url
    }
}