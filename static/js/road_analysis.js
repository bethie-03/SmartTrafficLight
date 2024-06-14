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
var buttonRoadAnalyse = document.getElementById('RoadAnalyse')
var alt = document.querySelector('.alt')
var altInput = document.querySelector('.Inputtext');
var altOutput = document.querySelector('.Outputtext')
var vehicleRange = document.querySelector('.vehicleRange');
var text = document.createElement('p')
text.id = 'persontext'
var InputImage = document.getElementById('InputImage');


function updatePlaceholder2(){
    var selectedOption1 = document.querySelector('input[id=vehicleRange]');

    if (selectedOption1 && placeholderTextVehicle) {
        placeholderTextVehicle.textContent = selectedOption1.value;
    }
}

function yesClick() {
    InputImage.style.display='none';
    yesclick = true;
    buttonProcessImage.style.display='none';
    del.style.display = 'none';
    chooseAnotherFile.style.display='none';
    buttonfileUpload.style.display='flex';
    alt.style.display='none';
    canvas.style.display='none';
    buttonRoadAnalyse.style.display = 'none'
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
        var fileInput = document.getElementById('file_upload');
        var buttonfileUpload = document.querySelector('.browse');

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

var circles = [];
var canvas = document.getElementById('canvas');

function ChoseLane() {
    const ctx = canvas.getContext('2d');
    const radius = 5;
    let selectedCircle = null;
    let offsetX, offsetY;
    const InputImagestyle = window.getComputedStyle(InputImage);

    canvas.width = parseInt(InputImagestyle.width);
    canvas.height = parseInt(InputImagestyle.height);
    ctx.drawImage(InputImage, 0, 0, canvas.width, canvas.height);
    createCircles();

    function createCircles() {
        circles.push({x: parseInt(InputImagestyle.width)/2 - 20, y: parseInt(InputImagestyle.height)/2 - 20, radius: radius});
        circles.push({x: parseInt(InputImagestyle.width)/2 + 20, y: parseInt(InputImagestyle.height)/2 - 20, radius: radius});
        circles.push({x: parseInt(InputImagestyle.width)/2 + 20, y: parseInt(InputImagestyle.height)/2 + 20, radius: radius});
        circles.push({x: parseInt(InputImagestyle.width)/2 - 20, y: parseInt(InputImagestyle.height)/2 + 20, radius: radius});
        drawCircles();
    }

    function drawCircles() {
        const color = ['red', 'green', 'blue', 'purple']
        for(let i = 0; i < circles.length; i++){
            ctx.beginPath();
            ctx.arc(circles[i].x, circles[i].y, circles[i].radius, 0, Math.PI * 2);
            ctx.fillStyle = color[i];
            ctx.strokeStyle = 'white'
            ctx.fill();
            ctx.stroke();
        }
    }

    function getMousePos(canvas, evt) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: evt.clientX - rect.left,
            y: evt.clientY - rect.top
        };
    }

    function getCircleUnderMouse(x, y) {
        return circles.find(circle => {
            return Math.sqrt((circle.x - x) ** 2 + (circle.y - y) ** 2) < radius;
        });
    }

    canvas.addEventListener('mousedown', function(e) {
        const mousePosition = getMousePos(canvas, e);
        selectedCircle = getCircleUnderMouse(mousePosition.x, mousePosition.y);
        if (selectedCircle) {
            offsetX = mousePosition.x - selectedCircle.x;
            offsetY = mousePosition.y - selectedCircle.y;
        }
    });

    function redraw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(InputImage, 0, 0, canvas.width, canvas.height);
        drawCircles();
    }

    canvas.addEventListener('mousemove', function(e) {
        if (selectedCircle) {
            const mousePosition = getMousePos(canvas, e);
            selectedCircle.x = mousePosition.x - offsetX;
            selectedCircle.y = mousePosition.y - offsetY;
            redraw();
        }
    });

    canvas.addEventListener('mouseup', function() {
        selectedCircle = null;
    });

    InputImage.style.display='none';
    canvas.style.display='block';
    buttonProcessImage.style.display='none';
    buttonRoadAnalyse.style.display = 'block';

}

function filter_coordinates() {
    const circles_coordinates = []
    for (let i = 0; i< circles.length; i++) {
        circles_coordinates.push([circles[i].x/canvas.width, circles[i].y/canvas.height])
    }
    return circles_coordinates
}

function processImage() {
    var formData = new FormData();
    const roadLength = document.getElementById('roadLength')
    const motorcycle_speed = document.getElementById('motorcycle_speed')
    const car_speed = document.getElementById('car_speed')
    const circles_coordinates = filter_coordinates()

    formData.append('imagesrc', InputImage.src);
    formData.append('top_left', circles_coordinates[0]);
    formData.append('top_right', circles_coordinates[1]);
    formData.append('bottom_right', circles_coordinates[2]);
    formData.append('bottom_left', circles_coordinates[3]);

    formData.append('roadLength', roadLength.value);
    formData.append('motorcycle_speed', motorcycle_speed.value);
    formData.append('car_speed', car_speed.value);

    processing_dots.style.display='flex'
    dots.style.display='flex'

    fetch('/analyse-image', {
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
        InputImage.title = 'After analyse';
        InputImage.src = data.result;
        InputImage.style.display='block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
    alt.style.display = 'block';
    altInput.style.display='none';
    altOutput.style.display='block';
    processing_dots.style.display='none';
    dots.style.display='none';
    canvas.style.display = 'none';
    buttonRoadAnalyse.style.display='none'
}
