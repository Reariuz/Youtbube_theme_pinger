from fluent_discourse import Discourse
client = Discourse(base_url="https://hub.diehumanisten.de", username="rene.bruns",
                   api_key="75e55d01584d41ebc915ee911ab9a08f2e4b992d7a2429da09dbe19b718c32b0", raise_for_rate_limit=False)


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
    print(latest)

# this part is only needed for testing and bugfixing this shit
def main():
    Hub_POST("lorem ipsum dolor sit amet")
    exit()
    

if __name__ == "__main__":
    main()


