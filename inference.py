from ultralytics import YOLO

model = YOLO(r'C:\Users\phuon\Documents\FPT\CN7\DAT301m\Vehicle Detection\Code\best.pt')

results = model(r"C:\Users\phuon\Documents\FPT\CN7\DAT301m\Vehicle Detection\Dataset\train\images\000000041_jpg.rf.36a1115b706e64545938d68c3a20b42f.jpg")

print(len(results))