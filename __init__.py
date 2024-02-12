from aqt import mw, gui_hooks
from aqt.webview import WebContent
from aqt.deckbrowser import DeckBrowser
from aqt.reviewer import ReviewerBottomBar
from anki.decks import DeckId
from typing import Any, Optional

ADDON_PREFIX = "study_review_deck_buttons_addon"
WEB_DIRECTORY = f"/_addons/{mw.addonManager.addonFromModule(__name__)}/web"

def handle_pycmd(handled, cmd, context):
    global REFRESH_VIEW
    if cmd.startswith(pre("start_study")):
        REFRESH_VIEW = True
        _, deck_id = cmd.split(":")
        start_study(int(deck_id))
        return (True, None)
    if cmd.startswith(pre("start_review")):
        REFRESH_VIEW = True
        _, deck_id = cmd.split(":")
        start_review(int(deck_id))
        return (True, None)
    if cmd.startswith(pre("get_learned_today_count")):
        # TODO: Ensure that today == today?
        learned_today = mw.col.decks.current()['newToday'][1]
        return (True, learned_today)

    return handled

def start_study(deck_id: int):
    # Get the current deck
    current_deck = mw.col.decks.get(DeckId(deck_id))
 
    today = mw.col.sched.today
    # Set "New Cards" value for "Today Only".
    current_deck['newLimitToday'] = {'limit': 10000, 'today': today}
    # Set "Review Cards" value for "Today Only".
    current_deck['reviewLimitToday'] = { 'limit': 0, 'today': today }

    # Save deck limits
    mw.col.decks.save(current_deck)

    # Set current deck for study
    mw.col.decks.select(DeckId(deck_id))

    # Start study session (review cards == 0)
    mw.moveToState("review")

def start_review(deck_id: int):
    # Get the current deck
    current_deck = mw.col.decks.get(DeckId(deck_id))

    today = mw.col.sched.today 
    # Set "New Cards" value for "Today Only".
    current_deck['newLimitToday'] = {'limit': 0, 'today': today}
    # Set "Review Cards" value for "Today Only".
    current_deck['reviewLimitToday'] = { 'limit': 10000, 'today': today }

    # Save deck limits
    mw.col.decks.save(current_deck)

    # Set current deck for study
    mw.col.decks.select(DeckId(deck_id))

    # Start review session (study cards == 0)
    mw.moveToState("review")

# Unset the "Today Only" limits for all decks to show correct number of reviews
# and new cards in the deck browser.
def reset_limits():
    for deck_id in mw.col.decks.allIds():
        deck = mw.col.decks.get(deck_id)
        deck['newLimitToday'] = {'limit': 0, 'today': 0}
        deck['reviewLimitToday'] = { 'limit': 0, 'today': 0 }
        mw.col.decks.save(deck)

# Append script that adds buttons to the deck browser.
def on_webview(web_content: WebContent, context: Optional[Any]) -> None:
    global REFRESH_VIEW

    if isinstance(context, DeckBrowser):
        if REFRESH_VIEW:
            reset_limits()
            REFRESH_VIEW = False
            mw.moveToState("deckBrowser")
        web_content.js.append(f"{WEB_DIRECTORY}/list-buttons.js")

    if isinstance(context, ReviewerBottomBar):
        web_content.js.append(f"{WEB_DIRECTORY}/review-stats.js")

# Setup addon.
REFRESH_VIEW = False
mw.addonManager.setWebExports(__name__, r"web/.*")
gui_hooks.webview_will_set_content.append(on_webview)
gui_hooks.webview_did_receive_js_message.append(handle_pycmd)


# 
# Utility Functions

# Print to the webview console.
def print_console(arg):
    mw.web.eval(f'console.log(`{arg}`)')

# Prefix string with a unique addon identifier to avoid name collisions.
def pre(string: str):
    return f"{ADDON_PREFIX}_{string}"