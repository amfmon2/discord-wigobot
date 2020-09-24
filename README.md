# WigoBot
Discord bot used for various RO-related activities by Wigo Guild.

## How To Use
- Type `-check <mvp_name>` to see location of MVP and last kill time.
- Type `-kill <mvp_name>` to set current time as MVP's last kill, and to set reminder for minimum and maximum spawn time
- Type `-spot <time_of_death> <mvp_name>` to add kill reminders on specified time. Note that `<time_of_death>` must be in 24-hour `HH:MM` format.

## How To Configure
1. Open `credentials.txt` and insert your Discord Bot token and MongoDB connection string.
2. Edit `gcm_hour_adjustment` inside `wigobot.py` to reflect correct time-zone relative to PH. (GCM is GMT 0 for reference.)
3. Edit `db, mvp_tracker and mvp_names` inside `wigobot.py` to set your MongoDB database and collection names.



