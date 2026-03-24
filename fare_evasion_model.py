import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from dotenv import load_dotenv
import time
 
load_dotenv()
API_KEY = os.getenv("MBTA_API_KEY")
 
BASE_URL = "https://api-v3.mbta.com"
HEADERS = {"x-api-key": API_KEY}
 
# MBTA Open Data - Monthly Ridership by Mode and Line (updated as of April 7, 2025)
RIDERSHIP_URL = "https://services1.arcgis.com/ceiitspzDAHrdGO1/arcgis/rest/services/Fall_2024_MBTA_Rail_Ridership_by_SDP_Time_Period_Route_Line_and_Stop/FeatureServer/0/query"
 
GREEN_LINE_BRANCHES = {
    "Green-B": "B Branch",
    "Green-C": "C Branch",
    "Green-D": "D Branch",
    "Green-E": "E Branch",
}

#Manual mapping of MBTA stop_id to branch for fare tap data, 
#since the API doesn't directly provide branch info at the stop level
STOP_TO_BRANCH = {
    "B Branch": [
        "Blandford Street",
        "Boston University East",
        "Boston University Central",
        "Amory Street",
        "Babcock Street",
        "Packard's Corner",
        "Harvard Avenue",
        "Griggs Street",
        "Allston Street",
        "Warren Street",
        "Washington Street",
        "Sutherland Road",
        "Chiswick Road",
        "Chestnut Hill Avenue",
        "South Street",
        "Boston College",
    ],
    "C Branch": [
        "Saint Mary's Street",
        "Hawes Street",
        "Kent Street",
        "Saint Paul Street",
        "Coolidge Corner",
        "Summit Avenue",
        "Brandon Hall",
        "Fairbanks Street",
        "Washington Square",
        "Tappan Street",
        "Dean Road",
        "Englewood Avenue",
        "Cleveland Circle",
    ],
    "D Branch": [
        "Fenway",
        "Longwood",
        "Brookline Village",
        "Brookline Hills",
        "Beaconsfield",
        "Reservoir",
        "Chestnut Hill",
        "Newton Centre",
        "Newton Highlands",
        "Eliot",
        "Waban",
        "Woodland",
        "Riverside",
    ],
    "E Branch": [
        "Prudential",
        "Symphony",
        "Northeastern University",
        "Museum of Fine Arts",
        "Longwood Medical Area",
        "Brigham Circle",
        "Fenwood Road",
        "Mission Park",
        "Riverway",
        "Back of the Hill",
        "Heath Street",
    ],
}

#Shared stops 
#(excluded from current estimates but included in code for potential future analysis)
SHARED_STOPS = [
    "Kenmore",
    "Hynes Convention Center",
    "Copley",
    "Arlington",
    "Boylston",
    "Park Street",
    "Government Center",
    "Haymarket",
    "North Station",
    "Science Park/West End",
    "Lechmere",
    "East Somerville",
    "Gilman Square",
    "Magoun Square",
    "Ball Square",
    "Medford/Tufts",
    "Union Square",
]

#Only two underground stops (excluding the shared stops) 
#on the Green Line, both on the E Branch
UNDERGROUND_STOPS = {"Prudential", "Symphony"}


# Evasion rates
    #Based on a recent news report from the MBTA that estimated fare evasion rates of 56.5% 
    #for above-ground lines due to the contactless payment system as of Sept. 2024 and 1-2% for underground lines, 
    #we can apply a blended evasion rate to each branch based on its proportion of above-ground stops. 
    #This is a simplified approach but provides a starting point for estimation.
    #https://www.nbcboston.com/investigations/after-mbta-implements-new-payment-system-rampant-fare-evasion-on-green-line/3707620/
EVASION_RATE_ABOVE_GROUND = 0.565
EVASION_RATE_UNDERGROUND  = 0.01

 
FARE = 2.40  # Current Green Line fare (as of 03/2026)

#Needed to normalize time periods for better visualization and analysis
#These are ESTIMATES because I could not find actual windows for each time period in the MBTA documentation, 
#but they are based on typical transit definitions and patterns.
#BIG WEAKNESS
TIME_PERIOD_HOURS = {
    "VERY_EARLY_MORNING": 1.5,  # ~4:30 AM – 6:00 AM
    "EARLY_AM":           1.5,  # ~6:00 AM – 7:30 AM
    "AM_PEAK":            2.0,  # ~7:30 AM – 9:30 AM
    "MIDDAY_BASE":        2.5,  # ~9:30 AM – 12:00 PM
    "MIDDAY_SCHOOL":      3.0,  # ~12:00 PM – 3:00 PM
    "PM_PEAK":            3.0,  # ~3:00 PM – 6:00 PM
    "EVENING":            2.5,  # ~6:00 PM – 8:30 PM
    "LATE_EVENING":       2.5,  # ~8:30 PM – 11:00 PM
    "NIGHT":              1.5,  # ~11:00 PM – 12:30 AM
    "OFF_PEAK":           6.0,  # catch-all for remaining hours
}
 
# ─────────────────────────────────────────────
# 1. FETCH RIDERSHIP DATA
# ─────────────────────────────────────────────
 
#Fetching the 
def fetch_ridership():
    print("Fetching MBTA ridership data by stop and branch...")
    
    all_rows = []
    offset = 0
    batch_size = 500

    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "outSR": 4326,
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": batch_size
        }
        r = requests.get(RIDERSHIP_URL, params=params)
        r.raise_for_status()

        data = r.json()
        features = data.get("features", [])
        if not features:
            break

        rows = [f["attributes"] for f in features]
        all_rows.extend(rows)

        if len(features) < batch_size:
            break

        offset += batch_size

    df = pd.DataFrame(all_rows)
   
    # Filter for Green Line branches only
    green = df[df["route_id"].str.startswith("Green", na=False)].copy()
    print(f"  → {len(green)} Green Line records")

    return green
  
# ─────────────────────────────────────────────
# 3. FETCH FARE TAP DATA FROM MBTA API
# ─────────────────────────────────────────────
 
def fetch_stop_metadata():
    print("Fetching fare tap data from MBTA V3 API...")
    rows = []
 
    for route_id, branch_name in GREEN_LINE_BRANCHES.items():
        url = f"{BASE_URL}/stops"
        params = {
            "filter[route]": route_id,
            "include": "facilities",
        }
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        stops = r.json().get("data", [])
 
        for stop in stops:
            attr = stop.get("attributes", {})
            rows.append({
                "branch": branch_name,
                "stop_name": attr.get("name"),
                "latitude": attr.get("latitude"),
                "longitude": attr.get("longitude")
            })
 
        print(f"  → {len(stops)} stops for {branch_name}")
 
    branchDF = pd.DataFrame(rows)
    
    return branchDF

#Helper function to assign evasion rates based on whether 
#the stop is underground or above ground
def get_evasion_rate(stop_name):
        if stop_name in UNDERGROUND_STOPS:
            return EVASION_RATE_UNDERGROUND
        return EVASION_RATE_ABOVE_GROUND

#Estimation function that applies evasion rates to ridership data to estimate evaders and revenue lost, 
def estimate_evasion(df_ridership, df_stops):
    print("Estimating fare evasion...")

    if "route_id" not in df_ridership.columns or "total_ons" not in df_ridership.columns:
        print("Could not find expected ridership columns. Printing available columns:")
        print(df_ridership.columns.tolist())
        return pd.DataFrame()

    # Map stop names to branches
    stop_branch_map = {stop: branch for branch, stops in STOP_TO_BRANCH.items() for stop in stops}
    df_ridership["branch_name"] = df_ridership["stop_name"].map(stop_branch_map)
    df_ridership = df_ridership.dropna(subset=["branch_name"])

    # Aggregate total boardings per branch per stop per day type
    monthly = (
        df_ridership
        .groupby(["branch_name", "stop_name", "day_type_name", "time_period_name"])["average_ons"]
        .sum()
        .reset_index()
    )
    monthly.rename(columns={"average_ons": "ridership_count"}, inplace=True)

    # Merge stop counts (only once)
    stop_counts = df_stops.groupby("branch").size().reset_index(name="stop_count")
    stop_counts.rename(columns={"branch": "branch_name"}, inplace=True)
    monthly = monthly.merge(stop_counts, on="branch_name", how="left")

    monthly["evasion_rate"] = monthly["stop_name"].apply(get_evasion_rate)
    monthly["estimated_evaders"] = (monthly["ridership_count"] * monthly["evasion_rate"]).astype(int)
    monthly["revenue_lost"] = monthly["estimated_evaders"] * FARE

    return monthly

#Visualization functions

#Bar chart: how many real-time predictions exist per branch (proxy for activity).
def plot_revenue_lost_per_stop(df):
    stop_revenue = (
        df.groupby(["stop_name", "branch_name"])["revenue_lost"]
        .sum()
        .reset_index()
        .sort_values("revenue_lost", ascending=False)
    )

    colors = {
        "B Branch": "#C8102E",
        "C Branch": "#003DA5",
        "D Branch": "#00843D",
        "E Branch": "#DA291C"
    }

    bar_colors = stop_revenue["branch_name"].map(colors)

    fig, ax = plt.subplots(figsize=(18, 6))
    bars = ax.bar(stop_revenue["stop_name"], stop_revenue["revenue_lost"], color=bar_colors)
    ax.set_title("Estimated Revenue Lost per Stop", fontsize=14, fontweight="bold")
    ax.set_xlabel("Stop")
    ax.set_ylabel("Revenue Lost ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.xticks(rotation=90, fontsize=7)

    # Add legend manually
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=b) for b, c in colors.items()]
    ax.legend(handles=legend_elements)

    plt.tight_layout()
    plt.savefig("plot_revenue_lost_per_stop.png", dpi=150)
    plt.show()
    print("Saved: plot_revenue_lost_per_stop.png")

#Bar chart: total estimated monthly revenue lost per branch
def plot_revenue_lost_per_branch(df):
    revenue = df.groupby("branch_name")["revenue_lost"].sum().sort_values(ascending=False)
 
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(revenue.index, revenue.values, color=["#C8102E", "#003DA5", "#00843D", "#DA291C"])
    ax.set_title("Estimated Total Revenue Lost to Fare Evasion per Branch", fontsize=14, fontweight="bold")
    ax.set_xlabel("Branch")
    ax.set_ylabel("Revenue Lost ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.bar_label(bars, fmt="$%.0f", padding=3)
    plt.tight_layout()
    plt.savefig("plot_revenue_lost.png", dpi=150)
    plt.show()
    print("Saved: plot_revenue_lost.png")
 
#Bar chart: estimated revenue lost by time period (normalizes for different time period lengths).
def plot_revenue_lost_by_time_period(df):
    summary = df.groupby("time_period_name")["revenue_lost"].sum().reset_index()
    summary["hours"] = summary["time_period_name"].map(TIME_PERIOD_HOURS)
    summary["revenue_per_hour"] = summary["revenue_lost"] / summary["hours"]
    summary = summary.sort_values("revenue_per_hour", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(summary["time_period_name"], summary["revenue_per_hour"], color="#003DA5")
    ax.set_title("Estimated Revenue Lost per Hour by Time Period", fontsize=14, fontweight="bold")
    ax.set_xlabel("Time Period")
    ax.set_ylabel("Revenue Lost per Hour ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.bar_label(bars, fmt="$%.0f", padding=3)
    plt.tight_layout()
    plt.savefig("plot_revenue_lost_by_time_period.png", dpi=150)
    plt.show()
    print("Saved: plot_revenue_lost_by_time_period.png")
 
if __name__ == "__main__":
    start = time.time()

    # Fetch all data sources
    df_ridership = fetch_ridership()
    df_stops = fetch_stop_metadata()
 
    # Print raw snapshots of the data for verification
    print("RIDERSHIP SAMPLE")
    print(df_ridership.head(5).to_string(index=False))
 
    print("STOPS SAMPLE")
    print(df_stops.head(5).to_string(index=False))
 
    # Estimate evasionprint
    df_evasion = estimate_evasion(df_ridership, df_stops)
    
    #Print evasion estimates snapshot and columns for verification before plotting
    #If the dataframe is not empty
    if not df_evasion.empty:
        print("EVASION ESTIMATES")
        print(df_evasion.head(10).to_string(index=False))
        print(f"{len(df_evasion)} total rows")
 
        # Save to CSV for potential further analysis
        df_evasion.to_csv("fare_evasion_estimates.csv", index=False)
        print("Saved: fare_evasion_estimates.csv")
 
        print(df_evasion.columns.tolist())
        print(df_evasion.head(3))
        
        # Plots (add more if needed)
        print("Generating plots")
        plot_revenue_lost_per_branch(df_evasion)
        plot_revenue_lost_by_time_period(df_evasion)
        plot_revenue_lost_per_stop(df_evasion)
    else:
        print("Evasion estimates could not be computed")
 
    print("Plots successfully generated")
    
    time_ran = time.time() - start
    print(f"Total execution time: {time_ran:.2f} seconds")