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
    # Open the file in read mode
    with open('Channel_list.txt', 'r') as file:
        for line in file:
            # Read all the lines of the file into a list
            Channel = line.replace("\n","").split(';')
            Channel_list.append(Channel)

    with open('search_terms.txt', 'r') as file:
        for line in file:
            # Read all the lines of the file into a list
            term = line.replace("\n","").split(';')
            search_list.append(term)

    print(search_list)


    video_list = []
    for line in Channel_list:
        video_list.append(get_current_video(line[0],line[1]))

    #print(video_list)

    with open('current_videos.json', 'r') as fp:
        previous_video = json.load(fp)
    
    #print(previous_video)
    #print(video_list)

    control_list = []
    for line in video_list:
        #print(line)
        #print(previous_video['Channel_Id'])

        if not line in previous_video:

            #do nothing
            print('new value found')
            print(line)
            control_list.append(line)
        else:
            print("comparrison worked")
            print(line)

    '''
    erst datei schreiben wenn programm fertig
    with open('current_videos.json', 'w') as fp:
        json.dump(video_list, fp)
    '''
        
    for line in control_list:
        relevance_indicator = bool(False)

        #get the transcript from the video in german
        transcript = YouTubeTranscriptApi.get_transcript(line['latest_Video_Id'], languages=['de'])

        overall_weight = 0

        resulting_table = []
        #resulting_table.append(line)

        found_words = []



        for word in search_list:

            result = search(word[0],transcript)
            #print(word[0],' Gewicht ist:', word[1])


            if math.log(len(result)+1)*int(word[1]) > 0:
                relevance_indicator = bool(True)
                new_list =[]

                found_words.append(word[0])

                new_list.append('Das Wort:"'+ word[0] +'" kommt '+ str(len(result))+ ' mal vor und ist mit '+ str(word[1])+ ' gewichtet')
                #new_list.append('gesamtgewicht ist:'+ str(math.log(len(result)+1)*int(word[1])))

                #check this line
                overall_weight += math.log(len(result)+1)*int(word[1])

                #reformats the transcript results
                for line2 in result:
                    new_dict ={}
                    
                    new_dict['text']=line2['text']
                    new_dict['minutes'] = int(line2['start']/60)
                    new_dict['seconds'] = int(line2['start']%60)
                    new_list.append(new_dict)
                
                #pprint.pprint(new_list)
                resulting_table.append(new_list)

            #format this shit

            #call export function
        if relevance_indicator == bool(True):
            #hier soll das zeilenweise Ausgabeformat entstehen
            print("create message for:" + str(line))
            message = []
            message.append("[**"+get_video_metadata(line['latest_Video_Id'])+"**](https://youtu.be/"+line['latest_Video_Id']+"?feature=shared)")
            message.append(line['Channel_Name'])
            message.append("---")
            message.append("*Relevanz: **"+str(overall_weight)+"***")
            message.append("*Folgende Wörter wurden im Video identifiziert:*")
            for word in found_words:
                message.append("+"+word)
            message.append("---")
            for line in resulting_table:
                message.append(line[0])
                for subline in line[1:]:
                    try:
                        #message.append("+ " + str(subline['minutes']) + ":" + str(subline['seconds']) + "- \"" +str(subline['text']) +"\"")
                        message.append("+ " + str(subline['minutes'])  + ":" + str(subline['seconds'])+ " - " +str(subline['text']))
                    except:
                        print("error")
                        print(subline)
                        
            print("write file")
            with open(message[1]+'_testfile.txt', 'w') as f:
                for row in message:
                    f.write(f"{row}\n")
            message.clear()  
    
    #pprint.pprint(message)

if __name__ == "__main__":
    main()