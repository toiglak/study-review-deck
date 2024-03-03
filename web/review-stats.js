const ADDON_PREFIX = "study_review_deck_buttons_addon";

async function main() {
  // Add count of the new cards learned today next to the total
  // available new cards count. This is useful to know, so that you
  // can plan out how many new words you want to learn today.
  on_added(".new-count", async (element) => {
    // Target underline element (<u>) if it exists.
    if (element.children.length > 0) element = element.firstChild;

    let learned_today = await cmd("get_learned_today_count");
    if (learned_today !== 0) element.textContent += `(${learned_today})`;
  });

  // Add 🏁 icon next to "Show Answer" and add a line separator
  // between the two. I know this solution is not perfect, but it's
  // the best I can do with this Anki's layout (without like
  // rewriting everything).
  on_added("#ansbut", async (element) => {
    // Add wrap up button only in the "study" session.
    if ((await cmd("get_state")) != "study") {
      return;
    }

    let wrapup_btn = document.createElement("span");
    wrapup_btn.innerHTML = " | 🏁";
    wrapup_btn.title = "Wrap up the study session.";
    wrapup_btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      await cmd("wrap_up");
    });

    let stats = document.querySelector(".stattxt");
    element.insertBefore(wrapup_btn, stats);
  });
}

window.addEventListener("DOMContentLoaded", main);

//
// Utility functions.

function on_added(selector, callback) {
  let processed_nodes = new Set();
  let observer = new MutationObserver((mutationsList, observer) => {
    for (let mutation of mutationsList) {
      if (mutation.type === "childList") {
        let element = document.querySelector(selector);
        if (element && !processed_nodes.has(element)) {
          observer.disconnect();
          processed_nodes.add(element);
          callback(element);
          observer.observe(document, { childList: true, subtree: true });
        }
        mutation.removedNodes.forEach((node) => {
          if (node.matches && node.matches(selector)) {
            processed_nodes.delete(node);
          }
        });
      }
    }
  });
  observer.observe(document, { childList: true, subtree: true });
}

// Prefix string with a unique addon identifier to avoid name collisions.
function pre(string) {
  return `${ADDON_PREFIX}_${string}`;
}

// Send a command to the Anki addon. You can await for the return value.
async function cmd(command, ...arg) {
  return new Promise((resolve, _reject) => {
    pycmd(pre(command) + ":" + arg.join(":"), (ret) => {
      resolve(ret);
    });
  });
}
