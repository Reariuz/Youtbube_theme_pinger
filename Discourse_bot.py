import os
DISCOURSE_API_KEY = os.getenv("DISCOURSE_API_KEY")
DISCOURSE_API_NAME = os.getenv("DISCOURSE_API_NAME")

from fluent_discourse import Discourse
client = Discourse(base_url="https://hub.diehumanisten.de", username=DISCOURSE_API_NAME,
                   api_key=DISCOURSE_API_KEY, raise_for_rate_limit=False)


def Hub_POST(message):

    data = {
        'title': 'testnaricht',
    # content
        'raw': '\n'.join(message),
    # Get a post ID when you need to reply to a post
    #should be the id of the thread
        'topic_id': '22032',
    # Category ID
    #'category': '5',
    # tags
    # wozu sind die tags?
    #    'tags': ['Label 1', 'Label 2'],

    }
    latest = client.posts.json.post(data)
    #print(latest)

# this part is only needed for testing and bugfixing this shit
def main():
    Hub_POST("lorem ipsum dolor sit amet")
    exit()
    

if __name__ == "__main__":
    main()


