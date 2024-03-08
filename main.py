import json
import math

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_api import get_current_video, get_video_metadata

def read_file_to_list(filename, delimiter=';'):
    """Reads a file into a list of lines."""
    try:
        with open(filename, 'r') as fp:
            return [line.strip().split(delimiter) for line in fp]
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def search(word, transcript):
    """Searches the transcript for the specified word."""
    return [line for line in transcript if word in line['text']]

def get_transcript(video_id, language='de'):
    """Gets the transcript for a video in the specified language."""
    try:
        return YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    except Exception as e:
        print(f"Error getting transcript for video {video_id}: {e}")
        return []

def calculate_relevance(result, weight):
    """Calculates the relevance of a search result."""
    return math.log(len(result) + 1) * int(weight)

def format_result(word, results, weight):
    """Formats the search results for a word."""
    message = [f'Das Wort "{word}" kommt {len(results)} mal vor und ist mit {weight} gewichtet.']
    for result in results:
        minutes = int(result['start'] / 60)
        seconds = int(result['start'] % 60)
        text = result['text'].replace("\n", " ")
        message.append(f"+ {minutes}:{seconds:02d} - {text} <br>")
    message.append("---")
    return message

def generate_output(video, overall_weight, found_words, resulting_table):
    """Generates and prints the output message based on the search results."""
    video_metadata = get_video_metadata(video['latest_Video_Id'])
    video_url = f"https://youtu.be/{video['latest_Video_Id']}?feature=shared"
    message = [
        f"[**{video_metadata}**]({video_url})",
        video['Channel_Name'],
        "---",
        f"*Relevanz: **{overall_weight:.2f}***<br>",
        "*Folgende Wörter wurden im Video identifiziert:*<br>"
    ] + [f"+{word}<br>" for word in found_words] + ["---"] + resulting_table

    filename = f"{video['Channel_Name']}_testfile.md"
    with open(filename, 'w') as f:
        for line in message:
            f.write(f"{line}\n")
    print(f"Output written to {filename}")

def main():
    channel_list = read_file_to_list('Channel_list.txt')
    search_terms = read_file_to_list('search_terms.txt')
    
    try:
        with open('current_videos.json', 'r') as fp:
            previous_videos = json.load(fp)
    except FileNotFoundError:
        print("current_videos.json not found, proceeding without previous videos.")
        previous_videos = []

    video_list = [get_current_video(channel_id, channel_name) for channel_id, channel_name in channel_list]
    new_videos = [video for video in video_list if video not in previous_videos]

    # Save the updated list of videos for future comparisons
    with open('current_videos.json', 'w') as fp:
        json.dump(video_list, fp)

    for video in new_videos:
        transcript = get_transcript(video['latest_Video_Id'])
        overall_weight, found_words, resulting_table = 0, [], []

        for word, weight in search_terms:
            result = search(word, transcript)
            relevance = calculate_relevance(result, int(weight))
            if result:
                overall_weight += relevance
                found_words.append(word)
                resulting_table.extend(format_result(word, result, weight))

        if found_words:
            generate_output(video, overall_weight, found_words, resulting_table)

if __name__ == "__main__":
    main()
