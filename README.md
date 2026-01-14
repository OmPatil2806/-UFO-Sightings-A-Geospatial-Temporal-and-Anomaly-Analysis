# 🛸 Exploratory Analysis of Global UFO Sightings

##  Project Overview
This project presents an end-to-end Exploratory Data Analysis (EDA) of a global UFO sightings dataset. The goal is to uncover meaningful patterns related to time, geography, reported UFO shapes, seasonal behavior, and anomalous sighting durations using structured data analysis and visualization techniques.

---

##  Objectives
- Analyze long-term trends in UFO sightings over time  
- Identify geographic hotspots at country and state levels  
- Examine commonly reported UFO shapes  
- Explore seasonal and monthly sighting patterns  
- Detect anomalous sightings with unusually long durations  
- Demonstrate a complete and structured EDA pipeline  

---

##  Dataset
- **Source:** Kaggle (UFO Sightings Dataset)  
- **Records:** 88,000+ reported sightings  
- **Key Features:**
  - `datetime` – Date and time of sighting  
  - `city`, `state`, `country` – Location details  
  - `shape` – Reported UFO shape  
  - `duration (seconds)` – Duration of sighting  
  - `latitude`, `longitude` – Geospatial coordinates  
  - `comments` – Witness descriptions  

---

##  Data Cleaning & Preparation
The dataset was prepared using the following steps:
- Converted datetime fields into proper datetime format  
- Handled missing values in categorical columns  
- Removed invalid and extreme duration outliers  
- Grouped rare UFO shapes into an “Other” category  
- Engineered new features such as `year`, `month`, and `decade`  
- Created a cleaned dataset for reliable analysis  

---

##  Exploratory Data Analysis
The analysis focuses on answering key business and analytical questions:
- How have UFO sightings changed over time?  
- Which decades recorded the highest number of sightings?  
- Which countries and US states report the most sightings?  
- What UFO shapes are most frequently observed?  
- Are sightings influenced by seasonal or monthly patterns?  
- Are there anomalous sightings with unusually long durations?  

A variety of visualizations including line charts, horizontal bar charts, box plots, and scatter plots were used to support insights.

---

##  Key Insights
- UFO sighting reports have increased significantly since the 1990s  
- The United States accounts for the majority of reported sightings  
- Sightings are concentrated in a few populous US states  
- A small number of shapes dominate reported observations  
- Sightings are more frequent during warmer months  
- A limited number of duration-based anomalies were identified  

---

## 🛠️ Tools & Technologies
- **Python**  
- **Pandas**  
- **Matplotlib**  
- **Jupyter Notebook**

---

##  Conclusion
This project demonstrates how a structured exploratory data analysis approach can transform raw observational data into meaningful insights. While the dataset does not provide evidence of extraterrestrial activity, it reveals strong patterns in human reporting behavior, geographic concentration, seasonal influence, and data anomalies. The project highlights the importance of data cleaning, feature engineering, and visualization in understanding real-world datasets.

---

## 👤 Author
**Om Patil**  
Aspiring Data Analyst | Python | Data Analysis | EDA  
🔗 LinkedIn: https://www.linkedin.com/in/om-patil-039863369/
