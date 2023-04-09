import instaloader
import snscrape.modules.twitter as sntwitter
import re
import requests

URLREGEX=r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"

class postdata:
    
    def __init__(self,id=None, caption=None, url=[] , date=None, tags=[], mentions=[], links=[]):
        self.id=id
        self.caption=re.sub(r'\n', ' ', caption)
        self.url=url
        self.date=date
        self.tags=tags
        self.mentions=mentions
        self.links=links

class Crawler:
    
    def __init__(self, username, smedia, maxcount=10):
        self.username=username
        self.smedia=smedia
        self.maxcount=maxcount
        self.postlist=[]

    def get_byid(self, id):
        for post in self.posts:
            if id==post.id:
                return post
        return None
    
    def crawl(self):
        if self.smedia=='instagram':
            self.crawlinstagram()
        elif self.smedia=='twitter':
            self.crawltwitter()

    def crawlinstagram(self):
        loader=instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, self.username)
        for i, post in enumerate(profile.get_posts()):
            if i>self.maxcount:
                break
            self.postlist.append(postdata(id=post.url[28:40],
                                   caption=post.caption,
                                   url=post.url,
                                   date=post.date,
                                   tags=post.tagged_users,
                                   mentions=post.caption_mentions,
                                   links=re.findall(URLREGEX, post.caption) if post.caption else None
                                ))
    def crawltwitter(self):
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+self.username).get_items()):
            if i>self.maxcount:
                break
            self.postlist.append(postdata(id=tweet.id,
                                   caption=tweet.content,
                                #   url=tweet.url,
                                #    date=tweet.created,
                                   mentions=[user.username for user in tweet.mentionedUsers] if tweet.mentionedUsers else None,
                                   links=re.findall(URLREGEX, tweet.content) if tweet.content else None
                                ))

    def detect_suspicion(self):
        for post in self.postlist:
            post.cleaned=cleantext(post.caption)
            post.category=classify(post.cleaned)

def classify(data):

    url = "https://sead.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": "320e403e955c478e824e69ede8f06eda",
        "Apim-Request-Id": "4ffcac1c-b2fc-48ba-bd6d-b69d9942995a",
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "PARTICIPANT_ID_HERE",
                "text": data,
                "modality": "text",
                "language": "en",
                "participantId": "PARTICIPANT_ID_HERE"
            }
        },
        "parameters": {
            "projectName": "seader",
            "verbose": True,
            "deploymentName": "seader",
            "stringIndexType": "TextElement_V8"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    answer = response.json()
    
    return answer['result']['prediction']['topIntent']

def cleantext(text):
    text=text.strip().lower()
    text=re.sub(r'\s+', ' ', text)
    text=re.sub(r'\s*[#@]\w+\s*', ' ', text)
    text=re.sub(r'[^\w]', '', text)
    return text

def crawlandreport(username, smedia):
    crawler=Crawler(username, smedia)
    crawler.crawl()
    crawler.detect_suspicion()
    
    spam=[]
    scam=[]
    phishing=[]
    baiting=[]
    identitytheft=[]
    pretexting=[]
    suspicious_ids=set()
    suspicious_links=set()
    
    for post in crawler.postlist:
        category=post.category
        if category=='None':
            continue
        if post.mentions:
            suspicious_ids.update(post.mentions)
        if post.links:
            suspicious_links.update(post.links)
        if category == 'spam':
            spam.append(post.caption)
        elif category == 'scam':
            scam.append(post.caption)
        elif category == 'baiting':
            baiting.append(post.caption)    
        elif category == 'phishing':
            phishing.append(post.caption)
        elif category == 'identity-theft':
            phishing.append(post.caption)
        elif category == 'pre-texting':
            phishing.append(post.caption)

    report=''
    
    if suspicious_ids:
        report+="Suspicious user profiles :\n\t" + '\n\t'.join(suspicious_ids) + '\n'
    if suspicious_links:
        report+="These links are appears to be malicious :\n\t" + '\n\t'.join(suspicious_links) + '\n'
    if spam:
        report+="\nSpam detected:\n\t" + '\n\t'.join(spam) + '\n'
    if scam:
        report+="\nScam detected:\n\t" + '\n\t'.join(scam) + '\n'
    if baiting:
        report+="\nBaiting detected:\n\t" + '\n\t'.join(baiting) + '\n'
    if phishing:
        report+="\nPhishing detected:\n\t" + '\n\t'.join(phishing) + '\n'
    if identitytheft:
        report+="\nPhishing detected:\n\t" + '\n\t'.join(identitytheft) + '\n'
    if pretexting:
        report+="\nPhishing detected:\n\t" + '\n\t'.join(pretexting) + '\n'

    if not report :
        report="\nNo suspicious activity found on this profile"
    else: 
        summary='This profile contains suspicious activities relevent to be ' + ('spam' if spam else '') + ('phishing' if phishing else '') + ('scam' if scam else '') + ('baiting' if baiting else '') + ('identity-theft' if identitytheft else '') + ('pre-texting' if pretexting else '')
        report=summary + '\n' + report
    return report

def crawlandreport_from_url(url):
    doms=url.split('/')
    try:
        print(doms)
        smedia=doms[2]
        username=doms[3]
        dot=smedia.split('.')
        print(dot)
        smedia=dot[1] if len(dot)==3 else dot[0]
    
    except IndexError:
        raise IOError("URL is not valid")
    print(username, smedia)
    return crawlandreport(username, smedia)