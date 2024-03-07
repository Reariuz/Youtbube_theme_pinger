# Youtbube_theme_pinger

The purpose of this Software is to inform a User upon a video that mentions a word in his observation list.

To get started you need a google API KEY.
You can get it from here:
[Youtube > Data Api](https://developers.google.com/youtube/v3/getting-started?hl=de)
If you achieved one place it in the youtube_api.py as DEVELOPER_KEY

---
Next you have to fill two files.
1. Channel List.
   Fill the file with the Youtube Channels you want to observe.
   The format is:
   channel-ID;Channelname
   UCZHpIFMfoJJ_1QxNGLJTzyA;@mrWissen2go

   You get the ID by going to the channel-info, scroll down to "share" and copy channel-ID
   The Channelname ist basically meaningless. It gets transportet to the final report without prozessing. 
   Write what you want.

2. search Terms
   This List contains the words to look up for in the video.
   The Format is:
   Term;weight
   Humanismus;3

   The term can contain empty spaces.
   Make sure to not include terms more than once. This may mess up the relevancy calculation later on.
   It is  allowed to include more specific words, for example: "party" & "politcal Party". If the text contains the word "politcal Party" the programm will find and mark both terms, Therefore giving extra points to relevancy. Use this for your advance.
   The weight is how valuable the mention of the word is for your relevancy.
   1 means close to no relevancy, 10 means maximum relevance.
   Try using high values only for specific terms and low ones for generic stuff.

   The order of the Words in the file is the order in wich words will be marked in the result.
   You can order by alphabet to better find words or order it by weight to have the importand words upfront.

If you have set up your programm correctly you can run the main.py
It will result in a single report per channel that mentions the word as a txt file but formatted as a markdown text.