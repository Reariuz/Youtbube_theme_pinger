from fluent_discourse import Discourse
client = Discourse(base_url="url", username="user_name",
                   api_key="user_key", raise_for_rate_limit=True)


def Hub_POST(message):

    data = {
        'title': '',
    # content
        'raw': message,
    # Get a post ID when you need to reply to a post
    #should be the id of the thread
        'topic_id': '5',
    # Category ID
    #'category': '5',
    # tags
    # wozu sind die tags?
        'tags': ['Label 1', 'Label 2'],

    }
    latest = client.posts.json.post(data)

# this part is only needed for testing and bugfixing this shit
def main():
    exit()
    

if __name__ == "__main__":
    main()


