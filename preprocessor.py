import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date']= df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    period =[ ]

    for hour in df[['day_name','hour']]['hour']:
        if hour ==23:
            period.append(str(hour) + "-" + str('00'))
        elif hour ==0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period']=period

    # UPDATED: Phone Number Masking (Security) — masks both user names and messages
    def mask_phone_number(text):
        text = str(text)
        # Pattern 1: +91 98765 43210 or +91-98765-43210 or +919876543210
        text = re.sub(r'(\+?\d{1,3}[\s-]?)(\d{5})[\s-]?(\d{5})', r'\1\2XXXXX', text)
        # Pattern 2: bare 10-digit Indian numbers (no country code)
        text = re.sub(r'\b(\d{5})(\d{5})\b', r'\1XXXXX', text)
        return text

    df['user'] = df['user'].apply(mask_phone_number)
    df['message'] = df['message'].apply(mask_phone_number)

    return df