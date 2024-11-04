from aqt import mw, gui_hooks
from aqt.webview import WebContent
from aqt.deckbrowser import DeckBrowser
from aqt.reviewer import ReviewerBottomBar
from anki.decks import DeckId
from typing import Any, Optional

ADDON_PREFIX = "study_review_deck_buttons_addon"
WEB_DIRECTORY = f"/_addons/{mw.addonManager.addonFromModule(__name__)}/web"

def handle_pycmd(handled, cmd, context):
    global STATE

    if mw.col.sched.version != 3:
        raise Exception("study-review-deck addon only works with the v3 scheduler")

    if cmd.startswith(pre("start_study")):
        _, deck_id = cmd.split(":")
        start_study(int(deck_id))
        return (True, None)
    if cmd.startswith(pre("start_review")):
        _, deck_id = cmd.split(":")
        start_review(int(deck_id))
        return (True, None)
    if cmd.startswith(pre("wrap_up")):
        wrap_up()
        return (True, None)
    if cmd.startswith(pre("get_learned_today_count")):
        today = mw.col.sched.today
        learned_today = 0
        current_deck = mw.col.decks.current()
        if current_deck['newToday'][0] == today:
            learned_today = current_deck['newToday'][1]
        return (True, learned_today)
    if cmd.startswith(pre("get_config")):
        config = mw.addonManager.getConfig(__name__)
        return (True, config)
    if cmd.startswith(pre("get_state")):
        return (True, STATE)

    return handled

def start_study(deck_id: int):
    global STATE
    global REFRESH_DECKS
    STATE = "study"
    REFRESH_DECKS = True

    # Get the current deck
    current_deck = mw.col.decks.get(DeckId(deck_id))
 
    today = mw.col.sched.today
    # Set "New Cards" amount for today ("Today Only").
    current_deck['newLimitToday'] = { 'limit': 10000, 'today': today }
    # Set "Review Cards" amount for today ("Today Only").
    current_deck['reviewLimitToday'] = { 'limit': 0, 'today': today }

    # Save deck limits
    mw.col.decks.save(current_deck)

    # Set current deck for study
    mw.col.decks.select(DeckId(deck_id))

    # Start study session (review cards == 0)
    mw.moveToState("review")

def start_review(deck_id: int):
    global STATE
    global REFRESH_DECKS
    STATE = "review"
    REFRESH_DECKS = True

    # Get the current deck
    current_deck = mw.col.decks.get(DeckId(deck_id))

    today = mw.col.sched.today 
    # Set "New Cards" amount for today ("Today Only").
    current_deck['newLimitToday'] = { 'limit': 0, 'today': today }
    # Set "Review Cards" amount for today ("Today Only").
    current_deck['reviewLimitToday'] = { 'limit': 10000, 'today': today }

    # Save deck limits
    mw.col.decks.save(current_deck)

    # Set current deck for study
    mw.col.decks.select(DeckId(deck_id))

    # Start review session (study cards == 0)
    mw.moveToState("review")

def wrap_up():
    global STATE
    global REFRESH_DECKS
    STATE = "wrap_up"
    REFRESH_DECKS = True

    today = mw.col.sched.today 
    current_deck = mw.col.decks.current()

    # Set "New Cards" amount to 0 for today. This will effectively
    # ensure that only learned cards will remain in the session.
    current_deck['newLimitToday'] = { 'limit': 0, 'today': today }

    # Save deck limits
    mw.col.decks.save(current_deck)

    # Refresh session
    mw.moveToState("review")


# Unset the "Today Only" limits for all decks to show correct number of reviews
# and new cards in the deck browser.
def reset_limits():
    for deck_id in mw.col.decks.allIds():
        deck = mw.col.decks.get(deck_id)
        deck['newLimitToday'] = { 'limit': 0, 'today': 0 }
        deck['reviewLimitToday'] = { 'limit': 0, 'today': 0 }
        mw.col.decks.save(deck)

def on_webview(web_content: WebContent, context: Optional[Any]) -> None:
    global REFRESH_DECKS

    # Append script that adds buttons to the deck browser.
    if isinstance(context, DeckBrowser):
        if REFRESH_DECKS:
            reset_limits()
            REFRESH_DECKS = False
            mw.moveToState("deckBrowser")
        web_content.js.append(f"{WEB_DIRECTORY}/deck-buttons.js")

    # Append script that shows "learned today" number next to the
    # new cards count in the stats (bottom bar).
    if isinstance(context, ReviewerBottomBar):
        web_content.js.append(f"{WEB_DIRECTORY}/review-stats.js")

# Setup addon.
STATE = "none"
REFRESH_DECKS = False
mw.addonManager.setWebExports(__name__, r"web/.*")
gui_hooks.webview_will_set_content.append(on_webview)
gui_hooks.webview_did_receive_js_message.append(handle_pycmd)


# 
# Utility Functions

# Print to the webview console.
def print_console(arg):
    mw.web.eval(f'console.log(`{arg}`)')

# Prefix string with the addon identifier to avoid name collisions.
def pre(string: str):
    return f"{ADDON_PREFIX}_{string}"