import plotly.graph_objs as go
import pandas as pd
import json
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd

pd.set_option("mode.copy_on_write", True)


def extract_summary(file):
    with open(file) as f:
        data = json.load(f)
    # Initialize a list to store the extracted values
    summary = []
    for item in data:
        if "body_eng" in item:
            s = item["body_eng"]
            summary.append(s)
    return summary


latent_vectors = pd.read_csv(
    "Narrative_DIff/narrative_latent_vectors_3.csv", header=None
)
# print(latent_vectors.shape)

tsne = TSNE(n_components=2, random_state=42)

v_2d = tsne.fit_transform(latent_vectors)
v_2d_df = pd.DataFrame(v_2d, columns=["x", "y"])

v_2d_df["language"] = ["English"] * 26 + ["Chinese"] * 28

# read the summary from json file
summary = []
file_list = [
    "eng_narrative_QnA_summary_Russo_Ukrainian_War_eng.json",
    "eng_narrative_QnA_summary_Russo_Ukrainian_War_zho.json",
]
for file in file_list:
    s = extract_summary("Narrative_DIff/" + file)
    summary = summary + s

"""
# read the label file
labels_T = pd.read_csv("CA/labels_4o.csv", header=None, names=["label"])
labels_T = labels_T.astype(int)
# get the label index if labe is 1
label_index = list(labels_T[labels_T["label"] == 1].index)

summary = [summary[i] for i in label_index]
"""
v_2d_df["summary"] = summary


# Function to format summaries for hover text
def format_summary(text):
    return text.replace("\n", "<br>")


v_2d_df["formatted_summary"] = v_2d_df["summary"].apply(format_summary)

# Plot using Plotly
# Create a color mapping for languages
color_map = {"English": "blue", "Chinese": "red"}
v_2d_df["color"] = v_2d_df["language"].map(color_map)

# Create a symbol mapping for languages
symbol_map = {"English": "blue", "Chinese": "red"}

v_2d_df["symbol"] = v_2d_df["language"].map(symbol_map)

# Create traces for each topic
traces = []
for language in v_2d_df["language"].unique():
    df = v_2d_df[v_2d_df["language"] == language]
    trace = go.Scatter(
        x=df["x"],
        y=df["y"],
        mode="markers",
        name=language,
        marker=dict(color=color_map[language], size=6),
        customdata=df[["formatted_summary"]],
        # hovertemplate="<b>%{customdata[0]}</b><extra></extra>",
        hoverinfo="none",
    )
    traces.append(trace)

# Create the layout
layout = go.Layout(
    title=f"t-SNE Visualization of News Articles: Russo Ukrainian War (d = 3)",
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
with open("Narrative_DIff/narrative_interactive_plot.html", "w") as f:
    f.write(html_content)
