
def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60

    days_text = "day{}".format("s" if days!=1 else "")
    hours_text = "hour{}".format("s" if hours!=1 else "")
    minutes_text = "minute{}".format("s" if minutes!=1 else "")
    seconds_text = "second{}".format("s" if seconds!=1 else "")

    result = ", ".join(filter(lambda x: bool(x),[
        "{0} {1}".format(days, days_text) if days else "",
        "{0} {1}".format(hours, hours_text) if hours else "",
        "{0} {1}".format(minutes, minutes_text) if minutes else "",
        "{0} {1}".format(seconds, seconds_text) if seconds else ""
    ]))

    return result
