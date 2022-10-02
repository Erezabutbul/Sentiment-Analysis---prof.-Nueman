import matplotlib.pyplot as plt
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import flair



##########################################  READ ME   ##################################################


# make sure the txt file is in the right format A \n B \n ex....
# sanity check printing the output list
# make sure there are no special chars like  - '
# change the speakers name , first AND second
# change the path id needed
# change the name of the CSV file
# make sure that you have ":" after the name of each speaker - in each line
# if not - make sure that the name of the other person is not in the utterance
# change names of speakers as the scrips demands
# change names of name_of_curr_file_to_write as the name of the script
#########################################################################################################


########################## Helping functions ##############################################################
# Extract sentiment score from text by model

def get_Vader_score(txt):
    sentiment_dict = vader_obj.polarity_scores(txt)
    compound = sentiment_dict['compound']
    # return_dict["vader_score"] = compound
    return compound


# def get_flair_score(txt):
#     s = flair.data.Sentence(txt)
#     flair_sentiment.predict(s)
#     total_sentiment = s.labels[0]
#     sign = 1 if total_sentiment.value == 'POSITIVE' else -1
#     score = total_sentiment.score
#     tmp = sign * score
#     ns = (tmp + 1) / 2
#     return ns
#

###############################################################################################################


# change the path to where the file is
# TODO - find a way to make the path browsable
sub_file_path = r"C:\Users\Erez\Desktop\Git Projects\SA\American_sniper.txt"

# Read from file
with open(sub_file_path, 'r') as f:
    lines = f.readlines()

############################################ INIT #########################################################
first_speaker = "CHRIS"
second_speaker = "TAYA"

i = 0
j = 0
ut_index = 0
counter_balance = 0
counter_of_lines = 0
counter_of_speaker_A = 0
counter_of_speaker_B = 0
A = list()
B = list()
rows = list()
output = list()
utterance = list()
scores_speaker_A = list()
scores_speaker_B = list()
name_of_curr_file_to_write = "American Sniper sentiment analysis Data "

#########################################################################################################


for line in lines:
    counter_of_lines += 1
    # check if speaker A is speaking in this line
    if line.__contains__(first_speaker):
        counter_of_speaker_A += 1
        A.append(line)
        utterance.append(line)
        # if speaker A spoke twice in a row, combine the statements
        if (i - 1 >= 0) and utterance[i - 1].__contains__(first_speaker):
            utterance[i - 1] = utterance[i - 1] + line.replace(first_speaker.lower(), "")
            utterance.remove(utterance[len(utterance) - 1])
            i -= 1
    else:
        # Speaker B is speaking in this line
        counter_of_speaker_B += 1
        B.append(line)
        utterance.append(line)
        if i - 1 >= 0 and utterance[i - 1].__contains__(second_speaker.lower()):
            utterance[i - 1] = utterance[i - 1] + line.replace(second_speaker, "")
            utterance.remove(utterance[len(utterance) - 1])
            i -= 1
    i += 1

# Remove the name of the speaker from the utterance
for ut in utterance:
    if ut.__contains__(second_speaker):
        output.append(ut.replace(second_speaker.lower(), ""))
    else:
        output.append(ut.replace(first_speaker.lower(), ""))
    output[j] = output[j].replace("\n", "")
    j += 1

################# Get sentiments scores from the utterances #######################################################################


# Vader Model
vader_obj = SentimentIntensityAnalyzer()

# flair Model
# flair_sentiment = flair.models.TextClassifier.load('sentiment-fast')


# now output contains the data by utterances
scores_Vader = list()
scores_flair = list()
for getGrade in output:
    scores_Vader.append(get_Vader_score(getGrade))
    # scores_flair.append(get_flair_score(getGrade))

if scores_Vader.__len__() == 0:
    scores = scores_flair
else:
    scores = scores_Vader

########################### Plot the data ##############################################################

# X axis = time line :
# speaker A presented in even numbers
# speaker B presented in odd numbers
# Y axis = sentiment score given by model

x_even = range(0, len(scores), 2)
x_odd = range(1, len(scores), 2)

# TODO - find a more elegant way to copy the scores into a new list
for j in range(0, len(scores), 2):
    scores_speaker_A.append(scores[j])

for w in range(1, len(scores), 2):
    scores_speaker_B.append(scores[w])

plt.plot(x_even, scores_speaker_A, color='blue', linestyle='dashed', linewidth=1, marker='o', markerfacecolor='blue',
         markersize=4)
plt.plot(x_odd, scores_speaker_B, color='red', linestyle='dashed', linewidth=1, marker='o', markerfacecolor='red',
         markersize=4)

plt.xlabel(first_speaker + " in blue, " + second_speaker + " in red")
plt.ylabel("Score in sentiment")
plt.title('Sentiment Analysis Scores')
plt.show()



################################# Export to CSV ###############################################


# field names
fields = ['index', 'score','A/B','utterance']

# data rows of csv file
for index in range(0, len(scores)):
    curr_line_str = first_speaker
    if index % 2 != 0:
        curr_line_str = second_speaker
    if ut_index < len(utterance):
        rows.append([index, scores[index], curr_line_str, utterance[ut_index]])
    ut_index += 1

with open(name_of_curr_file_to_write, 'w') as file:
    # using csv.writer method from CSV package
    write = csv.writer(file)
    write.writerow(fields)
    write.writerows(rows)
f.close()

########################################################## Sanity check ###############################################
# print("THIS IS OUTPUT : ")
# print(output)
# print()
# print()
# print("THIS IS utterance")
# print(utterance)
# print()
# print()

