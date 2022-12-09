import json

from argparse import ArgumentParser
from sentiment_analyzer import clean_comments, create_dataframe, analyze_comments
from youtube_service import YoutubeService
from pie_chart import create_pie_chart

# Accepts user interaction in console and the main class for the application.  
def main():
    try:
        # Creates the ArguemntParser for console interaction.
        argument_parser = ArgumentParser()
        argument_parser.add_argument("-u", "--url", help="URL of the video to be analyzed")
        argument_parser.add_argument(
            "-d", "--defaultconfig", action="store_true", help="Uses config.json by defualt"
        )
        argument_parser.add_argument(
            "-cf",
            "--configfile",
            default="config.json",
            help="Provide a config file",
        )
        argument_parser.add_argument(
            "-ir",
            "--include_replies",
            action="store_true",
            help="Include replies to comments for sentiment analysis",
        )
        argument_parser.add_argument(
            "-o",
            "--output_file",
            default="sentiment_analysis_chart.png",
            help="Name/Path of the output chart",
        )
        args = argument_parser.parse_args()

        if not (args.url or args.defaultconfig):
            argument_parser.print_help()
            raise SystemExit("Please specify correct parameters!")

        with open(args.configfile, encoding="utf-8") as configfile:
            config = json.load(configfile)

        video_url = config["url"] if args.defaultconfig else args.url
        include_replies = config["include_replies"] if args.defaultconfig else args.include_replies
        output_file = config["output_file"] if args.defaultconfig else args.output_file

        # Communicates with youtube API and perform sentiment analysis. 
        youtube_service = YoutubeService(video_url)
        all_comments = youtube_service.get_comment_threads(include_replies)
        comments_dataframe = create_dataframe(all_comments)
        cleaned_dataframe = clean_comments(comments_dataframe)
        results_dataframe = analyze_comments(cleaned_dataframe)

        # Creates the pie chart.
        video_title = youtube_service.get_video_title()
        create_pie_chart(results_dataframe, video_title, output_file)

    except KeyboardInterrupt:
        print("Keyboard Interrupt, program exited.")


if __name__ == "__main__":
    main()
