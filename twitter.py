import tweepy
import time
import random
from datetime import datetime
import os

# ייבוא פונקציות הסקריפינג מהקוד שלך
from your_telegram_bot_script import scrape_ynet, scrape_arutz7, scrape_walla  # החלף בנתיב הקובץ המדויק של הקוד שלך

# הגדרות API של טוויטר (החלף במפתחות שלך)
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# אימות עם ה-API של טוויטר
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# פונקציה לאיסוף ומתן חדשות (רק חדשות כלליות)
def get_latest_news():
    ynet_news = scrape_ynet()
    arutz7_news = scrape_arutz7()
    walla_news = scrape_walla()

    message = "📰 **המבזקים האחרונים** 📰\n\n"
    
    # מוסיפים חדשות מכל אתר (עד 3 כתבות, אך מוגבל ל-280 תווים)
    for site, articles in [('Ynet', ynet_news), ('ערוץ 7', arutz7_news), ('Walla', walla_news)]:
        if articles:
            for article in articles[:1]:  # לוקחים רק כתבה אחת מכל אתר כדי להתאים ל-280 תווים
                if 'time' in article:
                    title_text = f"{article['time']} - {article['title']}"
                else:
                    title_text = article['title']
                link = article['link']
                # בודקים אם נוספה הצלחה לאחר 280 תווים
                if len(message) + len(f"{site}: {title_text[:100]}... {link}\n") <= 280:
                    message += f"{site}: {title_text[:100]}... {link}\n"
                else:
                    break
    
    return message.strip()[:280]  # מבטיחים שלא עוברים את מגבלת 280 תווים

# פונקציה לפרסום ומחיקת ציוץ
def post_and_delete_tweet():
    try:
        # אוספים את החדשות
        news = get_latest_news()
        if not news.strip():
            print(f"{datetime.now()} - אין חדשות חדשות, מדלג...")
            return

        # פרסום ציוץ
        tweet = api.update_status(status=news)
        tweet_id = tweet.id
        print(f"{datetime.now()} - פורסם ציוץ: {news}")

        # המתנה אקראית בין 9 ל-11 דקות (מניעת ספאם)
        wait_time = random.uniform(540, 660)  # 9-11 דקות ב-seconds
        time.sleep(wait_time)

        # מחיקת הציוץ
        api.destroy_status(tweet_id)
        print(f"{datetime.now()} - ציוץ {tweet_id} נמחק")

    except tweepy.TweepyException as e:
        print(f"{datetime.now()} - שגיאה בטוויטר: {e}")
    except Exception as e:
        print(f"{datetime.now()} - שגיאה כללית: {e}")

# הרצת הלולאה הראשית
if __name__ == "__main__":
    print("הבוט מתחיל לעבוד...")

    while True:
        post_and_delete_tweet()
        # המתנה אקראית בין 9 ל-11 דקות לפני מחזור חדש
        wait_time = random.uniform(540, 660)  # 9-11 דקות ב-seconds
        time.sleep(wait_time)
