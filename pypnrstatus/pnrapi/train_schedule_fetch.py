import train_schedule

train = train_schedule.TrainSearch("12345")#month and day are highly recommended
if train.request():
    print train.get_json()
else:
    print train.error