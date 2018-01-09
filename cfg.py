from datetime import timedelta

# After one day the Api token will expire + the session is going to be reset so the user needs to login and he will therefore generate a new API key
app_timedeltaExpiration = timedelta(days = 1)
app_secret = 'thisisaveryspecialsecretkey'
