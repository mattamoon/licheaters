# Lichess API

###Download Speed:
The game stream is throttled, depending on who is making the request:

- Anonymous request: 20 games per second
- OAuth2 authenticated request: 30 games per second
- Authenticated, downloading your own games: 60 games per second
- https://lichess.org/api#tag/Games/operation/apiGamesUser

**Records reviewed without API Key**: 350 <br> 
**Time elapsed**: 21.27 seconds

**Records reviewed with API Key**: 350 <br>
**Time elapsed**: 9.13 seconds
---

# Setup Lichess API Key (_not required_)
1. Login @ [lichess.org]()
2. Profile > Preferences > API access tokens
3. https://lichess.org/account/oauth/token

