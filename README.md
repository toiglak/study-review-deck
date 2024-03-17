
---

This add-on allows you to separate the study and review phases of your Anki sessions, by adding "Study" and "Review" buttons for each deck in the main window.

When you click "Study", you will start a session with only new cards. When you click "Review", you will start a session with only cards that are due for review. This is useful when you want to study new cards without being interrupted by reviews.

> TODO: Reword above paragraph. We could just leave "This is useful when you want to study new cards without being interrupted by reviews" without explaining what "Study" and "Review" buttons do, since it's already explained in the first paragraph ("separate the study and review phases of your Anki sessions").

> TODO: Add image of the main window (without morphman and heatmap).

---

Additionally, in the study session, a "Wrap Up" (🏁) button is added. Pressing this button will remove new cards from the queue, allowing you to review the remaining words and wrap up the session.

This add-on also shows the number of new cards learned today above the "Show Answer" button, so that you can decide when to wrap up your studies.

> TODO: Add image of the study session (without morphman).


## Compatibility warning

This add-on requires Scheduler V3 (because it works by setting "Today Only" limit for new/review cards). It should be compatible with Anki versions X and later.


---

# TODO: Before releasing to AnkiWeb

- [ ] Nested decks
    - When studying, new cards will only appear if any of the subdecks has new cards set. However, since we set limts for all decks to 0 (including subdecks), parent deck won't show any new cards.
    - Solution: Remove limits for all subdecks when pressing "study" or "review" in the parent deck.
      - Reasoning: the point of this plugin is "user wants to study cards from one of the decks specifically". If they click on a nested deck, then they obviously want to study cards from all of its subdecks.

- [ ] "New cards ignore review limit" must be set in deck's config.
    - This is a requirement for the add-on's 'study' feature to work, as otherwise no new cards will be added to the queue.
    - We could set this option automatically, but then we should probably mention to the user that we did that (and also which deck options this plugin changes, so that user can revert them in case they want to).

- [ ] Check what is the oldest version of the Anki that supports this add-on.
    - The simplest way to do that would be to check it on different user account, or on Windows.
    - Though, in theory, an easiest way would be to simply backup the `iglak/Library/Anki2` folder and then just open older versions of Anki.