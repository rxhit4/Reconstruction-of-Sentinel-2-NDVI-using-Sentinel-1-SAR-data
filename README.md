
# Reconstruction of Sentinel-2 NDVI using Sentinel-1 (SAR) Data

This repository contains the code and configuration for reconstructing cloud-contaminated NDVI from Sentinel-2 satellite's optical imagery by integrating Sentinel-1 satellite's Synthetic Aperture Radar (SAR) data. The entire implementation is conducted within the Google Earth Engine (GEE) platform, allowing scalable and efficient restoration of vegetation indices, particularly in monsoon-affected regions.

---

## Study Area: Nashik District, Maharashtra

Nashik is a key agricultural zone in India known for grapes, sugarcane, onions, and soybeans. The area experiences heavy monsoon rains that hinder optical satellite observations. Its diverse cropping systems and cloud-prone climate make it ideal for evaluating SAR-optical NDVI fusion strategies.

### Grid-Based Scalability
- Nashik divided into **1150 grids of 4×4 km**
- Each grid processed independently in GEE for parallelism

![Fig 1: Grid wise whole district (1150 grids of 4x4km)](images/fig1_districtboundary.png)  
*Fig 1: Grid wise whole district (1150 grids of 4x4km)*

![Fig 2: Grid wise whole district (1150 grids of 4x4km)](images/fig2_gridwise.png)  
*Fig 2: Grid wise whole district (1150 grids of 4x4km)*

---

## Satellite Datasets Used

### Sentinel-1 (SAR)
- Mode: Interferometric Wide (IW) Swath
- Resolution: 10 m (VV and VH polarizations)
- Revisit Frequency: 6 days
- Source: Google Earth Engine (GRD format, converted to dB scale)

### Sentinel-2 (Optical)
- Resolution: 10 m (Bands 4 and 8 for NDVI)
- NDVI = (NIR - Red) / (NIR + Red)
- Cloud Mask: Scene Classification Map (SCL) from Sen2Cor algorithm

---

## Spatio-Temporal Feature Partitioning

SAR predictors are decomposed into:
- Global temporal mean
- Local temporal mean (neighborhood)
- Global spatial residuals
- Local spatial residuals

This partitioning enables the **Multiple Linear Regression (MLR)** model to capture both large-scale and fine-scale NDVI variation. Each pixel is modeled independently, using its localized SAR-derived features.

---

## Methodology for NDVI Restoration

![Fig 3: NDVI Reconstruction Workflow](images/fig_workflow.png)  
*Fig 3: Process workflow for SAR-optical NDVI reconstruction*

### Workflow Phases:
1. **Data Preparation**  
   - NDVI calculated using Bands 4 & 8 of Sentinel-2  
   - Cloud masking using SCL  
   - Sentinel-1 SAR converted to dB  

2. **Spatio-Temporal Feature Generation**  
   - Local and global SAR mean extraction  
   - Median filtering to suppress speckle  

3. **Data Synchronization**  
   - Sentinel-1 and Sentinel-2 aligned spatially and temporally (±12 days)

4. **Model Training & NDVI Prediction**  
   - Pixel-wise linear regression using SAR predictors

5. **Post-Processing**  
   - PCA smoothing  
   - Calibration to match observed NDVI range  
   - Gap filling in NDVI time series  

---

## Results & Discussion

- The approach successfully reconstructs NDVI under frequent cloud contamination
- Vegetation cycles (growth, senescence) are preserved

![Fig 4: NDVI Image Examples](images/fig3_reconstruction.png)  
*Fig 4: Reconstructed NDVI Image for the time period July 1–15, 2023*

- Reconstructed NDVI shows strong alignment with actual vegetation trends
- Enhanced spatial clarity in agricultural zones and stress detection

![Fig 5: NDVI Point Profiles](images/fig4_profiles.png)  
*Fig 5: NDVI Profiles of 4 different points before and after reconstruction*

---

## Model Validation

### Data Split:
- **Training**: 70% clear-sky data  
- **Testing**: 20% unseen NDVI  
- **Validation**: 10% synthetic cloud mask

### Evaluation Metrics:
| Metric     | Training | Testing | Validation |
|------------|----------|---------|------------|
| MAE        | 0.061    | 0.074   | 0.065      |
| CC         | 0.78     | 0.80    | 0.82      |

The results show strong temporal consistency and spatial fidelity in vegetation behavior, confirming the effectiveness of SAR-optical regression fusion.

---

## Conclusion

This NDVI reconstruction framework provides a scalable and practical solution for gap-filling in vegetation monitoring. By leveraging SAR data and spatio-temporal modeling, it overcomes limitations of cloud-obstructed optical datasets, especially in monsoon climates.

The approach generalizes well, is easily scalable to large regions, and can support precision agriculture, environmental monitoring, and climate-resilient planning.

---

## Installation

### 1️. Create a Google Earth Engine account
Sign up at [Google Earth Engine](https://earthengine.google.com/) and verify access.

### 2️. Set up Python environment (PyCharm recommended)
Create a new Python project in PyCharm or any IDE of your choice.

### 3️. Install required libraries and dependencies
Open terminal and run:
```bash
pip install earthengine-api geopandas pandas shapely json
```

### 4️. Authenticate Earth Engine
In Python, run:
```python
import ee
ee.Authenticate()
ee.Initialize()


## Usage

1. Update the configuration file (`Parameters.json`) with your **Area of Interest (AOI)**, **date range**, and **project title**.  

2. Then execute the following from your project directory:
```bash
cd scripts
python sar_optical_ndvi_reconstruction.py
```

The outputs will be saved to your Google Drive under the folder name specified by `PROJECT_TITLE` in your configuration file.


## Author & Acknowledgements

**Author**: Rohit Kumar Sarkar  
**Institute**: Techno India University, Kolkata  
**Guide**: Dr. Niraj Priyadarshi, Sci/Engr-SF, RRSC-East, NRSC, Indian Space Research Organisation (ISRO)  

> This work would not have been possible without the insightful guidance, support, and encouragement of Dr. Niraj Priyadarshi.
