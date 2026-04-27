# Green-Line
## Green Line Branch Performance and Fare Evasion Estimation (CS506 Data Science Tools and Applications Project)

Description:

MBTA Green Line has four branches (B, C, D, and E), and this project investigates the operational reliability and the financial efficiency of those branches. The Green Line offers both underground and above-ground services that serve different Boston neighborhoods and college campuses. After visiting some other countries this past year, it made me wonder why our train system seemed far behind train systems of some other countries. This project attempts to identify the issues and inefficiencies that the MBTA faces and potentially lead to change for a better system.

The project has three components. A predictive performance model will be created to forecast if a branch will experience a delay on a given day based on weather conditions, service announcements, and time of day. Secondly, a financial analysis model will determine which branch generates the most revenue relative to its operating costs. Lastly and most interestingly, create a model to estimate how much revenue is lost from fare evasion compared to ridership count, which is very common on the above-ground stops.

### How to build and run the code:

1) Clone repo and enter it

```bash
git clone git@github.com:joesteriti/Green-Line.git
cd "Final Project"
```

2) Create and activate a virtual environment

```bash
make setup
source .venv/bin/activate
make install
```

3) Set API key

- Copy `.env.example` to `.env`.
- Put your MBTA API key in `.env` as:

```bash
MBTA_API_KEY=your_real_key_here
```

You can request a key here: https://api-v3.mbta.com/

4) Download and place headway data

Download and unzip CSV files from:
- MBTA Rapid Transit Headways 2024: https://mbta-massdot.opendata.arcgis.com/datasets/ccb2941254944803bbd4e2df58e09906/about
- MBTA Rapid Transit Headways 2025: https://mbta-massdot.opendata.arcgis.com/datasets/84c9d171d32945f594fbb4d889153c44/about
- MBTA Rapid Transit Headways 2026: https://mbta-massdot.opendata.arcgis.com/datasets/fffd5e8ff7f042deb7834f3badf49e58/about

Expected folder layout:

```text
data/
  Headways_2024/
    2024-01_Headway.csv
    ...
    2024-12_Headway.csv
  Headways_2025/
    2025-01_Headway.csv
    ...
    2025-12_Headway.csv
  Headways_2026/
    2026-01_Headway.csv
    2026-02_Headway.csv
    2026-03_Headway.csv
```

5) Validate setup and run notebooks

```bash
make check
make notebook
```

Then run:
- `performance_model/performance_model.ipynb`
- `fare_evasion.ipynb`

### Tests:

- In `performance_model/performance_model.ipynb`, run all cells and confirm the tests section at the bottom passes.
- In `fare_evasion.ipynb`, run all cells and confirm the final tables/plots are generated.

### Visualizations:
Average Headway Per Day:

Headway Per Season:

Important: Which branch is worst most often:

Correlation Matrix

### Description of data processing and model:

### Results:

My original goal was to predict the worst branch when it came to headway. As my project went on, I realized that I should just predict the headway for each branch, and then make classifications after if needed. It is more helpful to consumers and policy makers to know the actual values rather than the worst branch. The goal was to make this useful in trying to determine whether to take one branch or aother for consumers and trying to decide which branch to improve for policy makers/MBTA coordinators.

An example for why solely classifcation would be bad. Even in the case that some branch is worse than another, if the branch is 2 seconds worse but doesn't actually give the quantifiable results, it could be misleading which is why goals changed to predicting 

With that said, I still included a prediction of the worst branch which is around 40% accurate and the top 2 worst branches predicted is about 70% accurate. The more useful data is the continuous headway error (MAE) showing that the overall MAE is 38.3 seconds. 

Average Headway Distribution:

![Headway Gap on Incorrect Predictions](visualizations/HeadwayGapOnIncorrectPredictions.png)

The median is 29.2 seconds. From a customer stand point, a less than 30 second error is acceptable when it comes to my daily commute. It is an error I am willing to incur for this model. If we look at the per branch breakdown for MAE of headway, we see that most 3 out of 4 branches hover around 40 second error compared to the actual headway recorded. Anything less than a minute would be acceptable in my standards and even in the 90th percentile, it is still less than a minute error.


![Predicted vs Actual Headway Per Branch](visualizations/PredictedVSAvgHeadwayByBranch.png)

Using this graph, the regression is pretty accurate given the data. Branch E suffers from a decent amount of outliers but the other branches fit very well according to this graphic.

-------------------------
## From the Proposal:

Project Timeline:

Week 1 & 2: Data Collection, Exploration, Cleaning
        Need to identify and clean important predictors. May need to do a lot of cleaning, so gave it some extra time. 
        
Week 3: Fare Evasion Estimation Development

Week 4 & 5: Performance Modeling (Includes the ML component, so gave it extra time)

Week 6: Financial Analysis (Going through MBTA budget documents) 

Week 7: Visualization (Including interactive visuals to effectively display the users' findings)

Week 8: Final Testing and Final Deliverables

Backup Plan: Only complete the Fare Evasion Estimation and Performance Model.


Goals:

Goal 1: Performance Model
Predict which branch will experience the worst delays on a given day, using weather conditions, day of the week, time, if there is a special event, and recent service disruption history as predictors. An ML model that produces accurate results is the final deliverable.

Goal 2: Revenue Efficiency
To identify which branch generates the most value relative to their operating costs by calculating and comparing revenue per mile for each Green Line Branch. A final deliverable will be each branch ranked by financial efficiency.

Goal 3: Fare Evasion Estimation Model
To accurately estimate lost fares across different station characteristics by comparing card taps to the actual ridership count. A final deliverable will be estimated lost fares per branch per day.


Data Collection Plan:

Data on the green lines' reliability (is the branch down? Is the train delayed? ridership data) and financial data on the green line branches need to be collected.
For performance data and the fare evasion estimation model, I will be using the following:
MBTA V3 API (https://www.mbta.com/developers/v3-api)
MassGIS Data (This one makes distinctions between above-ground and below-ground stops)(https://www.mass.gov/info-details/massgis-data-mbta-rapid-transit)
GTFS (https://github.com/google/transit/tree/master/gtfs/spec/en)
Weather API (https://openweathermap.org/api)

For financial data, I will be using the following:
2022 - 2024 NTD Annual Data - Operating Expenses (by Function) (https://data.transportation.gov/Public-Transit/2022-2024-NTD-Annual-Data-Operating-Expenses-by-Fu/dkxx-zjd6/about_data)
MBTA Rideship Reports (https://mbta-massdot.opendata.arcgis.com/datasets/MassDOT::mbta-monthly-ridership-by-mode-and-line/about)


Modeling Plan:

Performance Model: A random forest regression 
Revenue Efficiency: Mathematical calculation (Not ML)
Fare Evasion Estimation Model: Mathematical calculation and statistics (Not ML)


Visualization Plan:

Performance Model: Time series graph showing expected delays vs actual delays for each branch
Revenue Efficiency: Radar charts displaying different performance metrics and a scatter plot (Revenue vs cost)
Fare Evasion Estimation Model: Bar chart displaying the evasion rate per branch, or a heatmap showing the location of each station and the magnitude of fare loss for each station


Test Plan:

Performance Model: Withhold 30% of the data and train on the rest.

Revenue Efficiency: Statistical significance testing between branches.

Fare Evasion Estimation Model: Statistical significance testing between branches.
