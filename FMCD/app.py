import plotly.express as px
import pandas as pd
from sklearn.decomposition import PCA
import json

v_2d_df = pd.read_csv(
    "v_2d.csv",
)
v_2d_df["language"] = ["English"] * 100 + ["Chinese"] * 100

# Read the summary from JSON file
with open(
    "../CA/summary_combined_Territorial_disputes_in_the_South_China_Sea.json"
) as f:
    data = json.load(f)
summary = [item["summary"] for item in data]
v_2d_df["summary"] = summary


# Function to format summaries for hover text
def format_summary(text):
    return text.replace("\n", "<br>")


v_2d_df["formatted_summary"] = v_2d_df["summary"].apply(format_summary)

# Plot using Plotly
fig = px.scatter(
    v_2d_df,
    x="x",
    y="y",
    color="language",
    title="t-SNE Visualization of News Articles - Territorial disputes in the South China Sea",
    labels={"x": "t-SNE component 1", "y": "t-SNE component 2"},
    hover_data={"summary": False, "language": False, "x": False, "y": False},
    symbol="language",
)

# Customize the hover template to instruct user to hover
fig.update_traces(
    hovertemplate="<b>Hover over a point to see the summary</b><extra></extra>",
    customdata=v_2d_df[["formatted_summary"]].values,
)
# Update layout to adjust the width of the scatter plot
fig.update_layout(width=1000)  # Set the width in pixels

# Save the plot as an HTML file with embedded JavaScript and CSS
html_content = f"""
<html>
<head>
    <title>Interactive Plot</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        #summary-box {{
            position: absolute;
            top: 10px;
            right: 10px;
            width: 400px;
            max-height: 600px;
            overflow-y: auto;
            background-color: white;
            border: 1px solid black;
            padding: 10px;
            z-index: 1000;
            white-space: pre-line;
        }}
    </style>
</head>
<body>
    <div id="plot">{fig.to_html(full_html=False, include_plotlyjs='cdn')}</div>
    <div id="summary-box">Hover over a point to see the summary here.</div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const plotElement = document.querySelector('.plotly-graph-div');
            plotElement.on('plotly_hover', function(data) {{
                if(data.points.length > 0) {{
                    const summary = data.points[0].customdata[0];
                    document.getElementById('summary-box').innerHTML = summary;
                }}
            }});
            plotElement.on('plotly_unhover', function(data) {{
                document.getElementById('summary-box').innerHTML = 'Hover over a point to see the summary here.';
            }});
        }});
    </script>
</body>
</html>
"""

# Save the HTML content to a file
with open("interactive_plot.html", "w") as f:
    f.write(html_content)
