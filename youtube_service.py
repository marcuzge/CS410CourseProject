from googleapiclient.discovery import build

# Communicate with Youtube APIs
# Credit for comment handling https://github.com/youtube/api-samples/blob/master/python/comment_handling.py
# Credit for comment threads https://developers.google.com/youtube/v3/docs/commentThreads
class YoutubeService:
    def __init__(self, video_url):

        self._video_url = video_url
        self._video_id = video_url.split("?v=")[1]
        self._service = build("youtube", "v3", developerKey="YOUR_API_KEY")

    # Retrieve all the comments from a video, if --include_replies is true, replies from the top level comments would also be included. 
    def get_comment_threads(self, include_replies):
        comments = []

        results = (
            self._service.commentThreads()
            .list(
                part="snippet", videoId=self._video_id, textFormat="plainText", maxResults=100
            )
            .execute()
        )

        while results:
            for comment_thread in results["items"]:
                comment = comment_thread["snippet"]["topLevelComment"]
                comment_text = comment["snippet"]["textDisplay"]
                comments.append(comment_text)

                if include_replies and comment_thread["snippet"]["totalReplyCount"] > 0:
                    # retrieve the replies from the comment. 
                    replies_results = (
                        self._service.comments()
                        .list(
                            part="snippet",
                            parentId=comment_thread["id"],
                            textFormat="plainText",
                        )
                        .execute()
                    )
                    replies = replies_results["items"]
                    # Note that replies are in reversed order.
                    for reply in reversed(replies):
                        reply_text = reply["snippet"]["textDisplay"]
                        comments.append(reply_texy)

            if "nextPageToken" in results:
                results = (
                    self._service.commentThreads()
                    .list(
                        part="snippet",
                        videoId=self._video_id,
                        textFormat="plainText",
                        pageToken=results["nextPageToken"],
                        maxResults=100,
                    )
                    .execute()
                )
            else:
                return comments

    # Returns the title of the video.
    def get_video_title(self):
        response = self._service.videos().list(part="snippet", id=self._video_id).execute()
        return response["items"][0]["snippet"]["title"]
