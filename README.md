# Green-Line
Green Line Branch Performance and Revenue Efficiency (CS506 Data Science Tools and Applications Project)

Description:

MBTA Green Line has four branches (B, C, D, and E), and this project investigates the operational reliability and the financial efficiency of those branches. The Green Line offers both underground and above-ground services that serve different Boston neighborhoods and college campuses. After visiting some other countries this past year, it made me wonder why our train system seemed far behind train systems of some other countries.

The project has three components. A predictive performance model will be created to forecast if a branch will experience a delay on a given day based on weather conditions, service announcements, and time of day. Secondly, a financial analysis model will determine which branch generates the most revenue relative to its operating costs. Lastly and most interestingly, create a model to estimate how much revenue is lost from fare evasion compared to ridership count, which is very common on the above-ground stops.

Project Timeline:
Week 1 & 2: Data Collection, Exploration, Cleaning
        Need to identify and clean important predictors. May need to do a lot of cleaning so gave it some extra time. 
        
Week 3: Fare Evasion Estimation Development

Week 4 & 5: Performance Modeling (Includes the ML component so gave it extra time)

Week 6: Financial Analysis (Going through MBTA budget documents)

Week 7: Visualization (Including interactive visuals to effectively display the users my findings)

Week 8: Final Testing and Final Deliverables

Backup Plan: Only complete the Fare Evasion Estimation and Performance Model.

Goals:

Goal 1: Performance Model
Predict which branch will experience the worst delays on a given day, using weather conditions, day of the week, time, if there is a special event and recent service disruption history as predictors. An ML model that produces accurate results is the final deliverable.

Goal 2: Revenue Efficiency
To identify which branch generates the most value relative to their operating costs by calculating and comparing revenue per mile for each Green Line Branch. A final deliverable will be each branch ranked by financial efficiency.

Goal 3: Fare Evasion Estimation Model
To accurately estimate lost fares across different station characteristics by comparing card taps to the actual ridership count. A final deliverable will be estimated lost fares per branch per day.

Data Collection Plan:
Data on the green lines' reliability (is the branch down? Is the train delayed? ridership data) and financial data on the green line branches need to be collected to 

For performance data and the fare evasion estimation model, I will be using the following:
MBTA V3 API
Weather API
Ticketmaster API (for special event days of increased demand)

For financial data, I will be using the following:
MBTA Operating Costs Per Line
MBTA Rideship Reports
Fare Revenue By Line

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
