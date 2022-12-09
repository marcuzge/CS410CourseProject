import matplotlib.pyplot as plt

# Creates the pie chart for the sentiment analysis result
def create_pie_chart(dataframe, video_title, filename):

    dataframe["Counts"] = 1
    plot = dataframe.groupby(['Sentiment']).sum().plot.pie(y="Counts", figsize=(12, 12), startangle=90, autopct='%1.0f%%')
    plot.set_title(
    f"Sentiment Analysis Results\n{video_title}",
    fontdict={"color": "white", "fontweight": "bold", "fontsize": 15},
    linespacing=2,
    pad=35,
    )

    figure = plot.get_figure()
    figure.savefig(filename, facecolor="black", dpi=600)
