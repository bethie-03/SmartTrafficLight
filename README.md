# WEATHER ANALYSIS DASHBOARD

Follow các step dưới đây để chạy được dashboard nhé!

1. Clone nhánh này về:
```bash
git clone --branch analysis --single-branch https://github.com/bethie-03/SmartTrafficLight.git
```
2. Install các thư viện:
```bash
pip install requirements.txt
```
3. Tải dữ liệu thời tiết đã được phân loại từ google drive:
```bash
gdown 1ridi0bFXWw5zVvRgD1WFwkHunbxn5XQH
```
1. Unzip và thay các đường dẫn vào các biến dưới đây trong Dashboard.py:
```bash
folder_night = "...\Weather\Night"
folder_daylight = "...\Weather\Daylight"
folder_cameras = "...\Weather\Cameras"
```
4. Chạy Dashboard.py
```bash
python Dashboard.py
```