import plotly.graph_objs as go
import pandas as pd
import json

v_2d_df = pd.read_csv(
    "FMCD/v_2d.csv",
)

v_2d_df["language"] = ["English"] * 100 + ["Chinese"] * 100

# read the summary from json file
with open("CA/summary_combined_Territorial_disputes_in_the_South_China_Sea.json") as f:
    data = json.load(f)
summary = []
for item in data:
    summary.append(item["summary"])

v_2d_df["summary"] = summary


# Function to format summaries for hover text
def format_summary(text):
    return text.replace("\n", "<br>")


v_2d_df["formatted_summary"] = v_2d_df["summary"].apply(format_summary)

t_list = [
    0,
    5,
    6,
    8,
    9,
    10,
    11,
    12,
    14,
    15,
    17,
    18,
    20,
    22,
    23,
    24,
    25,
    27,
    28,
    30,
    33,
    34,
    35,
    36,
    38,
    39,
    41,
    42,
    43,
    44,
    46,
    48,
    58,
    71,
    86,
    88,
    92,
    99,
    101,
    102,
    103,
    107,
    108,
    129,
    132,
    133,
    163,
    165,
    173,
    175,
    177,
    178,
]
# set cluster true if the index is in t_list
v_2d_df["topic"] = "Other Topics"
v_2d_df.loc[t_list, "topic"] = "Same Topic"
# Plot using Plotly
# Create a color mapping for topics
color_map = {
    "Same Topic": "blue",
    "Other Topics": "red",
}
v_2d_df["color"] = v_2d_df["topic"].map(color_map)

# Create a symbol mapping for languages
symbol_map = {
    "English": "circle",
    "Chinese": "x",
}
v_2d_df["symbol"] = v_2d_df["language"].map(symbol_map)

# Create traces for each language
traces = []
for topic in v_2d_df["topic"].unique():
    df = v_2d_df[v_2d_df["topic"] == topic]
    for language in df["language"].unique():
        df_language = df[df["language"] == language]
        trace = go.Scatter(
            x=df_language["x"],
            y=df_language["y"],
            mode="markers",
            name=f"{topic} ({language})",
            marker=dict(color=color_map[topic], symbol=symbol_map[language], size=8),
            customdata=df_language[["formatted_summary"]],
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
with open("n_interactive_plot_200.html", "w") as f:
    f.write(html_content)
