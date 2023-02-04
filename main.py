import asyncio


## Thoughts:
## We need a way to run the get_times() function every day at midnight or something
## We need a way for our program to know that it's the right time to trigger so it can grab the info from weather, bus times, etc. and send an email to us

## This can probably be done with asyncio, where we have just separate these features into two different functions
## For the first part of 'get_times()' we can call it once, then do asyncio.sleep(86400), the number of seconds in a day. Then it infinite loops back



## Ideas about structure:
#  
#  We can run many clocks. A clock can trigger once per second, once per minute, per day, etc.
#  This is because not every action needs to be run at the same time
#  This can be done with either using 1) asyncio with sleeps that are tied to system clock
#  or 2) a scheduler of some sort
#  This link, https://stackoverflow.com/questions/474528/how-to-repeatedly-execute-a-function-every-x-seconds , can give you the answers

async def daily_clock():


    # to make it better for the first iteration of the program (when we first press run), instead of making it asyncio.sleep() a constant amount of seconds we can calculate 
    # how many seconds are in between now and 00:00am and use that value instead.
    # This way we can start the program at anytime instead of just at 00:00 am.

    pass


async def minute_clock():

    pass


async def main():

    pass



if __name__ == '__main__':
    main()