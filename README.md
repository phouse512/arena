Crowdsourced Animal Crossing
============================

An experiment with old-school GC Animal Crossing played by a large crowd. That
crowd is TBD.

### Scoreboard
Currently all that is displayed on twitch is the actual animal crossing game. Ideally
users should be able to see their contributions and progress somewhere. The metrics I'm
thinking of so far are listed:
- a constantly updating list of registered commands
- top contributors (for now, just a hashmap of accepted commands to usernames)
- lurkers (people that chat, but don't input any controls)

#### Design considerations
- realtime- the display should be a realtime stream of data
- fault-tolerant - my threading code is definitely not perfect, so there will be times when
    I need to restart the server. The scoreboard should be able to handle that
- simple


