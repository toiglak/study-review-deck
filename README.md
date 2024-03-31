Compatible with Anki versions: 2.1.61 and above

---

# Study-Review Deck

This add-on allows you to separate the study and review phases of your Anki sessions, by adding "Study" and "Review" buttons for each deck. It is useful when you want to study new cards without being interrupted by reviews.

<p align="center">
  <img width="735" alt="Main window showing 'Study' and 'Review' buttons" src="https://github.com/toiglak/study-review-deck-buttons/assets/37531387/10916f28-1c3a-4cda-80a2-caebb9b64867">
</p>

Clicking "Review" initiates a session with only the cards due for review. \
Clicking "Study" starts a session with only new cards.

During a study session, a "Wrap Up" (🏁) button appears next to the "Show Answer" button. This button removes new cards from the queue, allowing you to review the remaining cards and finish the session. This is especially useful when you have a large number of new cards in a deck.

<p align="center">
  <img width="735" alt="Study session showing 'Wrap Up' button" src="https://github.com/toiglak/study-review-deck-buttons/assets/37531387/628d7c0d-2bff-4a31-813a-8577bf0a34bf">  
</p>

## Installation

1. Optional but recommended: [Create a backup](https://docs.ankiweb.net/backups.html#manual-colpkg-backups) of your collection.
2. Make sure that you're using Scheduler V3.
3. Download and install the add-on, then restart Anki.
4. Enable "New cards ignore review limit" option for all your decks.

## Important Information

- This add-on operates by setting "Today only" daily limit for new cards and reviews. If you decide to uninstall this add-on, you may need to manually reset these limits in the deck options.
- Syncing with AnkiWeb during a session may hide today's reviews (as the "Today's limit" will still be set). If this happens, return to the main view (with the deck list) and then sync.
- The "Study" button does not currently support nested decks.
- I've shared this add-on because I find it useful, but please note that there may be bugs or things I didn't account for. Also, while it works for me, it may not fit your workflow. Use at your own discretion.

## License

This add-on is licensed under the GNU Affero General Public License, version 3 (AGPL-3.0). You can find a copy of the license in the [LICENSE](LICENSE) file.
