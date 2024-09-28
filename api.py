from flask import jsonify
import praw
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import os

    
# Set the path where the images will be saved
SAVE_DIR = 'static/images'

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

print("API - Start")

# Connecting to the Reddit API to retrieve posts and comments from the SkincareAddiction subreddit (with 3.9 million subscribers) using the keyword 
#'ordinary' to analyze the brand. Saving the retrieved data in CSV files

# Credentials
client_id = '_Dg7T7G5aQ3WIMFli6d31g'
client_secret = 'gjenP2Q3zzLAI_eukg7v3mbM780kGg'
user_agent = 'my_bot/0.1 by u/No-Cherry-3059'

post_count_limit = 10
comment_count_limit = 100

GET_SUBREDDIT = ''
GET_WORD = ''
    
# Initializing PRAW with the credentials
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


def datacheck(SUBREDDIT, WORD):
    # Setting the variables
    GET_SUBREDDIT = SUBREDDIT # 'SkincareAddiction'
    GET_WORD = WORD #'ordinary'


    # Retrieving posts (limited to 300) and associated comments from the SkincareAddiction subreddit
    print("API - Request Data")
    subreddit = reddit.subreddit(GET_SUBREDDIT)
    print("API - Response")
    posts = list(subreddit.search(GET_WORD, limit = post_count_limit))

    Post_Cleaned = clean_Posts(posts)
    Comments_Cleaned = clean_Comments(posts)
   
   
    print("API - Loading Dataframes")         
    df_comments =pd.DataFrame(Comments_Cleaned) 
    df_posts =pd.DataFrame(Post_Cleaned) 
    print("API - End")      

    #
    df_comments.to_csv('ordinary_comment.csv', index=False)
    df_posts.to_csv('ordinary_post.csv', index=False)

    # Data cleaning
    # Converting the 'created' column to a readable datetime format and storing it in a new column named 'date'. 
    # Afterward, removing the original 'created' column

    df_comments=pd.read_csv('ordinary_comment.csv')
    df_posts=pd.read_csv('ordinary_post.csv')
    df_comments['date'] = pd.to_datetime(df_comments['created'], unit='s').dt.date
    df_posts['date'] = pd.to_datetime(df_posts['created'], unit='s').dt.date
    df_comments = df_comments.drop('created', axis=1)
    df_posts = df_posts.drop('created', axis=1)

    # 230 posts related to the topic of The Ordinary brand were retrieved from the subreddit
    df_posts.info()

    

    ordinary_posts = df_posts[df_posts['title'].str.contains(GET_WORD, case=False)].copy()

    ordinary_posts['selftext'] = ordinary_posts['selftext'].fillna(' ')
    ordinary_posts[['polarity post', 'subjectivity post']] = ordinary_posts['title'].apply(lambda x: pd.Series(analyze_sentiment(x)))
    ordinary_posts[['polarity selftext', 'subjectivity selftext']] = ordinary_posts['selftext'].apply(lambda x: pd.Series(analyze_sentiment(x)))
    ordinary_posts['selftext sentiment'] = ordinary_posts ['polarity selftext'].apply(lambda x: pd.Series(sentiment_type(x)))
    
    get_chart(ordinary_posts)        
    #attitude_result = get_post_description_sentiment(ordinary_posts)
    attitude_result = get_comment_sentiment(df_comments)        
 
    return jsonify({
        'post_count': len(Post_Cleaned),
        'comment_count': len(Comments_Cleaned),        
        'attitude_result': attitude_result    
    })



def clean_Posts(posts):
    print("API - Clean Post Data")
    Post_Cleaned = [] 
    for post in posts:    
        Post_Cleaned.append({
            'title': post.title,
            'selftext': post.selftext,
            'score': post.score,
            'num_comments': post.num_comments,
            'created': post.created_utc
        }) 
    return Post_Cleaned


def clean_Comments(posts):
    print("API - Clean Comment Data")
    Comments_Cleaned = []

    for post in posts:        
        comment_count = 0 
        post.comments.replace_more(limit=1) 
        for comment in post.comments.list():  
            print(post.title)
            if isinstance(comment, praw.models.MoreComments):
                continue 
            if comment_count<comment_count_limit:
                Comments_Cleaned.append({
                    'title': post.title, 
                    'selftext': post.selftext,
                    'num_comments': post.num_comments,
                    'comment': comment.body,
                    'created': post.created_utc 
                })  
                comment_count += 1
            else:
                break  # Stop the loop after 3 comments
    print("API - Comment Data Cleaned")
    return Comments_Cleaned


def get_chart(df_posts):    
    plt.figure(figsize=(10, 6))
    sns.histplot(df_posts['polarity post'], bins=20, kde=True)
    plt.title('Distribution of Post Title Polarity')
    plt.xlabel('Polarity')
    plt.ylabel('Frequency')
    #plt.show()
        # Define the path where the image will be saved
    filename = 'result_chart_1.png'
    filepath = os.path.join(SAVE_DIR, filename)

    # Save the plot to the specified file path
    plt.savefig(filepath)
    plt.close() 
    
    

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity   

def get_post_description_sentiment(posts):       
    sentiment_selftext_counts = posts['selftext sentiment'].value_counts()
    most_freq_selftext_sentiment = sentiment_selftext_counts.idxmax()
    print ('Most frequent selftext sentiment:')
    print (most_freq_selftext_sentiment)
    return most_freq_selftext_sentiment


def get_comment_sentiment(df_comments):       
    comments = df_comments[df_comments['title'].str.contains(GET_WORD, case=False)].copy()
    comments[['polarity comment', 'subjectivity comment']] = comments['comment'].apply(lambda x: pd.Series(analyze_sentiment(x)))
    comments['comment sentiment'] = comments ['polarity comment'].apply(lambda x: pd.Series(sentiment_type(x)))
    sentiment_comment_counts = comments['comment sentiment'].value_counts()
    most_freq_comment_sentiment = sentiment_comment_counts.idxmax()
    print (most_freq_comment_sentiment)
    return most_freq_comment_sentiment

    
def sentiment_type(x):
    if x == 0:
        return ('Neutral')
    elif x > 0:
        return ('Positive')
    else:
        return ('Negative')


def get_mostusedwords(commentlist):
    freq_word_comment = commentlist.words_
    top_5_words = sorted(freq_word_comment.items(), key=lambda x: x[1], reverse=True)[:5]
    print ('Top 5 most frequent words in the comment section:')
    for word,_ in top_5_words:
        print (word)
    return top_5_words

    































def get_sentiment(ordinary_posts):
    
    # NEW CODE
    ordinary_posts['post sentiment'] = ordinary_posts ['polarity post'].apply(lambda x: pd.Series(sentiment_type(x)))
    ordinary_posts['selftext sentiment'] = ordinary_posts ['polarity selftext'].apply(lambda x: pd.Series(sentiment_type(x)))

    # SENTIMENT POST COUNTS

    sentiment_post_counts = ordinary_posts['post sentiment'].value_counts()
    print (sentiment_post_counts)

    # SENTIMENT SELFTEXT COUNTS
    sentiment_selftext_counts = ordinary_posts['selftext sentiment'].value_counts()
    print (sentiment_selftext_counts)

    # MOST FREQUEST SENTIMENT IN POST
    most_freq_post_sentiment = sentiment_post_counts.idxmax()
    print ('Most frequent post sentiment:')
    print (most_freq_post_sentiment)


    # MOST FREQUEST SENTIMENT IN SELFTEXT

    most_freq_selftext_sentiment = sentiment_selftext_counts.idxmax()
    print ('Most frequent selftext sentiment:')
    print (most_freq_selftext_sentiment)