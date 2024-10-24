# labchart_econ
---
This package is used for synchronizing time of video frames recorded with an e-con camera and of electrical recordings generated by LabChart.

---
## How to use

### 1. Install via pip
```
pip install git+https://github.com/mfukurow/labchart_econ.git
```

### 2. Import labchart_econ
Open powershell or terminal
```
ipython
import labchart_econ
```

### 3. Read timestamp from an e-con video
```
vfilepath = hoge/hoge/hoge.mp4
t_frame = labchart_econ.read_timestamp(vfilepath)
```

### 4. Get triggered frame
```
t_trigframe, is_trigframe = labchart_econ.get_t_trigframe(t_frame)

# you will be asked to determine "interval range" to detect the trigerred frames after displaying an inter-frame interval plot
```

### 5. Synchronize triggered frame time with trigger pulse time
```
t_pulse, t_frame, is_trigframe = labchart_econ.sync_labchart_econ()
```