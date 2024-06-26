document.addEventListener('DOMContentLoaded', function() {
    var dots = document.querySelector('.dots').children;
    var menu = document.querySelector('.menu');
    var menuIcon = document.getElementById('menu_icon');
    var VD_selection = document.getElementById('VD');
    var Home_selection = document.getElementById('Home');
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

    VD_selection.addEventListener('click', function() {
        window.location.href = '/VD-template';
    })

    Home_selection.addEventListener('click', function() {
        window.location.href = '/';
    })

    for (let i = 0; i < dots.length; i++) {
        dots[i].style.marginBottom = `0px`;
    }

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
    buttonRoadAnalyse.style.display = 'none';
    altOutput.style.display='none';
    dashboard.style.display = 'none';
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
            }
            reader.readAsDataURL(file)
            fileInput.value = '';
        } else {
            alert('Please choose a file!');
        }

        InputImage.addEventListener('load', function(){
            const Imagerect = InputImage.getBoundingClientRect();
            alt.style.marginTop = (Imagerect.bottom) + 'px';
            buttonProcessImage.style.marginTop = (Imagerect.bottom + 20) + 'px';
            buttonRoadAnalyse.style.marginTop = (Imagerect.bottom + 20) + 'px';
            processing_dots.style.marginTop=(Imagerect.bottom + 20) + 'px';;
            alt.style.display='block';
        })

        altInput.style.display='block';
        chooseAnotherFile.style.display='block';
        buttonfileUpload.style.display='none';
        buttonProcessImage.style.display='block';
    } else {
        alert('false');
    }
}

var circles = [];
var canvas = document.getElementById('canvas');

function ChoseLane() {
    const ctx = canvas.getContext('2d');
    const radius = 5;
    const texts = []
    const color = ['red', 'green', 'blue', 'purple']
    
    let selectedCircleIndex, selectedCircle, selectedText = null;
    let offsetX, offsetY;
    
    const InputImagestyle = window.getComputedStyle(InputImage);

    canvas.width = parseInt(InputImagestyle.width);
    canvas.height = parseInt(InputImagestyle.height);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(InputImage, 0, 0, canvas.width, canvas.height);
    createCirclesandTexts();

    function createCirclesandTexts() {
        if (circles.length == 0){
        circles.push({x: parseInt(InputImagestyle.width)/2 - 30, y: parseInt(InputImagestyle.height)/2 - 30, radius: radius});
        circles.push({x: parseInt(InputImagestyle.width)/2 + 30, y: parseInt(InputImagestyle.height)/2 - 30, radius: radius});
        circles.push({x: parseInt(InputImagestyle.width)/2 + 30, y: parseInt(InputImagestyle.height)/2 + 30, radius: radius});
        circles.push({x: parseInt(InputImagestyle.width)/2 - 30, y: parseInt(InputImagestyle.height)/2 + 30, radius: radius});
        } else {
        circles[0]={x: parseInt(InputImagestyle.width)/2 - 30, y: parseInt(InputImagestyle.height)/2 - 30, radius: radius};
        circles[1]={x: parseInt(InputImagestyle.width)/2 + 30, y: parseInt(InputImagestyle.height)/2 - 30, radius: radius};
        circles[2]={x: parseInt(InputImagestyle.width)/2 + 30, y: parseInt(InputImagestyle.height)/2 + 30, radius: radius};
        circles[3]={x: parseInt(InputImagestyle.width)/2 - 30, y: parseInt(InputImagestyle.height)/2 + 30, radius: radius};
        };
        texts.push({x: parseInt(InputImagestyle.width)/2 - 30, y: parseInt(InputImagestyle.height)/2 - 40, content: 'top left', width: 0});
        texts.push({x: parseInt(InputImagestyle.width)/2 + 30, y: parseInt(InputImagestyle.height)/2 - 40, content: 'top right', width: 0});
        texts.push({x: parseInt(InputImagestyle.width)/2 + 30, y: parseInt(InputImagestyle.height)/2 + 40, content: 'bottom left', width: 0});
        texts.push({x: parseInt(InputImagestyle.width)/2 - 30, y: parseInt(InputImagestyle.height)/2 + 40, content: 'bottom right', width: 0});
        draw()
    }

    function drawCircles() {
        for(let i = 0; i < circles.length; i++){
            ctx.save();
            ctx.beginPath();
            ctx.arc(circles[i].x, circles[i].y, circles[i].radius, 0, Math.PI * 2);
            ctx.fillStyle = color[i];
            ctx.strokeStyle = 'white'
            ctx.fill();
            ctx.stroke();
            ctx.restore();
        }
    }

    function drawPoly() {
        ctx.save();

        ctx.globalAlpha = 0.5;
        ctx.beginPath();
        ctx.moveTo(circles[0].x, circles[0].y)
        ctx.lineTo(circles[1].x, circles[1].y)
        ctx.lineTo(circles[2].x, circles[2].y)
        ctx.lineTo(circles[3].x, circles[3].y)
        ctx.closePath();
        ctx.fillStyle = 'white';
        ctx.fill();
        ctx.globalAlpha = 0.5;
        ctx.restore();
    }

    function writeText() {
        for(let i = 0; i < texts.length; i++){
            ctx.save();
            ctx.beginPath();
            ctx.font = '15px Arial';
            ctx.fillStyle = 'white';
            ctx.fillText(texts[i].content, texts[i].x, texts[i].y);
            ctx.lineWidth = 0.2;                
            ctx.strokeStyle = color[i];        
            ctx.strokeText(texts[i].content, texts[i].x, texts[i].y);
            texts[i].width = ctx.measureText(texts[i]).width
            ctx.measureText(text)
            ctx.restore();
        }
    }

    function draw() {
        drawPoly();
        drawCircles();
        writeText();
    }

    function getMousePos(canvas, evt) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: evt.clientX - rect.left,
            y: evt.clientY - rect.top
        };
    }

    function getCircleIndexUnderMouse(x, y) {
        return circles.findIndex(circle => {
            return Math.sqrt((circle.x - x) ** 2 + (circle.y - y) ** 2) < radius;
        });
    }

    canvas.addEventListener('mousedown', function(e) {
        const mousePosition = getMousePos(canvas, e);
        selectedCircleIndex = getCircleIndexUnderMouse(mousePosition.x, mousePosition.y);
         
        if (selectedCircleIndex !== -1) {
            selectedCircle = circles[selectedCircleIndex]
            selectedText =  texts[selectedCircleIndex]
            offsetX = mousePosition.x - selectedCircle.x;
            offsetY = mousePosition.y - selectedCircle.y;
        }
    });

    function redraw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(InputImage, 0, 0, canvas.width, canvas.height);
        draw();
    }

    canvas.addEventListener('mousemove', function(e) {
        if (selectedCircle) {
            const mousePosition = getMousePos(canvas, e);
            selectedCircle.x = mousePosition.x - offsetX;
            selectedCircle.y = mousePosition.y - offsetY;
            if (selectedCircleIndex == 0 || selectedCircleIndex == 1){
                selectedText.x = selectedCircle.x - selectedText.width / 4;
                selectedText.y = selectedCircle.y - 10;
            } else {
                selectedText.x = selectedCircle.x - selectedText.width / 4;
                selectedText.y = selectedCircle.y + 20;
            }

            redraw();
        }
    });

    canvas.addEventListener('mouseup', function() {
        selectedCircle = null;
        selectedText = null;
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
    const dashboard = document.getElementById('dashboard')
    const Ratio = document.getElementById('Ratio')
    const motorcycleCount = document.getElementById('Motorcycle_count')
    const carCount = document.getElementById('Car_count')
    const busCount = document.getElementById('Bus_count')
    const truckCount = document.getElementById('Truck_count')
    const greenLightTime = document.getElementById('Green_light_time')

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
        dashboard.style.display = 'block';
        InputImage.title = 'After analyse';
        InputImage.src = data.result;
        InputImage.style.display='block';
        Ratio.textContent = 'Ratio: ' + data.Ratio
        motorcycleCount.textContent = 'Motorcycle count: ' + data.Motorcycle_count
        carCount.textContent = 'Car count: ' + data.Car_count
        busCount.textContent = 'Bus count: ' + data.Bus_count
        truckCount.textContent = 'Truck count: ' + data.Truck_count
        greenLightTime.textContent = "Green Light Time: " + data.Green_light_time + 's'
        processing_dots.style.display='none';
        dots.style.display='none';
    })
    .catch(error => {
        console.error('Error:', error);
    });

    altInput.style.display='none';
    altOutput.style.display='block';
    canvas.style.display = 'none';
    buttonRoadAnalyse.style.display='none'
}
