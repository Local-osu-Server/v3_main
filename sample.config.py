from typing import Optional

# Just a note
# When doing the -devserver method
# be sure to put the domain 'coverbancho.tk' in as the domain
# it will redirect back to your local host and you can be
# good. Only change if testing and I probably won't provide
# little support on setting that up

# domain for the server isn't a necessary thing,
# domain: str = 'coverbancho.tk'

paths: dict[str, Optional[str]] = {
    'osu! path': '', # if provided no need to fill in below
                     # unless songs, replay, and ss folder are somewhere else 
    
    'songs': None, # osu! songs folder
    'replay': None, # osu! replay folder
    'screenshots': None # osu! screenshot folder
}

"""Ingame Config"""
player_name: str = 'Guest' # ingame name

# example: ('link to image', 'click link')
menu_icon: Optional[tuple[str, str]] = None

"""Server Config"""
# needed for loading leaderboards
# if `None` then leaderboards won't load nor score submission
osu_api_key: Optional[str] = '' 

# TODO: probably gonna remove this and
# find a way to just copy the image into your clip board
# but if u want ur screenshots to be uploaded
# get your client id here https://api.imgur.com/
# if `None` it won't upload screenshots
imgur_client_id: Optional[str] = ''

# that is if you want ur bancho rank to show up
# if `None` it will show you as rank 1
osu_daily_api_key: Optional[str] = ''

# sign up for one right here https://beatconnect.io/accounts/privatesignup/
# if `None` then direct won't work/will be disabled
beatconnect_api_key: Optional[str] = '' 

# list of urls, example: ('https://dsada.png', https://dsad11a.png)
# if `None` then it will just show no background
# unless you have the skin background inabled
seasonal_bgs: Optional[tuple[str]] = ('',) 