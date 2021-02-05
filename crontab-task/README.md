
### Crontab
Here we give an example of how to create periodically executing tasks using
native Unix job scheduler [**cron**](https://en.wikipedia.org/wiki/Cron)
and its configuration file **crontab**.

In this example we created two *bash* scripts, which start and stop the alarm
for stand-up. The alarm is visually represented by a
[**blinkstick cube**](https://www.blinkstick.com/products/blinkstick-square#enclosure).

So, execution of these two scripts can be scheduled in the *crontab* file as
follows:
```bash
# standup alarm                                                                 
30 9 * * 1-5 ${HOME}/projects/blinklib/standup-alarm > /dev/null 2>&1           

# kill alarm                                                                    
40 9 * * 1-5 ${HOME}/projects/blinklib/kill-alarm > /dev/null 2>&1
```

Ask around for more details about *crontab* template.
