import plotly.graph_objs as go
import pandas as pd
import json

v_2d_df = pd.read_csv(
    "v_2d.csv",
)

v_2d_df["language"] = ["English"] * 100 + ["Chinese"] * 100

# read the summary from json file
with open(
    "../CA/summary_combined_Territorial_disputes_in_the_South_China_Sea.json"
) as f:
    data = json.load(f)
summary = []
for item in data:
    summary.append(item["summary"])

v_2d_df["summary"] = summary


# Function to format summaries for hover text
def format_summary(text):
    return text.replace("\n", "<br>")


v_2d_df["formatted_summary"] = v_2d_df["summary"].apply(format_summary)

# Plot using Plotly
# Create a color mapping for languages
color_map = {
    "English": "blue",
    "Chinese": "red",
}
v_2d_df["color"] = v_2d_df["language"].map(color_map)

# Create a symbol mapping for languages
symbol_map = {
    "English": "circle",
    "Chinese": "x",
}
v_2d_df["symbol"] = v_2d_df["language"].map(symbol_map)

# Create traces for each language
traces = []
for language in v_2d_df["language"].unique():
    df = v_2d_df[v_2d_df["language"] == language]
    trace = go.Scatter(
        x=df["x"],
        y=df["y"],
        mode="markers",
        name=language,
        marker=dict(color=color_map[language], symbol=symbol_map[language], size=8),
        customdata=df[["formatted_summary"]],
        # hovertemplate="<b>%{customdata[0]}</b><extra></extra>",
        hoverinfo="none",
    )
    traces.append(trace)

# Create the layout
layout = go.Layout(
    title="t-SNE Visualization of News Articles - Territorial disputes in the South China Sea",
    xaxis=dict(title="t-SNE component 1"),
    yaxis=dict(title="t-SNE component 2"),
    showlegend=True,
)

# Create the figure
fig = go.Figure(data=traces, layout=layout)

# Customize the hover template to instruct user to hover
# fig.update_traces(
#    hovertemplate="<b>Hover over a point to see the summary</b><extra></extra>",
#    customdata=v_2d_df[["formatted_summary"]].values,
# )
# Update layout to adjust the width of the scatter plot
# fig.update_layout(width=1000)  # Set the width in pixels

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
            width: 30vw;
            max-height: 98vh;
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
            const plotDiv = document.getElementById('plot');
            const plotElement = plotDiv.querySelector('.js-plotly-plot');
            const newWidth = window.innerWidth * 2 / 3;
            Plotly.relayout(plotElement, 'width', newWidth);
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
with open("interactive_plot_200.html", "w") as f:
    f.write(html_content)
