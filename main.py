import json
import math
import pprint

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_api import get_current_video,get_video_metadata

result_list =[]
search_list = []


# searches for a term of the searchlist in the transcript returns the line
def search(term,transcript):
    result_list.clear()
    for line in transcript:
        if term in line['text']:
            result_list.append(line)
    
    return result_list



def main():

    Channel_list = []
    video_list = []
    control_list = []

    # Open the Channel List and transfer to Channel_list
    with open('Channel_list.txt', 'r') as file:
        for line in file:
            # Read all the lines of the file into a list
            Channel = line.replace("\n","").split(';')
            Channel_list.append(Channel)

    # Open the search term List and transfer to Search_list
    with open('search_terms.txt', 'r') as file:
        for line in file:
            # Read all the lines of the file into a list
            term = line.replace("\n","").split(';')
            search_list.append(term)


    # get the current video from youtube_api function
    for line in Channel_list:
        video_list.append(get_current_video(line[0],line[1]))


    #load a list of the last checked videos an channels to compare
    with open('current_videos.json', 'r') as fp:
        previous_video = json.load(fp)


    #Compares the lists to generate the Control_list containing only the changed entrys
    for line in video_list:
        if not line in previous_video:
            control_list.append(line)

    '''
    ### TODO - de-comment this paragraph to write the new video_ids to file for next-time comparission
    ### DONOT de-comment this before because it will overwrite the json-file and future test might not create videos
    erst datei schreiben wenn programm fertig
    with open('current_videos.json', 'w') as fp:
        json.dump(video_list, fp)
    '''

    #main loop

    for line in control_list:
        relevance_indicator = bool(False)

        #get the transcript from the video in german
        transcript = YouTubeTranscriptApi.get_transcript(line['latest_Video_Id'], languages=['de'])

        #set the relevancy value for each video back to 0
        overall_weight = 0

        resulting_table = []
        found_words = []


        for word in search_list:

            result = search(word[0],transcript)


            if math.log(len(result)+1)*int(word[1]) > 0:
                relevance_indicator = bool(True)
                new_list =[]

                found_words.append(word[0])

                new_list.append('Das Wort:"'+ word[0] +'" kommt '+ str(len(result))+ ' mal vor und ist mit '+ str(word[1])+ ' gewichtet')

                #adding the weight to the overall using logaryhmic
                overall_weight += math.log(len(result)+1)*int(word[1])

                #reformats the transcript results
                for line2 in result:
                    new_dict ={} 
                    new_dict['text']=str(line2['text']).replace("\n", " ")
                    new_dict['minutes'] = int(line2['start']/60)
                    new_dict['seconds'] = int(line2['start']%60)
                    new_list.append(new_dict)
                resulting_table.append(new_list)


        #if Words were found in video toggle the formating 
        if relevance_indicator == bool(True):
            #Format the results line-wise and write them to a list
            print("create message for:" + str(line))
            message = []
            message.append("[**"+get_video_metadata(line['latest_Video_Id'])+"**](https://youtu.be/"+line['latest_Video_Id']+"?feature=shared)")
            message.append(line['Channel_Name'])
            message.append("---")
            message.append("*Relevanz: **"+str(overall_weight)+"***")
            message.append("*Folgende Wörter wurden im Video identifiziert:*")
            #adding all the words from the searchlist that has ben found
            for word in found_words:
                message.append("+"+word)
            #format and add all the wordspecific timestamps and quotes    
            message.append("---")
            for line in resulting_table:
                message.append(line[0])
                for subline in line[1:]:
                    ### TODO -keep try except until final tests
                    try:
                        message.append("+ " + str(subline['minutes'])  + ":" + str(subline['seconds'])+ " - " +str(subline['text']))
                    except:
                        print("error")
                        print(subline)
                message.append("---")

            pprint.pprint(message)

            print("write file")
            with open(message[1]+'_testfile.md', 'w') as f:
                for row in message:
                    f.write(f"{row}\n")
            message.clear()  
    
    #pprint.pprint(message)

if __name__ == "__main__":
    main()