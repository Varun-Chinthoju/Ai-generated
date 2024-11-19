"""
note: this doesn't work, i'm just playing around with ai
"""


import tkinter as tk
from youtubesearchpython import VideosSearch
from pytube import YouTube
import webbrowser


class YouTubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube App")
        self.search_query = tk.StringVar()

        # Search frame
        search_frame = tk.Frame(self.root)
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_query).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Search", command=self.search_videos).pack(side=tk.LEFT)
        search_frame.pack(padx=10, pady=10)

        # Video list frame
        self.video_list_frame = tk.Frame(self.root)
        self.video_list_frame.pack(padx=10, pady=10)

        # Error label
        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack(padx=10, pady=10)

    def search_videos(self):
        """Search YouTube for query and display video titles."""
        query = self.search_query.get()
        if not query:
            self.error_label['text'] = "Enter search query"
            return

        try:
            videos_search = VideosSearch(query, limit=10)
            video_urls = videos_search.result["result"]
            self.error_label['text'] = ""
        except Exception as e:
            self.error_label['text'] = f"Search failed: {str(e)}"
            return

        # Clear previous video list
        for widget in self.video_list_frame.winfo_children():
            widget.destroy()

        if not video_urls:
            self.error_label['text'] = "No videos found"
            return

        for i, video in enumerate(video_urls):
            video_title = video["title"]
            video_link = video["link"]

            # Create button for each video
            tk.Button(self.video_list_frame, text=video_title, wraplength=400, command=lambda link=video_link: self.play_video(link)).pack(fill=tk.X)

    def play_video(self, link):
        """Open video in default browser."""
        try:
            webbrowser.open(link)
        except Exception as e:
            self.error_label['text'] = f"Failed to open video: {str(e)}"


def main():
    root = tk.Tk()
    app = YouTubeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()